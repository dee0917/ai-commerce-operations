import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Minus, Plus, Trash2, ArrowRight, ArrowLeft, ShoppingBag, ShieldCheck, Truck } from 'lucide-react';
import { useCart } from '../hooks/useCart';
import { SafeImage } from '../components/SafeImage';

export const Cart: React.FC = () => {
    const { items, updateQuantity, removeItem, totalPrice, totalItems } = useCart();
    const navigate = useNavigate();

    if (items.length === 0) {
        return (
            <div className="bg-vanguard-obsidian min-h-screen">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-28">
                    <div className="border border-dashed border-vanguard-slate/25 bg-vanguard-industrial/30 py-24 flex flex-col items-center text-center">
                        <ShoppingBag size={56} className="text-slate-600 stroke-[1.25px] mb-6" />
                        <div className="font-mono text-vanguard-red text-[10px] font-bold tracking-[0.4em] uppercase mb-3">Empty Inventory</div>
                        <h1 className="text-3xl md:text-4xl font-black text-white uppercase tracking-tighter mb-4">Your Kit Is Unloaded</h1>
                        <p className="text-slate-400 text-sm max-w-sm mb-10">
                            Nothing staged for deployment yet. Browse the armoury and build out your everyday carry.
                        </p>
                        <Link to="/shop" className="btn-tactical inline-flex items-center gap-3">
                            Enter the Armoury <ArrowRight size={18} />
                        </Link>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-vanguard-obsidian min-h-screen">
            {/* Header band */}
            <div className="border-b border-vanguard-slate/20 bg-vanguard-industrial/40">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14 md:py-16">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="h-px w-10 bg-vanguard-red" />
                        <span className="font-mono text-vanguard-red text-[10px] font-bold tracking-[0.4em] uppercase">Staging Area</span>
                    </div>
                    <h1 className="text-4xl md:text-6xl font-black text-white uppercase tracking-tighter">Your Kit</h1>
                    <p className="text-slate-400 mt-4 font-mono text-[11px] uppercase tracking-widest">
                        {totalItems()} {totalItems() === 1 ? 'Item' : 'Items'} Staged for Deployment
                    </p>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16 grid grid-cols-1 lg:grid-cols-12 gap-12">
                {/* Line items */}
                <div className="lg:col-span-8">
                    <div className="border-t border-vanguard-slate/20">
                        {items.map((item) => (
                            <div key={item.id} className="flex gap-5 sm:gap-6 py-6 border-b border-vanguard-slate/20">
                                <Link
                                    to={`/product/${item.product.slug}`}
                                    className="h-28 w-28 sm:h-32 sm:w-32 shrink-0 bg-vanguard-industrial border border-vanguard-slate/20 overflow-hidden group"
                                >
                                    <SafeImage
                                        src={item.product.images[0]?.src}
                                        alt={item.product.name}
                                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                                    />
                                </Link>

                                <div className="flex-grow flex flex-col min-w-0">
                                    <div className="flex justify-between gap-4">
                                        <div className="min-w-0">
                                            <Link
                                                to={`/product/${item.product.slug}`}
                                                className="font-mono text-sm font-bold text-white uppercase tracking-tight hover:text-vanguard-red transition-colors line-clamp-2"
                                            >
                                                {item.product.name}
                                            </Link>
                                            <div className="font-mono text-[10px] text-slate-500 uppercase tracking-widest mt-1.5">
                                                SKU: {item.product.sku}
                                            </div>
                                        </div>
                                        <button
                                            onClick={() => removeItem(item.product.id)}
                                            className="text-slate-500 hover:text-vanguard-red transition-colors shrink-0 h-fit p-1"
                                            aria-label={`Remove ${item.product.name}`}
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>

                                    <div className="mt-auto pt-4 flex items-end justify-between gap-4">
                                        <div className="flex items-center border border-vanguard-slate/30 bg-black/20">
                                            <button
                                                onClick={() => updateQuantity(item.product.id, item.quantity - 1)}
                                                className="p-2.5 hover:bg-vanguard-red hover:text-white transition-colors"
                                                aria-label="Decrease quantity"
                                            >
                                                <Minus size={13} />
                                            </button>
                                            <span className="w-10 text-center font-mono text-sm tabular-nums">{item.quantity}</span>
                                            <button
                                                onClick={() => updateQuantity(item.product.id, item.quantity + 1)}
                                                className="p-2.5 hover:bg-vanguard-red hover:text-white transition-colors"
                                                aria-label="Increase quantity"
                                            >
                                                <Plus size={13} />
                                            </button>
                                        </div>
                                        <div className="text-right">
                                            <div className="font-mono text-base font-bold text-white tabular-nums">
                                                ${(Number(item.product.price) * item.quantity).toFixed(2)}
                                            </div>
                                            <div className="font-mono text-[10px] text-slate-500 tabular-nums">
                                                ${Number(item.product.price).toFixed(2)} each
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>

                    <Link
                        to="/shop"
                        className="inline-flex items-center gap-2 mt-8 text-slate-500 hover:text-vanguard-red transition-colors font-mono text-[10px] uppercase tracking-widest"
                    >
                        <ArrowLeft size={14} /> Continue Loadout
                    </Link>
                </div>

                {/* Summary */}
                <div className="lg:col-span-4">
                    <div className="lg:sticky lg:top-28 border border-vanguard-slate/20 bg-vanguard-industrial/50 p-7">
                        <h2 className="font-mono text-xs font-bold text-white uppercase tracking-[0.25em] mb-6 pb-4 border-b border-vanguard-slate/15">
                            Order Summary
                        </h2>
                        <dl className="space-y-4 font-mono text-sm">
                            <div className="flex justify-between text-slate-400">
                                <dt className="text-[11px] uppercase tracking-widest">Subtotal</dt>
                                <dd className="text-white tabular-nums">${totalPrice().toFixed(2)}</dd>
                            </div>
                            <div className="flex justify-between text-slate-400">
                                <dt className="text-[11px] uppercase tracking-widest">Logistics</dt>
                                <dd className="text-slate-300">Calculated at checkout</dd>
                            </div>
                        </dl>
                        <div className="flex justify-between items-baseline mt-6 pt-5 border-t border-vanguard-slate/15">
                            <span className="font-mono text-[11px] uppercase tracking-widest text-slate-400">Total</span>
                            <span className="font-mono text-2xl font-bold text-white tabular-nums">${totalPrice().toFixed(2)}</span>
                        </div>

                        <button
                            onClick={() => navigate('/checkout')}
                            className="w-full mt-7 py-4 bg-vanguard-red text-white font-mono font-bold uppercase tracking-[0.2em] text-xs flex items-center justify-center gap-3 group hover:bg-white hover:text-vanguard-red transition-all duration-300"
                        >
                            Proceed to Checkout
                            <ArrowRight size={16} className="group-hover:translate-x-1.5 transition-transform" />
                        </button>

                        <ul className="mt-7 space-y-3">
                            <li className="flex items-center gap-3 text-[10px] text-slate-500 uppercase tracking-widest font-mono">
                                <ShieldCheck size={14} className="text-slate-600" /> Encrypted secure checkout
                            </li>
                            <li className="flex items-center gap-3 text-[10px] text-slate-500 uppercase tracking-widest font-mono">
                                <Truck size={14} className="text-slate-600" /> Insured worldwide dispatch
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
};
