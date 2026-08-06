import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Sparkles, Hand } from 'lucide-react';
import { fetchProducts } from '../services/api';
import type { WooProduct } from '../types';
import ProductCard from '../components/ProductCard';

const Home: React.FC = () => {
    const [products, setProducts] = useState<WooProduct[]>([]);

    useEffect(() => {
        fetchProducts({ per_page: 8 }).then(setProducts);
    }, []);

    return (
        <div className="pt-24 space-y-32 pb-32 overflow-hidden">
            {/* Hero Section - Split-ImageLeft */}
            <section className="max-w-[1400px] mx-auto px-8">
                <div className="grid grid-cols-1 lg:grid-cols-2 min-h-[85vh] border-[0.5px] border-stone-400">
                    <div className="relative border-r-[0.5px] border-stone-400 h-[60vh] lg:h-auto overflow-hidden">
                        <img
                            src="/hero.png"
                            alt="AuraGuard Altar"
                            className="absolute inset-0 w-full h-full object-cover scale-105 hover:scale-100 transition-transform duration-[3s] ease-out"
                            loading="eager"
                        />
                        <div className="absolute inset-0 bg-brand-secondary/5 mix-blend-multiply opacity-30"></div>
                    </div>
                    <div className="flex flex-col justify-center px-12 lg:px-24 py-24 bg-[#EAE3DB] relative overflow-hidden">
                        {/* Decorative Element */}
                        <div className="absolute -right-20 -top-20 w-64 h-64 border border-brand-secondary/5 rounded-full rotate-45 pointer-events-none"></div>

                        <div className="relative z-10">
                            <span className="uppercase tracking-[0.5em] text-[10px] font-bold mb-8 flex items-center gap-4 text-brand-accent">
                                <span className="w-12 h-[1px] bg-brand-accent"></span> EST. 1928 HERITAGE
                            </span>
                            <h1 className="text-6xl lg:text-8xl font-display leading-[1] mb-10 font-light tracking-tight">
                                Protect Your <br /><span className="italic font-serif">Original</span> Energy
                            </h1>
                            <p className="font-light text-xl mb-14 max-w-sm tracking-wide leading-loose opacity-80 border-l border-brand-accent pl-8 py-2">
                                For centuries, the masters have understood the flow. Discover authentic, hand-crafted objects designed to anchor your spirit.
                            </p>
                            <Link
                                to="/shop"
                                className="group inline-flex items-center gap-6 uppercase tracking-[0.3em] font-medium border-stone-400 pb-2 self-start transition-all hover:gap-10"
                            >
                                <span className="border-b border-brand-secondary group-hover:border-brand-accent group-hover:text-brand-accent transition-colors">Start Your Guard</span>
                                <span className="text-xl">→</span>
                            </Link>
                        </div>
                    </div>
                </div>
            </section>

            {/* Marquee Social Proof */}
            <div className="bg-brand-secondary py-6 -rotate-1 relative z-20 overflow-hidden select-none">
                <div className="flex whitespace-nowrap animate-marquee">
                    {[...Array(6)].map((_, i) => (
                        <div key={i} className="flex gap-20 items-center px-10 text-brand-primary/40 font-display text-2xl uppercase tracking-[0.4em]">
                            <span>Authentic Heritage</span>
                            <Sparkles className="w-6 h-6 text-brand-accent fill-brand-accent" />
                            <span>Spiritually Blessed</span>
                            <ShieldCheck className="w-6 h-6 text-brand-accent" />
                            <span>Hand Crafted</span>
                            <Hand className="w-6 h-6 text-brand-accent" />
                        </div>
                    ))}
                </div>
            </div>

            <style>{`
                @keyframes marquee {
                    0% { transform: translateX(0); }
                    100% { transform: translateX(-50%); }
                }
                .animate-marquee {
                    animation: marquee 30s linear infinite;
                }
            `}</style>

            {/* Featured Products */}
            <section className="max-w-[1400px] mx-auto px-8 relative">
                <div className="absolute -left-32 top-1/4 opacity-5 pointer-events-none rotate-90 hidden xl:block">
                    <span className="text-[12rem] font-display uppercase tracking-[0.2em] whitespace-nowrap">AUTHENTICITY</span>
                </div>

                <div className="flex flex-col md:flex-row justify-between items-baseline mb-20 fade-up border-b-[0.5px] border-stone-400 pb-6">
                    <h2 className="text-5xl font-display uppercase tracking-widest font-light">The Sacred Collection</h2>
                    <p className="hidden md:block font-light opacity-50 uppercase tracking-widest text-xs">Curated for the modern seeker</p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-16">
                    {products.map(product => (
                        <ProductCard key={product.id} product={product} />
                    ))}
                </div>
                <div className="mt-20 text-center">
                    <Link to="/shop" className="inline-block px-12 py-4 border border-brand-secondary uppercase tracking-[0.3em] text-xs hover:bg-brand-secondary hover:text-brand-primary transition-all duration-500">
                        Enter The Full Archive
                    </Link>
                </div>
            </section>

            {/* Immersive Section - Values */}
            <section className="bg-brand-secondary text-brand-primary py-32 relative overflow-hidden">
                <div className="absolute inset-0 opacity-10 pointer-events-none">
                    <img src="/products/hero-bg.jpg" className="w-full h-full object-cover mix-blend-overlay" />
                </div>

                <div className="max-w-[1400px] mx-auto px-8 grid grid-cols-1 md:grid-cols-3 gap-24 relative z-10 text-center divide-y md:divide-y-0 md:divide-x divide-stone-800">
                    {[
                        { icon: Hand, title: "Artisan Built", desc: "Each talisman is hand-carved in our heritage workshops using techniques passed down for three generations." },
                        { icon: Sparkles, title: "Ritual Purity", desc: "Before leaving our care, every piece undergoes a ritual purification by our resident practitioners." },
                        { icon: ShieldCheck, title: "Inner Shield", desc: "Beyond aesthetic, our objects serve as energetic anchors, protecting your equilibrium in a chaotic world." }
                    ].map((item, idx) => (
                        <div key={idx} className="flex flex-col items-center gap-8 fade-up group pt-16 md:pt-0">
                            <div className="w-20 h-20 border border-stone-800 rounded-full flex items-center justify-center group-hover:border-brand-accent transition-colors duration-700">
                                <item.icon className="w-8 h-8 text-brand-accent stroke-[1.2]" />
                            </div>
                            <div className="space-y-4">
                                <h3 className="uppercase tracking-[0.4em] font-medium text-lg">{item.title}</h3>
                                <p className="font-light text-sm opacity-60 px-12 leading-relaxed">{item.desc}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            {/* Founder Note - Overlapping Grid */}
            <section className="max-w-[1400px] mx-auto px-8">
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-0 items-center">
                    <div className="lg:col-span-7 relative aspect-[16/9] lg:aspect-auto lg:h-[700px] border-[0.5px] border-stone-400 p-6 fade-up">
                        <img
                            src="/products/founder-artisan.jpg"
                            alt="The Artisan at Work"
                            className="w-full h-full object-cover"
                            loading="lazy"
                        />
                        <div className="absolute bottom-12 -right-12 bg-brand-primary p-12 border border-stone-400 hidden lg:block max-w-sm">
                            <p className="font-serif italic text-2xl opacity-90 leading-relaxed">
                                "Our mission is to bridge the gap between ancient protection and modern aesthetics."
                            </p>
                            <p className="mt-8 uppercase tracking-widest text-[10px] font-bold">Master Lin, Lead Artisan</p>
                        </div>
                    </div>
                    <div className="lg:col-span-5 lg:pl-24 py-20 fade-up space-y-10">
                        <div className="space-y-4">
                            <span className="text-[10px] uppercase tracking-[0.5em] font-bold text-brand-accent">Beyond The Object</span>
                            <h2 className="text-5xl font-display font-light uppercase tracking-widest leading-[1.1]">The Philosophy of Aura</h2>
                        </div>
                        <div className="w-32 border-t border-brand-secondary"></div>
                        <div className="space-y-6 font-light leading-loose text-lg opacity-80 max-w-lg">
                            <p>
                                Protection is not about building walls, but about cultivating an inner clarity that no external pressure can distort. Our talismans are designed as focal points for this clarity.
                            </p>
                            <p>
                                We use only natural materials—cinnabar, obsidian, jade, and sandalwood—honoring the raw energies of the earth as the foundation of our craft.
                            </p>
                        </div>
                        <div className="pt-8">
                            <Link to="/about" className="group inline-flex items-center gap-4 uppercase tracking-[0.3em] text-xs font-bold hover:text-brand-accent transition-colors">
                                <span>The Full Heritage</span>
                                <span className="group-hover:translate-x-2 transition-transform">→</span>
                            </Link>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Home;
