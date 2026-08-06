import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import type { CartItem, WooProduct } from '../types';
import { storeAddToCart } from '../services/api';

interface CartContextType {
    cartItems: CartItem[];
    addToCart: (product: WooProduct, quantity?: number) => Promise<void>;
    removeFromCart: (productId: number) => void;
    updateQuantity: (productId: number, quantity: number) => void;
    isDrawerOpen: boolean;
    setIsDrawerOpen: (isOpen: boolean) => void;
    cartTotal: number;
    itemCount: number;
}

const CartContext = createContext<CartContextType | null>(null);

export const CartProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [cartItems, setCartItems] = useState<CartItem[]>(() => {
        const saved = localStorage.getItem('auraguard_cart');
        return saved ? JSON.parse(saved) : [];
    });
    const [isDrawerOpen, setIsDrawerOpen] = useState(false);

    useEffect(() => {
        localStorage.setItem('auraguard_cart', JSON.stringify(cartItems));
    }, [cartItems]);

    const addToCart = async (product: WooProduct, quantity = 1) => {
        try {
            if (import.meta.env.VITE_WOO_URL) {
                // Live mode
                await storeAddToCart(product.id, quantity);
            }
        } catch {
            // Ignore for mock mode or fallback
        }

        setCartItems(prev => {
            const existing = prev.find(item => item.product.id === product.id);
            if (existing) {
                return prev.map(item =>
                    item.product.id === product.id ? { ...item, quantity: item.quantity + quantity } : item
                );
            }
            return [...prev, { product, quantity }];
        });

        // Show toast or open drawer
        setIsDrawerOpen(true);
    };

    const removeFromCart = (productId: number) => {
        setCartItems(prev => prev.filter(item => item.product.id !== productId));
    };

    const updateQuantity = (productId: number, quantity: number) => {
        if (quantity <= 0) {
            removeFromCart(productId);
            return;
        }
        setCartItems(prev =>
            prev.map(item => (item.product.id === productId ? { ...item, quantity } : item))
        );
    };

    const cartTotal = cartItems.reduce((sum, item) => sum + parseFloat(item.product.price || '0') * item.quantity, 0);
    const itemCount = cartItems.reduce((sum, item) => sum + item.quantity, 0);

    return (
        <CartContext.Provider
            value={{
                cartItems,
                addToCart,
                removeFromCart,
                updateQuantity,
                isDrawerOpen,
                setIsDrawerOpen,
                cartTotal,
                itemCount,
            }}
        >
            {children}
        </CartContext.Provider>
    );
};

export const useCart = () => {
    const ctx = useContext(CartContext);
    if (!ctx) throw new Error('useCart must be used within CartProvider');
    return ctx;
};
