#!/usr/bin/env python3
"""
Shared WooCommerce REST v3 client.

Handles the three things every caller needs and none of them should reimplement:
signing, retries, and pagination.

Auth note: WooCommerce only accepts HTTP Basic on an HTTPS store. Over plain HTTP it
requires OAuth 1.0a one-legged signing, which is what this client always uses. The same
signature is accepted on HTTPS, so callers do not branch on scheme.

Credentials come from the environment (or a .env file passed to load_env). They are
never written into this file.
"""

import base64
import hashlib
import hmac
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

RETRY_STATUSES = {429, 500, 502, 503, 504}
MAX_ATTEMPTS = 4


class WooError(RuntimeError):
    def __init__(self, status, body, url):
        self.status = status
        self.body = body
        self.url = url
        super().__init__("HTTP %s on %s: %s" % (status, url, body[:400]))


def load_env(path):
    """Read KEY=VALUE lines into os.environ without overwriting real env vars."""
    if not path or not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


class WooClient:
    def __init__(self, base_url=None, consumer_key=None, consumer_secret=None):
        self.base_url = (base_url or os.environ.get("WOO_URL", "")).rstrip("/")
        self.key = consumer_key or os.environ.get("WOO_CONSUMER_KEY", "")
        self.secret = consumer_secret or os.environ.get("WOO_CONSUMER_SECRET", "")

        missing = [
            name
            for name, value in (
                ("WOO_URL", self.base_url),
                ("WOO_CONSUMER_KEY", self.key),
                ("WOO_CONSUMER_SECRET", self.secret),
            )
            if not value
        ]
        if missing:
            raise SystemExit("Missing credentials: %s" % ", ".join(missing))

    # ---- signing -------------------------------------------------------

    @staticmethod
    def _quote(value):
        return urllib.parse.quote(str(value), safe="")

    def _sign(self, method, url, params):
        normalized = "&".join(
            "%s=%s" % (self._quote(k), self._quote(v)) for k, v in sorted(params.items())
        )
        base_string = "&".join([method.upper(), self._quote(url), self._quote(normalized)])
        signing_key = (self.secret + "&").encode()
        digest = hmac.new(signing_key, base_string.encode(), hashlib.sha256).digest()
        return base64.b64encode(digest).decode()

    def _signed_url(self, method, path, query=None):
        url = "%s/wp-json/wc/v3/%s" % (self.base_url, path.lstrip("/"))
        params = dict(query or {})
        params.update(
            {
                "oauth_consumer_key": self.key,
                "oauth_nonce": uuid.uuid4().hex,
                "oauth_signature_method": "HMAC-SHA256",
                "oauth_timestamp": str(int(time.time())),
            }
        )
        params["oauth_signature"] = self._sign(method, url, params)
        return url + "?" + urllib.parse.urlencode(params)

    # ---- transport -----------------------------------------------------

    def request(self, method, path, query=None, payload=None):
        last_error = None
        for attempt in range(1, MAX_ATTEMPTS + 1):
            url = self._signed_url(method, path, query)
            body = json.dumps(payload).encode() if payload is not None else None
            req = urllib.request.Request(url, data=body, method=method.upper())
            if body is not None:
                req.add_header("Content-Type", "application/json")
            try:
                with urllib.request.urlopen(req, timeout=120) as response:
                    raw = response.read().decode("utf-8")
                    return json.loads(raw) if raw else None
            except urllib.error.HTTPError as exc:
                text = exc.read().decode("utf-8", "replace")
                if exc.code in RETRY_STATUSES and attempt < MAX_ATTEMPTS:
                    last_error = WooError(exc.code, text, url)
                    time.sleep(2 ** attempt)
                    continue
                raise WooError(exc.code, text, url) from exc
            except urllib.error.URLError as exc:
                if attempt < MAX_ATTEMPTS:
                    last_error = exc
                    time.sleep(2 ** attempt)
                    continue
                raise
        raise last_error

    def get(self, path, **query):
        return self.request("GET", path, query=query)

    def post(self, path, payload, **query):
        return self.request("POST", path, query=query, payload=payload)

    def paged(self, path, per_page=100, **query):
        """Yield every record across pages. WooCommerce caps per_page at 100."""
        page = 1
        while True:
            batch = self.get(path, per_page=per_page, page=page, **query)
            if not batch:
                return
            for item in batch:
                yield item
            if len(batch) < per_page:
                return
            page += 1
