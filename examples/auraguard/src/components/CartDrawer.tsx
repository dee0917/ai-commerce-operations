import React, { useEffect, useRef } from 'react';
import { X, Minus, Plus, ShoppingBag } from 'lucide-react';
import { useCart } from '../hooks/useCart';
import clsx from 'clsx';
import { Link } from 'react-router-dom';

const CartDrawer: React.FC = () => {
    const { cartItems, isDrawerOpen, setIsDrawerOpen, updateQuantity, removeFromCart, cartTotal } = useCart();
    const drawerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handleEscape = (e: KeyboardEvent) => {
            if (e.key === 'Escape') setIsDrawerOpen(false);
        };
        if (isDrawerOpen) {
            document.addEventListener('keydown', handleEscape);
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'unset';
        }
        return () => {
            document.removeEventListener('keydown', handleEscape);
            document.body.style.overflow = 'unset';
        };
    }, [isDrawerOpen, setIsDrawerOpen]);

    return (
        <>
            {/* Backdrop */}
            <div
                className={clsx(
                    "fixed inset-0 bg-brand-secondary/40 backdrop-blur-sm z-50 transition-opacity duration-300",
                    isDrawerOpen ? "opacity-100" : "opacity-0 pointer-events-none"
                )}
                onClick={() => setIsDrawerOpen(false)}
            />

            {/* Drawer */}
            <div
                ref={drawerRef}
                className={clsx(
                    "fixed top-0 right-0 h-full w-full sm:w-[500px] bg-brand-primary z-50 shadow-2xl flex flex-col transform transition-transform duration-300 ease-out",
                    isDrawerOpen ? "translate-x-0" : "translate-x-full"
                )}
            >
                <div className="flex items-center justify-between p-6 border-b border-brand-secondary/10">
                    <h2 className="font-display text-2xl tracking-widest uppercase">Your Cart</h2>
                    <button onClick={() => setIsDrawerOpen(false)} className="p-2 hover:bg-brand-secondary/5 rounded-full transition-colors">
                        <X className="w-5 h-5" />
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-6">
                    {cartItems.length === 0 ? (
                        <div className="flex-1 flex flex-col items-center justify-center text-center opacity-60">
                            <ShoppingBag className="w-12 h-12 mb-4 animate-bounce" />
                            <p className="font-display text-lg uppercase tracking-widest">Your cart is empty.</p>
                            <button
                                onClick={() => setIsDrawerOpen(false)}
                                className="mt-6 uppercase text-sm border-b-2 border-brand-secondary pb-1 tracking-widest hover:text-brand-accent hover:border-brand-accent transition-colors"
                            >
                                Continue Shopping
                            </button>
                        </div>
                    ) : (
                        cartItems.map((item) => (
                            <div key={item.product.id} className="flex gap-4 group">
                                <Link to={`/product/${item.product.slug}`} className="block w-24 h-32 shrink-0 overflow-hidden bg-brand-secondary/5">
                                    <img
                                        src={item.product.images[0]?.src}
                                        alt={item.product.images[0]?.alt}
                                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                                    />
                                </Link>

                                <div className="flex-1 flex flex-col justify-between py-1">
                                    <div>
                                        <div className="flex justify-between items-start gap-2">
                                            <Link to={`/product/${item.product.slug}`} className="font-display text-lg leading-tight hover:text-brand-accent transition-colors">
                                                {item.product.name}
                                            </Link>
                                            <button onClick={() => removeFromCart(item.product.id)} className="p-1 hover:text-brand-accent transition-colors">
                                                <X className="w-4 h-4" />
                                            </button>
                                        </div>
                                        <div className="mt-1 text-sm font-medium">
                                            ${item.product.price}
                                        </div>
                                    </div>

                                    <div className="flex items-center border border-brand-secondary w-fit">
                                        <button
                                            className="px-3 py-1 hover:bg-brand-secondary hover:text-brand-primary transition-colors"
                                            onClick={() => updateQuantity(item.product.id, item.quantity - 1)}
                                        >
                                            <Minus className="w-3 h-3" />
                                        </button>
                                        <span className="px-4 py-1 text-sm font-medium w-8 text-center">{item.quantity}</span>
                                        <button
                                            className="px-3 py-1 hover:bg-brand-secondary hover:text-brand-primary transition-colors"
                                            onClick={() => updateQuantity(item.product.id, item.quantity + 1)}
                                        >
                                            <Plus className="w-3 h-3" />
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>

                {cartItems.length > 0 && (
                    <div className="p-6 border-t border-brand-secondary/10 bg-brand-primary/50 backdrop-blur-md">
                        <div className="flex justify-between items-center mb-6 font-display text-xl uppercase tracking-widest">
                            <span>Subtotal</span>
                            <span>${cartTotal.toFixed(2)}</span>
                        </div>
                        <p className="text-xs text-center mb-6 opacity-60 uppercase tracking-widest">Taxes and shipping calculated at checkout</p>
                        <Link
                            to="/checkout"
                            onClick={() => setIsDrawerOpen(false)}
                            className="w-full block text-center bg-brand-secondary text-brand-primary py-4 uppercase tracking-[0.2em] font-medium hover:bg-brand-accent transition-colors shadow-lg"
                        >
                            Checkout
                        </Link>
                    </div>
                )}
            </div>
        </>
    );
};

export default CartDrawer;
