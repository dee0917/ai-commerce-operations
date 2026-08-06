import React, { useState } from 'react';

interface SafeImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
    fallbackUrl?: string;
}

export const SafeImage: React.FC<SafeImageProps> = ({
    src,
    alt,
    fallbackUrl = "https://placehold.co/800x800/121212/FF3D00?text=VANGUARD+GEAR+MATERIAL+PENDING",
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
