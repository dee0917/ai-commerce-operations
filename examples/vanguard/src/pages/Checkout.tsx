import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Lock, CheckCircle2, ArrowRight } from 'lucide-react';
import { useCart } from '../hooks/useCart';
import { submitCheckout } from '../services/api';
import { SafeImage } from '../components/SafeImage';
import { toast } from 'react-hot-toast';

const fields = [
    { name: 'first_name', label: 'First Name', placeholder: 'Kenji', half: true },
    { name: 'last_name', label: 'Last Name', placeholder: 'Nakamura', half: true },
    { name: 'email', label: 'Comm Channel (Email)', placeholder: 'operator@signal.io', half: false, type: 'email' },
    { name: 'address_1', label: 'Drop Address', placeholder: '14 Keong Saik Road', half: false },
    { name: 'city', label: 'City', placeholder: 'Singapore', half: true },
    { name: 'postcode', label: 'Postal Code', placeholder: '089117', half: true },
] as const;

export const Checkout: React.FC = () => {
    const { items, totalPrice, totalItems, clearCart } = useCart();
    const [submitting, setSubmitting] = useState(false);
    const [done, setDone] = useState(false);
    const [orderNumber, setOrderNumber] = useState('');

    if (done) {
        return (
            <div className="bg-vanguard-obsidian min-h-screen flex items-center justify-center px-4 py-28">
                <div className="max-w-md w-full text-center border border-vanguard-slate/20 bg-vanguard-industrial/40 p-12">
                    <CheckCircle2 size={56} className="text-vanguard-red mx-auto mb-6" />
                    <div className="font-mono text-vanguard-red text-[10px] font-bold tracking-[0.4em] uppercase mb-3">Order Confirmed</div>
                    <h1 className="text-3xl font-black text-white uppercase tracking-tighter mb-4">Kit Deployed</h1>
                    {orderNumber && (
                        <div className="font-mono text-xs text-white tracking-widest mb-6" data-testid="order-number">
                            ORDER #{orderNumber}
                        </div>
                    )}
                    <p className="text-slate-400 text-sm mb-10">
                        Your order is logged. A tracking ID lands in your comm channel once the kit leaves the depot.
                    </p>
                    <Link to="/shop" className="btn-tactical inline-flex items-center gap-3">
                        Back to the Armoury <ArrowRight size={18} />
                    </Link>
                </div>
            </div>
        );
    }

    if (items.length === 0) {
        return (
            <div className="bg-vanguard-obsidian min-h-screen flex items-center justify-center px-4 py-28">
                <div className="text-center">
                    <h1 className="text-3xl font-black text-white uppercase tracking-tighter mb-4">Nothing to Check Out</h1>
                    <p className="text-slate-400 text-sm mb-8">Your kit is empty. Load up before deployment.</p>
                    <Link to="/shop" className="btn-tactical inline-flex items-center gap-3">Enter the Armoury <ArrowRight size={18} /></Link>
                </div>
            </div>
        );
    }

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setSubmitting(true);

        const data = new FormData(e.currentTarget);
        const value = (name: string) => String(data.get(name) ?? '').trim();

        const address = {
            first_name: value('first_name'),
            last_name: value('last_name'),
            address_1: value('address_1'),
            city: value('city'),
            postcode: value('postcode'),
            country: 'SG',
            email: value('email'),
            phone: value('phone'),
        };

        try {
            const result = await submitCheckout(
                { billing_address: address, shipping_address: address, payment_method: '' },
                items
            );
            if (result?.order_number) setOrderNumber(String(result.order_number));
            clearCart();
            setDone(true);
            window.scrollTo(0, 0);
        } catch (err) {
            toast.error(err instanceof Error ? err.message : 'Checkout failed. Try again.', {
                style: { background: '#121212', color: '#fff', border: '1px solid #FF3D00', fontFamily: 'IBM Plex Mono' },
            });
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="bg-vanguard-obsidian min-h-screen">
            <div className="border-b border-vanguard-slate/20 bg-vanguard-industrial/40">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14 md:py-16">
                    <Link to="/cart" className="inline-flex items-center gap-2 text-slate-500 hover:text-vanguard-red transition-colors font-mono text-[10px] uppercase tracking-widest mb-6">
                        <ArrowLeft size={14} /> Back to Kit
                    </Link>
                    <h1 className="text-4xl md:text-6xl font-black text-white uppercase tracking-tighter">Checkout</h1>
                </div>
            </div>

            <form onSubmit={handleSubmit} className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16 grid grid-cols-1 lg:grid-cols-12 gap-12">
                {/* Form */}
                <div className="lg:col-span-7">
                    <h2 className="font-mono text-xs font-bold text-white uppercase tracking-[0.25em] mb-8 pb-4 border-b border-vanguard-slate/15">
                        Dispatch Details
                    </h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                        {fields.map((f) => (
                            <div key={f.name} className={f.half ? 'sm:col-span-1' : 'sm:col-span-2'}>
                                <label htmlFor={f.name} className="block font-mono text-[10px] uppercase tracking-widest text-slate-400 mb-2">
                                    {f.label}
                                </label>
                                <input
                                    id={f.name}
                                    name={f.name}
                                    type={'type' in f ? f.type : 'text'}
                                    required
                                    placeholder={f.placeholder}
                                    className="w-full bg-vanguard-industrial/60 border border-vanguard-slate/30 px-4 py-3 text-sm text-white placeholder:text-slate-600 focus:outline-none focus:border-vanguard-red focus:ring-1 focus:ring-vanguard-red/40 transition-colors"
                                />
                            </div>
                        ))}
                    </div>

                    <div className="mt-8 p-5 border border-vanguard-slate/20 bg-vanguard-industrial/30 flex items-center gap-3">
                        <Lock size={16} className="text-vanguard-red shrink-0" />
                        <p className="text-[11px] text-slate-400 leading-relaxed">
                            Payment is processed on an encrypted channel. We never store card data on our servers.
                        </p>
                    </div>
                </div>

                {/* Summary */}
                <div className="lg:col-span-5">
                    <div className="lg:sticky lg:top-28 border border-vanguard-slate/20 bg-vanguard-industrial/50 p-7">
                        <h2 className="font-mono text-xs font-bold text-white uppercase tracking-[0.25em] mb-6 pb-4 border-b border-vanguard-slate/15">
                            Order Review ({totalItems()})
                        </h2>

                        <ul className="space-y-4 max-h-72 overflow-y-auto no-scrollbar pr-1">
                            {items.map((item) => (
                                <li key={item.id} className="flex gap-4 items-center">
                                    <div className="h-14 w-14 shrink-0 bg-vanguard-obsidian border border-vanguard-slate/20 overflow-hidden relative">
                                        <SafeImage src={item.product.images[0]?.src} alt={item.product.name} className="w-full h-full object-cover" />
                                        <span className="absolute -top-1.5 -right-1.5 bg-vanguard-red text-white text-[9px] font-mono font-bold h-4 min-w-4 px-1 rounded-full flex items-center justify-center tabular-nums">
                                            {item.quantity}
                                        </span>
                                    </div>
                                    <div className="flex-grow min-w-0">
                                        <div className="font-mono text-[11px] font-bold text-white uppercase tracking-tight line-clamp-1">{item.product.name}</div>
                                        <div className="font-mono text-[10px] text-slate-500">${Number(item.product.price).toFixed(2)} each</div>
                                    </div>
                                    <div className="font-mono text-xs font-bold text-white tabular-nums">
                                        ${(Number(item.product.price) * item.quantity).toFixed(2)}
                                    </div>
                                </li>
                            ))}
                        </ul>

                        <dl className="mt-6 pt-5 border-t border-vanguard-slate/15 space-y-3 font-mono">
                            <div className="flex justify-between text-slate-400 text-sm">
                                <dt className="text-[11px] uppercase tracking-widest">Subtotal</dt>
                                <dd className="text-white tabular-nums">${totalPrice().toFixed(2)}</dd>
                            </div>
                            <div className="flex justify-between text-slate-400 text-sm">
                                <dt className="text-[11px] uppercase tracking-widest">Logistics</dt>
                                <dd className="text-slate-300">Free</dd>
                            </div>
                            <div className="flex justify-between items-baseline pt-3 border-t border-vanguard-slate/15">
                                <span className="text-[11px] uppercase tracking-widest text-slate-400">Total</span>
                                <span className="text-2xl font-bold text-white tabular-nums">${totalPrice().toFixed(2)}</span>
                            </div>
                        </dl>

                        <button
                            type="submit"
                            disabled={submitting}
                            className="w-full mt-7 py-4 bg-vanguard-red text-white font-mono font-bold uppercase tracking-[0.2em] text-xs flex items-center justify-center gap-3 hover:bg-white hover:text-vanguard-red transition-all duration-300 disabled:opacity-50 disabled:cursor-wait"
                        >
                            {submitting ? 'Processing...' : 'Confirm Order'}
                            {!submitting && <Lock size={14} />}
                        </button>
                    </div>
                </div>
            </form>
        </div>
    );
};
