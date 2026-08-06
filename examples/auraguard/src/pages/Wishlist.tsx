import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Heart } from 'lucide-react';
import { fetchProducts } from '../services/api';
import type { WooProduct } from '../types';
import { useWishlist } from '../hooks/useWishlist';
import ProductCard from '../components/ProductCard';

const Wishlist: React.FC = () => {
    const { wishlistIds } = useWishlist();
    const [products, setProducts] = useState<WooProduct[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        fetchProducts({ per_page: 100 }).then(prods => {
            setProducts(prods);
            setIsLoading(false);
        });
    }, []);

    const saved = products.filter(p => wishlistIds.includes(p.id));

    return (
        <div className="pt-32 max-w-[1400px] mx-auto px-8 pb-32">
            <header className="mb-16 fade-up">
                <h1 className="text-6xl font-display uppercase tracking-widest font-light mb-6 border-b-[0.5px] border-stone-400 pb-4">
                    Your Wishlist
                </h1>
                <p className="text-sm uppercase tracking-[0.2em] text-brand-secondary/50">
                    {saved.length > 0
                        ? `${saved.length} Talisman${saved.length === 1 ? '' : 's'} Kept Close`
                        : 'A Quiet Collection of What Calls to You'}
                </p>
            </header>

            {isLoading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                    {[...Array(4)].map((_, i) => (
                        <div key={i} className="aspect-square bg-brand-secondary/5 animate-pulse rounded-sm" />
                    ))}
                </div>
            ) : saved.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 fade-up">
                    {saved.map(product => (
                        <ProductCard key={product.id} product={product} />
                    ))}
                </div>
            ) : (
                <div className="fade-up flex flex-col items-center justify-center text-center py-24 border-[0.5px] border-stone-300">
                    <Heart className="w-10 h-10 text-brand-secondary/30 mb-8" strokeWidth={1} />
                    <h2 className="font-display text-3xl uppercase tracking-widest font-light mb-4">
                        Your Wishlist Is Empty
                    </h2>
                    <p className="text-sm tracking-wide text-brand-secondary/50 max-w-md mb-10 leading-relaxed">
                        Nothing has been kept yet. Wander the collection and press the heart on any
                        talisman that holds your attention.
                    </p>
                    <Link
                        to="/shop"
                        className="bg-brand-secondary text-brand-primary py-4 px-12 uppercase tracking-[0.3em] text-[10px] font-bold transition-colors hover:bg-brand-accent"
                    >
                        Explore Talismans
                    </Link>
                </div>
            )}
        </div>
    );
};

export default Wishlist;
