#!/usr/bin/env node
/**
 * Converts a storefront's src/data/mockData.ts into a neutral product feed JSON.
 *
 * The generated sites keep their seed catalogue as TypeScript. This reads that file
 * without a build step by stripping the type annotations and importing it as ESM, so a
 * site that was built against mock data can be pushed into a real store unchanged.
 *
 * Usage: node export_mock_feed.mjs <path/to/mockData.ts> <path/to/out.json>
 */

import { readFile, writeFile, unlink } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
import os from 'node:os';

const [source, target] = process.argv.slice(2);
if (!source || !target) {
    console.error('Usage: node export_mock_feed.mjs <mockData.ts> <out.json>');
    process.exit(1);
}

const raw = await readFile(source, 'utf8');

const stripped = raw
    .split('\n')
    .filter((line) => !/^\s*import\s+type\s/.test(line))
    .join('\n')
    // `export const mockProducts: WooProduct[] = [` -> `export const mockProducts = [`
    .replace(/:\s*[A-Za-z_$][\w$]*\[\]\s*=/g, ' =')
    .replace(/:\s*[A-Za-z_$][\w$]*\s*=\s*\[/g, ' = [');

const tempFile = path.join(os.tmpdir(), `acp-feed-${process.pid}.mjs`);
await writeFile(tempFile, stripped, 'utf8');

let mod;
try {
    mod = await import(pathToFileURL(tempFile).href);
} finally {
    await unlink(tempFile).catch(() => {});
}

const products = mod.mockProducts ?? [];
const categories = mod.mockCategories ?? [];

if (!products.length) {
    console.error(`No products exported from ${source}`);
    process.exit(1);
}

const feed = {
    categories: categories.map((c) => ({ name: c.name, slug: c.slug })),
    products: products.map((p) => ({
        name: p.name,
        slug: p.slug,
        sku: p.sku,
        description: p.description ?? '',
        short_description: p.short_description ?? '',
        regular_price: String(p.regular_price ?? p.price ?? '0'),
        sale_price: p.sale_price ? String(p.sale_price) : '',
        stock_quantity: p.stock_quantity ?? null,
        stock_status: p.stock_status ?? 'instock',
        categories: (p.categories ?? []).map((c) => c.slug ?? c.name),
        // Local paths under the site's public/ folder; the importer resolves them to files.
        images: (p.images ?? []).map((img) => img.src),
    })),
};

await writeFile(target, JSON.stringify(feed, null, 2), 'utf8');
console.log(`Wrote ${feed.products.length} products and ${feed.categories.length} categories to ${target}`);
