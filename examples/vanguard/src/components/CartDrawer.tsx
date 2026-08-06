import React from 'react';
import { X, ShoppingBag, Plus, Minus, Trash2, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../hooks/useCart';
import { AnimatePresence, motion } from 'framer-motion';

interface CartDrawerProps {
    isOpen: boolean;
    onClose: () => void;
}

export const CartDrawer: React.FC<CartDrawerProps> = ({ isOpen, onClose }) => {
    const { items, updateQuantity, removeItem, totalPrice, totalItems } = useCart();
    const navigate = useNavigate();

    const goToCart = () => {
        onClose();
        navigate('/cart');
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    {/* Overlay */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                        className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[60]"
                    />

                    {/* Drawer */}
                    <motion.div
                        initial={{ x: '100%' }}
                        animate={{ x: 0 }}
                        exit={{ x: '100%' }}
                        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                        className="fixed right-0 top-0 h-full w-full max-w-md bg-vanguard-obsidian border-l border-vanguard-slate/30 z-[70] flex flex-col shadow-2xl"
                    >
                        {/* Header */}
                        <div className="p-6 border-b border-vanguard-slate/20 flex items-center justify-between bg-vanguard-industrial">
                            <div className="flex items-center gap-3">
                                <ShoppingBag className="text-vanguard-red" size={20} />
                                <h2 className="font-mono text-lg font-bold uppercase tracking-widest">Your Kit</h2>
                                <span className="bg-vanguard-red text-white text-[10px] px-2 py-0.5 rounded-full">
                                    {totalItems()}
                                </span>
                            </div>
                            <button
                                onClick={onClose}
                                className="p-2 hover:bg-white/10 rounded-full transition-colors"
                                aria-label="Close drawer"
                            >
                                <X size={20} />
                            </button>
                        </div>

                        {/* Content */}
                        <div className="flex-grow overflow-y-auto p-6 no-scrollbar">
                            {items.length === 0 ? (
                                <div className="h-full flex flex-col items-center justify-center text-center opacity-40">
                                    <ShoppingBag size={64} className="mb-4 stroke-[1px]" />
                                    <p className="font-mono text-sm uppercase">Empty Inventory</p>
                                    <p className="text-xs mt-2">Ready for deployment.</p>
                                </div>
                            ) : (
                                <div className="space-y-6">
                                    {items.map((item) => (
                                        <div key={item.id} className="flex gap-4 group">
                                            <div className="h-24 w-24 flex-shrink-0 bg-vanguard-industrial rounded border border-vanguard-slate/20 overflow-hidden">
                                                <img
                                                    src={item.product.images[0].src}
                                                    alt={item.product.name}
                                                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                                                />
                                            </div>
                                            <div className="flex-grow flex flex-col">
                                                <div className="flex justify-between items-start">
                                                    <h3 className="font-mono text-xs font-bold uppercase tracking-tight line-clamp-1">
                                                        {item.product.name}
                                                    </h3>
                                                    <button
                                                        onClick={() => removeItem(item.product.id)}
                                                        className="text-slate-500 hover:text-vanguard-red transition-colors"
                                                    >
                                                        <Trash2 size={14} />
                                                    </button>
                                                </div>
                                                <p className="text-[10px] text-slate-500 mt-1 mb-3">SKU: {item.product.sku}</p>

                                                <div className="mt-auto flex justify-between items-center">
                                                    <div className="flex items-center border border-vanguard-slate/30 bg-black/20">
                                                        <button
                                                            onClick={() => updateQuantity(item.product.id, item.quantity - 1)}
                                                            className="p-1.5 hover:bg-vanguard-red hover:text-white transition-colors"
                                                        >
                                                            <Minus size={12} />
                                                        </button>
                                                        <span className="w-8 text-center font-mono text-xs">{item.quantity}</span>
                                                        <button
                                                            onClick={() => updateQuantity(item.product.id, item.quantity + 1)}
                                                            className="p-1.5 hover:bg-vanguard-red hover:text-white transition-colors"
                                                        >
                                                            <Plus size={12} />
                                                        </button>
                                                    </div>
                                                    <span className="font-mono text-sm font-bold">${(Number(item.product.price) * item.quantity).toFixed(2)}</span>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>

                        {/* Footer */}
                        {items.length > 0 && (
                            <div className="p-6 border-t border-vanguard-slate/20 bg-vanguard-industrial space-y-4">
                                <div className="flex justify-between items-center">
                                    <span className="font-mono text-xs uppercase tracking-widest text-slate-400">Tactical Subtotal</span>
                                    <span className="font-mono text-xl font-bold text-white">${totalPrice().toFixed(2)}</span>
                                </div>
                                <p className="text-[10px] text-slate-500 text-center uppercase tracking-tighter">
                                    Logistics and mission-ready checks calculated at checkout.
                                </p>
                                <button
                                    onClick={goToCart}
                                    className="w-full py-4 bg-vanguard-red text-white font-mono font-bold uppercase tracking-[0.2em] text-sm flex items-center justify-center gap-3 group hover:bg-white hover:text-vanguard-red transition-all duration-300"
                                >
                                    Proceed to Checkout
                                    <ArrowRight size={18} className="group-hover:translate-x-2 transition-transform" />
                                </button>
                                <button
                                    onClick={goToCart}
                                    className="w-full text-center font-mono text-[10px] uppercase tracking-widest text-slate-500 hover:text-white transition-colors"
                                >
                                    View Full Kit
                                </button>
                            </div>
                        )}
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
};
