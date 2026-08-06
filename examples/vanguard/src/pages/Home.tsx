import React, { useEffect, useState } from 'react';
import { Hero } from '../components/Hero';
import { BentoGrid } from '../components/BentoGrid';
import { fetchProducts } from '../services/api';
import type { WooProduct } from '../types';
import { Target, Shield, Zap, Package } from 'lucide-react';

export const Home: React.FC = () => {
    const [products, setProducts] = useState<WooProduct[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const load = async () => {
            const data = await fetchProducts({ per_page: 8 });
            setProducts(data);
            setLoading(false);
        };
        load();
    }, []);

    return (
        <div className="flex flex-col">
            <Hero />

            {/* Trust Badges - Gear Highlight */}
            <section className="bg-vanguard-obsidian py-20 border-b border-vanguard-slate/20">
                <div className="max-w-7xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-8">
                    {[
                        { icon: <Shield size={24} />, label: "Field Tested", desc: "Proven in the harshest environments." },
                        { icon: <Zap size={24} />, label: "Tactical Response", desc: "Built for split-second deployment." },
                        { icon: <Target size={24} />, label: "Sub-Micron Precision", desc: "Surgical-grade craftsmanship." },
                        { icon: <Package size={24} />, label: "Secure Logistics", desc: "Dispatched under heavy encryption." }
                    ].map((item, i) => (
                        <div key={i} className="flex flex-col items-center text-center group">
                            <div className="mb-4 text-vanguard-red group-hover:scale-110 transition-transform">
                                {item.icon}
                            </div>
                            <h3 className="font-mono text-xs font-bold uppercase tracking-widest mb-2 text-white">{item.label}</h3>
                            <p className="text-[10px] text-slate-500 uppercase leading-relaxed max-w-[150px]">{item.desc}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* Featured Collection */}
            <section className="py-24 bg-vanguard-gray-900">
                <div className="max-w-7xl mx-auto px-4 mb-16 flex justify-between items-end">
                    <div>
                        <h2 className="text-4xl font-black text-white mb-2">THE OBSIDIAN COLLECTION</h2>
                        <div className="font-mono text-xs text-vanguard-red tracking-widest uppercase">Mission-Critical Essentials</div>
                    </div>
                    <button className="hidden sm:block font-mono text-xs uppercase tracking-widest text-slate-400 hover:text-white transition-colors pb-1 border-b border-vanguard-slate/30">
                        Access All Files
                    </button>
                </div>

                {loading ? (
                    <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-4 gap-6">
                        {[...Array(8)].map((_, i) => (
                            <div key={i} className="aspect-square skeleton rounded-lg" />
                        ))}
                    </div>
                ) : (
                    <BentoGrid products={products} />
                )}
            </section>

            {/* Review Strip - PRD Sports & Active skeleton */}
            <section className="bg-vanguard-industrial py-20 overflow-hidden relative border-t border-vanguard-slate/20">
                <div className="absolute top-0 right-0 p-8 font-mono text-[150px] font-black text-white/5 pointer-events-none select-none">VANGUARD</div>
                <div className="max-w-7xl mx-auto px-4">
                    <h2 className="font-mono text-sm tracking-[0.5em] text-vanguard-red mb-12 text-center uppercase">Verified Operatives</h2>
                    <div className="grid md:grid-cols-3 gap-12">
                        {[
                            { author: "E. SULLIVAN", role: "Search & Rescue", text: "The Stinger Bolt Action Pen has become an inseparable part of my EDC. It's not just a writing tool; it's a solid piece of survival gear." },
                            { author: "K. NAKAMURA", role: "Network Architect", text: "Cipher wallet is the peak of minimalist design. Replaced my bulky leather brick and haven't looked back. RFID protection is a must." },
                            { author: "M. VANCE", role: "Field Operative", text: "Axis organizer solved my noise discipline issues. No more jingling keys. The modularity is brilliant for mission-specific setups." }
                        ].map((review, i) => (
                            <div key={i} className="bg-black/20 p-8 border border-vanguard-slate/10 relative">
                                <div className="text-vanguard-red mb-4">★★★★★</div>
                                <p className="text-sm italic text-slate-300 mb-6 font-serif">"{review.text}"</p>
                                <div>
                                    <div className="font-mono text-xs font-bold text-white uppercase">{review.author}</div>
                                    <div className="font-mono text-[9px] text-slate-500 uppercase">{review.role}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Newsletter */}
            <section className="py-24 bg-vanguard-obsidian border-t border-white/5">
                <div className="max-w-3xl mx-auto px-4 text-center">
                    <h2 className="text-3xl font-black text-white mb-6 uppercase tracking-tighter">Request Intel Updates</h2>
                    <p className="text-slate-400 mb-10 text-sm">Join the Vanguard list for priority access to new hardware drops and tactical insights.</p>
                    <div className="flex border border-vanguard-slate/30 p-1 bg-vanguard-industrial">
                        <input
                            type="email"
                            placeholder="ENTER COMM CHANNEL EMAIL"
                            className="flex-grow bg-transparent px-4 py-3 font-mono text-sm uppercase focus:outline-none text-white"
                        />
                        <button className="bg-vanguard-red text-white py-3 px-8 font-mono font-bold uppercase hover:bg-white hover:text-vanguard-red transition-all">
                            Initialize
                        </button>
                    </div>
                </div>
            </section>
        </div>
    );
};
