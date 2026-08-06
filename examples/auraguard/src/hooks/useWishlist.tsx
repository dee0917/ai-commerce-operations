import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import type { } from '../types';

interface WishlistContextType {
    wishlistIds: number[];
    toggleWishlist: (productId: number) => void;
    isInWishlist: (productId: number) => boolean;
}

const WishlistContext = createContext<WishlistContextType | null>(null);

export const WishlistProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [wishlistIds, setWishlistIds] = useState<number[]>(() => {
        const saved = localStorage.getItem('auraguard_wishlist');
        return saved ? JSON.parse(saved) : [];
    });

    useEffect(() => {
        localStorage.setItem('auraguard_wishlist', JSON.stringify(wishlistIds));
    }, [wishlistIds]);

    const toggleWishlist = (productId: number) => {
        setWishlistIds(prev =>
            prev.includes(productId) ? prev.filter(id => id !== productId) : [...prev, productId]
        );
    };

    const isInWishlist = (productId: number) => wishlistIds.includes(productId);

    return (
        <WishlistContext.Provider value={{ wishlistIds, toggleWishlist, isInWishlist }}>
            {children}
        </WishlistContext.Provider>
    );
};

export const useWishlist = () => {
    const ctx = useContext(WishlistContext);
    if (!ctx) throw new Error('useWishlist must be used within WishlistProvider');
    return ctx;
};
