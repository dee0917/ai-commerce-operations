import React, { useState } from 'react';
import { Plus, Heart, Eye } from 'lucide-react';
import { Link } from 'react-router-dom';
import type { WooProduct } from '../types';
import { useCart } from '../hooks/useCart';
import { clsx } from 'clsx';
import { toast } from 'react-hot-toast';
import { SafeImage } from './SafeImage';

interface ProductCardProps {
    product: WooProduct;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
    const [isHovered, setIsHovered] = useState(false);
    const [isWishlisted, setIsWishlisted] = useState(false);
    const addItem = useCart((state) => state.addItem);

    const handleAddToCart = (e: React.MouseEvent) => {
        e.preventDefault();
        addItem(product);
        toast.success(`Kit Updated: ${product.name}`, {
            style: {
                background: '#121212',
                color: '#fff',
                border: '1px solid #FF3D00',
                fontFamily: 'IBM Plex Mono',
            }
        });
    };

    const toggleWishlist = (e: React.MouseEvent) => {
        e.preventDefault();
        setIsWishlisted(!isWishlisted);
        if (!isWishlisted) {
            toast('Mission Favorite Logged', {
                icon: '🎯',
                style: { background: '#121212', color: '#fff', border: '1px solid #334155', fontFamily: 'IBM Plex Mono' }
            });
        }
    };

    return (
        <div
            className="group relative bento-card flex flex-col h-full bg-vanguard-obsidian border border-vanguard-slate/10 hover:border-vanguard-red/30 transition-all duration-500"
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
        >
            {/* Badges */}
            <div className="absolute top-3 left-3 z-10 flex flex-col gap-2">
                {product.stock_status === 'outofstock' && (
                    <span className="bg-slate-700 text-white text-[9px] font-mono font-bold px-2 py-0.5 uppercase tracking-tighter">
                        Depleted
                    </span>
                )}
            </div>

            {/* Wishlist Button */}
            <button
                onClick={toggleWishlist}
                className="absolute top-3 right-3 z-10 p-2 rounded-full bg-black/40 backdrop-blur-md border border-white/5 text-slate-400 hover:text-vanguard-red hover:border-vanguard-red/50 transition-all duration-300"
            >
                <Heart size={14} className={clsx(isWishlisted && "fill-vanguard-red text-vanguard-red scale-110", "transition-transform")} />
            </button>

            {/* Image Gallery */}
            <Link to={`/product/${product.slug}`} className="relative aspect-square overflow-hidden bg-vanguard-industrial flex items-center justify-center">
                <SafeImage
                    src={product.images[0]?.src}
                    alt={product.name}
                    className={clsx(
                        "w-full h-full object-cover transition-all duration-1000 grayscale-[20%] group-hover:grayscale-0",
                        isHovered && product.images[1] ? "opacity-0 scale-105" : "opacity-100 scale-100"
                    )}
                />
                {product.images[1] && (
                    <SafeImage
                        src={product.images[1].src}
                        alt={`${product.name} detail`}
                        className={clsx(
                            "absolute inset-0 w-full h-full object-cover transition-all duration-1000",
                            isHovered ? "opacity-100 scale-110" : "opacity-0 scale-100"
                        )}
                    />
                )}

                {/* Quick Actions Overlay */}
                <div className={clsx(
                    "absolute inset-0 bg-vanguard-obsidian/40 backdrop-blur-[2px] flex items-center justify-center gap-4 transition-all duration-500",
                    isHovered ? "opacity-100" : "opacity-0 pointer-events-none"
                )}>
                    <Link
                        to={`/product/${product.slug}`}
                        className="p-4 bg-white text-vanguard-obsidian rounded-full hover:bg-vanguard-red hover:text-white transition-all transform hover:rotate-12 active:scale-95 shadow-xl"
                    >
                        <Eye size={20} />
                    </Link>
                </div>
            </Link>

            {/* Info */}
            <div className="p-5 flex flex-col flex-grow bg-vanguard-industrial/30">
                <div className="flex justify-between items-start mb-3">
                    <Link to={`/product/${product.slug}`} className="font-mono text-[13px] font-black text-white uppercase tracking-tighter hover:text-vanguard-red transition-colors flex-grow leading-tight">
                        {product.name}
                    </Link>
                    <div className="flex flex-col items-end shrink-0 ml-4">
                        <span className="text-white font-mono font-bold text-sm">${product.price}</span>
                    </div>
                </div>

                <p className="text-[11px] text-slate-500 line-clamp-2 mb-6 h-8 font-sans leading-relaxed">
                    {product.short_description}
                </p>

                {/* Quick Add Button */}
                <button
                    onClick={handleAddToCart}
                    disabled={product.stock_status === 'outofstock'}
                    className={clsx(
                        "mt-auto w-full py-3 flex items-center justify-center gap-3 font-mono text-[10px] uppercase font-bold tracking-[0.2em] border-2 transition-all duration-300",
                        product.stock_status === 'outofstock'
                            ? "border-vanguard-slate/20 text-slate-600 cursor-not-allowed"
                            : "border-vanguard-slate/30 text-white hover:border-vanguard-red hover:bg-vanguard-red"
                    )}
                >
                    <Plus size={14} className={clsx(product.stock_status !== 'outofstock' && "animate-pulse")} />
                    {product.stock_status === 'outofstock' ? 'Material Depleted' : 'Deploy to Kit'}
                </button>
            </div>
        </div>
    );
};
