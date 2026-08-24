import React, { useState } from 'react';

interface SafeImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
    fallbackUrl?: string;
}

// 光之淨化：不再依賴外部佔位圖服務（外部佔位圖源不穩定、可能被擋）。
// 改用內建 SVG data URI——永遠載得到、零外部依賴、無 AI 指紋。
const LOCAL_FALLBACK =
    "data:image/svg+xml;utf8," +
    encodeURIComponent(
        `<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800">` +
        `<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">` +
        `<stop offset="0" stop-color="#232a30"/><stop offset="1" stop-color="#12171c"/>` +
        `</linearGradient></defs>` +
        `<rect width="800" height="800" fill="url(#g)"/>` +
        `<circle cx="400" cy="380" r="120" fill="none" stroke="#e8934a" stroke-width="3" opacity="0.5"/>` +
        `<text x="400" y="580" text-anchor="middle" fill="#8fa3b8" font-family="sans-serif" font-size="28" letter-spacing="4">VANGUARD GEAR</text>` +
        `</svg>`
    );

export const SafeImage: React.FC<SafeImageProps> = ({
    src,
    alt,
    fallbackUrl = LOCAL_FALLBACK,
    ...props
}) => {
    const [error, setError] = useState(false);

    if (error || !src) {
        return <img src={fallbackUrl} alt={alt} {...props} />;
    }

    return (
        <img
            src={src}
            alt={alt}
            onError={() => setError(true)}
            {...props}
        />
    );
};
