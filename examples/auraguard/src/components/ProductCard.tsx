import React, { memo } from 'react';
import { Heart } from 'lucide-react';
import type { WooProduct } from '../types';
import { useCart } from '../hooks/useCart';
import { useWishlist } from '../hooks/useWishlist';
import clsx from 'clsx';
import { Link } from 'react-router-dom';

interface Props {
    product: WooProduct;
}

const ProductCard: React.FC<Props> = ({ product }) => {
    const { addToCart } = useCart();
    const { toggleWishlist, isInWishlist } = useWishlist();

    const hasMultipleImages = product.images.length > 1;
    const isWishlisted = isInWishlist(product.id);

    return (
        <div className="group relative flex flex-col fade-up">
            <div className="relative aspect-[3/4] overflow-hidden bg-brand-secondary/5 border border-stone-200">
                <Link to={`/product/${product.slug}`} className="block w-full h-full">
                    <img
                        src={product.images[0]?.src}
                        alt={product.images[0]?.alt || product.name}
                        className={clsx(
                            "absolute inset-0 w-full h-full object-cover transition-all duration-700 group-hover:scale-110",
                            hasMultipleImages && "group-hover:opacity-0"
                        )}
                        loading="lazy"
                    />
                    {hasMultipleImages && (
                        <img
                            src={product.images[1]?.src}
                            alt={product.images[1]?.alt || product.name}
                            className="absolute inset-0 w-full h-full object-cover opacity-0 transition-opacity duration-700 group-hover:opacity-100 group-hover:scale-110"
                            loading="lazy"
                        />
                    )}
                </Link>

                {/* Tags */}
                <div className="absolute top-4 left-4 flex flex-col gap-2 z-10">
                    <span className="bg-brand-primary/80 backdrop-blur-md text-brand-secondary text-[8px] px-2 py-1 tracking-[0.2em] uppercase font-bold border border-stone-300">Purified</span>
                </div>

                {/* Wishlist */}
                <button
                    onClick={(e) => { e.preventDefault(); toggleWishlist(product.id); }}
                    className="absolute top-4 right-4 p-2 bg-brand-primary/80 backdrop-blur-md border border-stone-200 rounded-full opacity-0 translate-y-[-10px] group-hover:translate-y-0 group-hover:opacity-100 transition-all hover:bg-brand-accent hover:text-white"
                >
                    <Heart className={clsx("w-3 h-3 transition-colors", isWishlisted ? "fill-current" : "")} />
                </button>

                {/* Quick Add To Cart */}
                {product.purchasable && product.stock_status !== 'outofstock' && (
                    <button
                        onClick={(e) => { e.preventDefault(); addToCart(product, 1); }}
                        className="absolute bottom-0 left-0 right-0 bg-brand-secondary text-brand-primary py-4 uppercase tracking-[0.3em] text-[10px] font-bold opacity-0 translate-y-full group-hover:translate-y-0 group-hover:opacity-100 transition-all hover:bg-brand-accent flex items-center justify-center gap-2"
                    >
                        Anchor to Bag
                    </button>
                )}
            </div>

            <div className="mt-6 space-y-2">
                <div className="flex justify-between items-start gap-4">
                    <h3 className="font-display text-xl uppercase tracking-tighter leading-none flex-1">
                        <Link to={`/product/${product.slug}`} className="hover:text-brand-accent transition-colors">
                            {product.name}
                        </Link>
                    </h3>
                    <div className="text-sm font-light tracking-widest">
                        <span>${product.price}</span>
                    </div>
                </div>
                <p className="text-[10px] uppercase tracking-[0.2em] opacity-40 font-bold">
                    {product.categories[0]?.name}
                </p>
            </div>
        </div>
    );
};

export default memo(ProductCard);
