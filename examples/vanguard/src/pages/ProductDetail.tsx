import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchProduct, fetchProducts } from '../services/api';
import type { WooProduct } from '../types';
import { useCart } from '../hooks/useCart';
import { ProductCard } from '../components/ProductCard';
import { Shield, Target, Zap, ArrowLeft, Minus, Plus, ShoppingBag } from 'lucide-react';
import { clsx } from 'clsx';
import { toast } from 'react-hot-toast';
import { SafeImage } from '../components/SafeImage';

export const ProductDetail: React.FC = () => {
    const { slug } = useParams<{ slug: string }>();
    const [product, setProduct] = useState<WooProduct | null>(null);
    const [related, setRelated] = useState<WooProduct[]>([]);
    const [loading, setLoading] = useState(true);
    const [quantity, setQuantity] = useState(1);
    const [activeImage, setActiveImage] = useState(0);

    const addItem = useCart(state => state.addItem);

    useEffect(() => {
        const load = async () => {
            if (!slug) return;
            setLoading(true);
            const data = await fetchProduct(slug);
            if (data) {
                setProduct(data);
                const relatedData = await fetchProducts({ per_page: 4 });
                setRelated(relatedData.filter(p => p.id !== data.id).slice(0, 4));
            }
            setLoading(false);
            window.scrollTo(0, 0);
        };
        load();
    }, [slug]);

    const handleAddToCart = () => {
        if (product) {
            addItem(product, quantity);
            toast.success(`Kit Updated: ${product.name}`, {
                style: { background: '#121212', color: '#fff', border: '1px solid #FF3D00', fontFamily: 'IBM Plex Mono' }
            });
        }
    };

    if (loading) return (
        <div className="min-h-screen bg-vanguard-obsidian flex items-center justify-center">
            <div className="font-mono text-vanguard-red animate-pulse">DECRYPTING DATA...</div>
        </div>
    );

    if (!product) return (
        <div className="min-h-screen bg-vanguard-obsidian flex flex-col items-center justify-center p-4">
            <h1 className="font-mono text-2xl text-white mb-4">ACCESS DENIED: PRODUCT NOT FOUND</h1>
            <Link to="/shop" className="btn-tactical">Return to Armoury</Link>
        </div>
    );

    return (
        <div className="bg-vanguard-obsidian min-h-screen pb-20">
            <div className="max-w-7xl mx-auto px-4 py-8">
                <Link to="/shop" className="inline-flex items-center gap-2 text-slate-500 hover:text-vanguard-red transition-colors font-mono text-[10px] uppercase tracking-widest mb-12">
                    <ArrowLeft size={14} /> Back to Armoury
                </Link>

                <div className="grid lg:grid-cols-2 gap-16">
                    {/* Gallery */}
                    <div className="space-y-6">
                        <div className="aspect-square bg-vanguard-industrial border border-vanguard-slate/20 rounded-lg overflow-hidden relative group">
                            <SafeImage
                                src={product.images[activeImage]?.src}
                                alt={product.name}
                                className="w-full h-full object-cover grayscale-[10%] group-hover:grayscale-0 transition-all duration-700"
                            />
                            <div className="absolute top-6 right-6 font-mono text-[10px] bg-black/40 backdrop-blur-md px-3 py-1 border border-white/10">
                                REF_NO: {product.sku}
                            </div>
                        </div>

                        <div className={clsx("grid grid-cols-4 gap-4", product.images.length < 2 && "hidden")}>
                            {product.images.map((img, i) => (
                                <button
                                    key={img.id}
                                    onClick={() => setActiveImage(i)}
                                    className={clsx(
                                        "aspect-square rounded border transition-all overflow-hidden",
                                        activeImage === i ? "border-vanguard-red scale-105" : "border-vanguard-slate/20 opacity-50 hover:opacity-100"
                                    )}
                                >
                                    <SafeImage src={img.src} alt="Detail" className="w-full h-full object-cover" />
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Details */}
                    <div className="flex flex-col">
                        <div className="flex items-center gap-3 mb-6">
                            <span className="bg-vanguard-red/10 text-vanguard-red font-mono text-[9px] font-bold px-2 py-0.5 border border-vanguard-red/20 uppercase tracking-widest">
                                {product.categories[0]?.name}
                            </span>
                            {product.stock_status === 'instock' ? (
                                <span className="text-green-500 font-mono text-[9px] uppercase tracking-widest flex items-center gap-1">
                                    <Zap size={10} /> Operational
                                </span>
                            ) : (
                                <span className="text-slate-500 font-mono text-[9px] uppercase tracking-widest flex items-center gap-1">
                                    <Target size={10} /> Depleted
                                </span>
                            )}
                        </div>

                        <h1 className="text-4xl md:text-5xl lg:text-6xl font-black text-white mb-6 uppercase tracking-tighter leading-tight">
                            {product.name}
                        </h1>

                        <div className="flex items-baseline gap-4 mb-8">
                            <span className="text-4xl font-mono font-bold text-white">${product.price}</span>
                            <span className="font-mono text-[10px] text-slate-500 uppercase">US Credits</span>
                        </div>

                        <p className="text-slate-400 leading-relaxed mb-10 text-sm md:text-base border-l-2 border-vanguard-slate/20 pl-6">
                            {product.description}
                        </p>

                        {/* Inventory Controls */}
                        <div className="space-y-8 mt-auto">
                            {product.stock_status === 'instock' ? (
                                <div className="flex flex-col sm:flex-row gap-6">
                                    <div className="flex items-center border border-vanguard-slate/30 bg-vanguard-industrial/50">
                                        <button onClick={() => setQuantity(q => Math.max(1, q - 1))} className="p-4 hover:text-vanguard-red"><Minus size={18} /></button>
                                        <span className="w-12 text-center font-mono text-lg font-bold">{quantity}</span>
                                        <button onClick={() => setQuantity(q => q + 1)} className="p-4 hover:text-vanguard-red"><Plus size={18} /></button>
                                    </div>
                                    <button
                                        onClick={handleAddToCart}
                                        className="btn-tactical flex-grow flex items-center justify-center gap-3"
                                    >
                                        Deploy to Kit
                                        <ShoppingBag size={20} />
                                    </button>
                                </div>
                            ) : (
                                <button disabled className="w-full py-5 bg-vanguard-slate/20 text-slate-500 font-mono font-bold uppercase tracking-widest cursor-not-allowed">
                                    Material Unavailable
                                </button>
                            )}

                            {/* Specs Grid */}
                            <div className="grid grid-cols-3 gap-6 pt-10 border-t border-vanguard-slate/10">
                                <div className="text-center">
                                    <Shield size={20} className="mx-auto mb-2 text-slate-500" />
                                    <div className="font-mono text-[9px] uppercase text-slate-400">Durability</div>
                                    <div className="font-mono text-[10px] font-bold text-white">LEVEL IV</div>
                                </div>
                                <div className="text-center">
                                    <Target size={20} className="mx-auto mb-2 text-slate-500" />
                                    <div className="font-mono text-[9px] uppercase text-slate-400">Precision</div>
                                    <div className="font-mono text-[10px] font-bold text-white">±0.01MM</div>
                                </div>
                                <div className="text-center">
                                    <Zap size={20} className="mx-auto mb-2 text-slate-500" />
                                    <div className="font-mono text-[9px] uppercase text-slate-400">Response</div>
                                    <div className="font-mono text-[10px] font-bold text-white">INSTANT</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Related Products */}
                <section className="mt-32">
                    <div className="flex items-center gap-4 mb-12">
                        <h2 className="font-mono text-xl font-bold text-white uppercase tracking-tighter">Supplemental Gear</h2>
                        <div className="flex-grow h-px bg-vanguard-slate/10" />
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                        {related.map(p => (
                            <ProductCard key={p.id} product={p} />
                        ))}
                    </div>
                </section>
            </div>
        </div>
    );
};
