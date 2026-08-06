import React, { useEffect, useState, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Heart, Sparkles } from 'lucide-react';
import { fetchProduct, fetchProducts } from '../services/api';
import type { WooProduct } from '../types';
import { useCart } from '../hooks/useCart';
import { useWishlist } from '../hooks/useWishlist';
import ProductCard from '../components/ProductCard';
import clsx from 'clsx';

const ProductDetail: React.FC = () => {
    const { slug } = useParams();
    const [product, setProduct] = useState<WooProduct | null>(null);
    const [related, setRelated] = useState<WooProduct[]>([]);
    const [activeImage, setActiveImage] = useState(0);
    const [quantity, setQuantity] = useState(1);
    const [selectedOptions, setSelectedOptions] = useState<Record<string, string>>({});
    const { addToCart } = useCart();
    const { toggleWishlist, isInWishlist } = useWishlist();
    const ctaRef = useRef<HTMLButtonElement>(null);

    useEffect(() => {
        if (slug) {
            fetchProduct(slug).then(p => {
                setProduct(p);
                if (p?.related_ids?.length) {
                    fetchProducts().then(all =>
                        setRelated(all.filter(item => p.related_ids.includes(item.id)))
                    );
                }
            });
        }
    }, [slug]);

    if (!product) return <div className="pt-48 min-h-screen text-center font-display text-2xl animate-pulse">Summoning...</div>;

    const handleAddToCart = () => addToCart(product, quantity);

    return (
        <div className="pt-48 pb-32">
            <div className="max-w-[1400px] mx-auto px-8 grid grid-cols-1 lg:grid-cols-2 gap-16 lg:gap-32 fade-up items-start">
                {/* Gallery - Sticky on Desktop */}
                <div className="space-y-6 lg:sticky lg:top-32">
                    <div className="aspect-[3/4] bg-brand-secondary/5 relative border border-stone-400 p-2 overflow-hidden">
                        <div className="absolute inset-2 bg-brand-primary overflow-hidden">
                            <img
                                src={product.images[activeImage]?.src}
                                alt={product.images[activeImage]?.alt}
                                className="w-full h-full object-cover transition-transform duration-700 hover:scale-105"
                            />
                        </div>
                    </div>
                    <div className="grid grid-cols-5 gap-4">
                        {product.images.map((img, i) => (
                            <button
                                key={img.id}
                                onClick={() => setActiveImage(i)}
                                className={clsx(
                                    "aspect-square border transition-all relative overflow-hidden",
                                    activeImage === i ? "border-brand-secondary p-[1px]" : "border-stone-400/30 p-1 opacity-50 hover:opacity-100"
                                )}
                            >
                                <img src={img.src} alt={img.alt} className="w-full h-full object-cover" />
                            </button>
                        ))}
                    </div>
                </div>

                {/* Info Container */}
                <div className="space-y-16">
                    <div className="space-y-8">
                        <nav className="text-[10px] uppercase tracking-[0.5em] font-bold text-brand-accent flex items-center gap-3">
                            <Link to="/" className="hover:opacity-60 transition-opacity">Sanctuary</Link>
                            <span className="opacity-20">/</span>
                            <Link to="/shop" className="hover:opacity-60 transition-opacity">Collection</Link>
                        </nav>

                        <h1 className="text-6xl lg:text-7xl font-display leading-[0.9] tracking-tight font-light uppercase">{product.name}</h1>

                        <div className="flex items-center gap-6">
                            <span className="text-3xl font-light tracking-widest">
                                ${product.price}
                            </span>
                        </div>
                    </div>

                    <div className="w-24 border-t border-brand-accent"></div>

                    {/* Metadata Grid */}
                    <div className="grid grid-cols-2 gap-12 py-4 border-t border-b border-stone-400/20">
                        <div className="space-y-3">
                            <h4 className="uppercase tracking-widest text-[10px] font-bold opacity-40">Frequency</h4>
                            <p className="font-display text-xl uppercase tracking-widest leading-none">High Vibration</p>
                        </div>
                        <div className="space-y-3">
                            <h4 className="uppercase tracking-widest text-[10px] font-bold opacity-40">Status</h4>
                            <p className="font-display text-xl uppercase tracking-widest leading-none text-brand-accent flex items-center gap-2">
                                <Sparkles className="w-4 h-4 fill-brand-accent stroke-none" /> Purified
                            </p>
                        </div>
                    </div>

                    <div
                        className="prose prose-stone font-light text-lg leading-[1.8] opacity-80"
                        dangerouslySetInnerHTML={{ __html: product.description }}
                    />

                    {/* Technical Specs Accordion-style */}
                    <div className="space-y-12">
                        {product.attributes.map(attr => (
                            <div key={attr.id} className="space-y-6">
                                <h3 className="uppercase tracking-[0.3em] text-[10px] font-bold opacity-40">{attr.name} Selection</h3>
                                <div className="flex flex-wrap gap-4">
                                    {attr.options.map(opt => (
                                        <button
                                            key={opt}
                                            onClick={() => setSelectedOptions(s => ({ ...s, [attr.name]: opt }))}
                                            className={clsx(
                                                "px-8 py-3 border text-[10px] uppercase font-bold tracking-[0.2em] transition-all",
                                                selectedOptions[attr.name] === opt
                                                    ? "border-brand-secondary bg-brand-secondary text-brand-primary shadow-xl scale-105"
                                                    : "border-stone-400/50 hover:border-brand-secondary"
                                            )}
                                        >
                                            {opt}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Final Action Block */}
                    <div className="space-y-10 pt-10 border-t border-stone-200">
                        <div className="flex items-center gap-8">
                            <div className="flex items-center border border-stone-300 h-16">
                                <button className="px-6 h-full hover:bg-stone-50 transition-colors" onClick={() => setQuantity(q => Math.max(1, q - 1))}>—</button>
                                <span className="w-16 text-center font-display text-2xl">{quantity}</span>
                                <button className="px-6 h-full hover:bg-stone-50 transition-colors" onClick={() => setQuantity(q => q + 1)}>+</button>
                            </div>

                            <button
                                ref={ctaRef}
                                onClick={handleAddToCart}
                                disabled={!product.purchasable || product.stock_status === 'outofstock'}
                                className="flex-1 bg-brand-secondary text-brand-primary h-16 uppercase tracking-[0.4em] font-bold text-xs hover:bg-brand-accent transition-all duration-500 shadow-2xl disabled:opacity-50 disabled:bg-gray-400 disabled:cursor-not-allowed group"
                            >
                                <span className="group-hover:scale-110 transition-transform inline-block">
                                    {product.stock_status === 'outofstock' ? 'Out of Sanctuary' : 'Anchor to Bag'}
                                </span>
                            </button>
                        </div>

                        <button
                            onClick={() => toggleWishlist(product.id)}
                            className="w-full h-14 flex items-center justify-center gap-4 uppercase tracking-[0.3em] text-[10px] font-bold border border-stone-200 hover:border-brand-secondary transition-colors"
                        >
                            <Heart className={clsx("w-4 h-4 transition-colors", isInWishlist(product.id) && "fill-brand-accent text-brand-accent")} />
                            {isInWishlist(product.id) ? 'Hearted' : 'Add to Wishlist'}
                        </button>
                    </div>
                </div>
            </div>

            {/* Enrichment: The Ritual Detail */}
            <section className="bg-brand-secondary text-brand-primary mt-32 py-32 px-8 overflow-hidden relative">
                <div className="max-w-[1400px] mx-auto grid grid-cols-1 lg:grid-cols-2 gap-32 items-center relative z-10">
                    <div className="space-y-12 fade-up">
                        <span className="text-[10px] uppercase tracking-[0.5em] font-bold text-brand-accent block">Craftsmanship</span>
                        <h2 className="text-5xl lg:text-7xl font-display uppercase tracking-widest font-light leading-none">The <span className="italic font-serif">7-Day</span> <br />Cleaning Ritual</h2>
                        <p className="font-light text-xl leading-relaxed opacity-60">
                            Creation is only the physical birth. To ensure your {product.name} carries only pure energy, it undergoes a 168-hour sound-bath treatment in our private sanctuary. No object leaves our monastery without being grounded in silence.
                        </p>
                        <div className="flex gap-12 pt-8">
                            <div className="space-y-2">
                                <span className="text-4xl font-display block">168h</span>
                                <span className="text-[10px] uppercase tracking-widest opacity-40 font-bold">Resonance Bath</span>
                            </div>
                            <div className="space-y-2">
                                <span className="text-4xl font-display block">0.0v</span>
                                <span className="text-[10px] uppercase tracking-widest opacity-40 font-bold">Static Discharge</span>
                            </div>
                        </div>
                    </div>
                    <div className="aspect-square border border-brand-primary/20 p-4 fade-up">
                        <img src="/products/energy-ritual.jpg" className="w-full h-full object-cover" />
                    </div>
                </div>
                <div className="absolute top-0 right-0 text-[20rem] font-display font-light opacity-[0.03] pointer-events-none select-none uppercase tracking-tighter leading-none translate-x-1/2 -translate-y-1/2">Energy</div>
            </section>

            {related.length > 0 && (
                <section className="mt-48 max-w-[1400px] mx-auto px-8 fade-up">
                    <div className="flex justify-between items-end mb-16 border-b border-stone-300 pb-8">
                        <div>
                            <span className="text-[10px] uppercase tracking-[0.5em] font-bold text-brand-accent block mb-4">Harmony</span>
                            <h2 className="text-4xl font-display uppercase tracking-widest font-light">Compatible Energies</h2>
                        </div>
                        <Link to="/shop" className="uppercase tracking-[0.3em] text-[10px] font-bold border-b border-brand-secondary pb-1">All Objects</Link>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                        {related.map(p => <ProductCard key={p.id} product={p} />)}
                    </div>
                </section>
            )}
        </div>
    );
};

export default ProductDetail;
