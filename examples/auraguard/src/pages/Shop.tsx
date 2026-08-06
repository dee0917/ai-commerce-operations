import React, { useEffect, useState } from 'react';
import { fetchProducts, fetchCategories } from '../services/api';
import type { WooProduct, WooCategory } from '../types';
import ProductCard from '../components/ProductCard';

const Shop: React.FC = () => {
    const [products, setProducts] = useState<WooProduct[]>([]);
    const [categories, setCategories] = useState<WooCategory[]>([]);
    const [activeCategory, setActiveCategory] = useState<string>('');
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        Promise.all([
            fetchCategories(),
            fetchProducts({ category: activeCategory || undefined })
        ]).then(([cats, prods]) => {
            setCategories(cats);
            setProducts(prods);
            setIsLoading(false);
        });
    }, [activeCategory]);

    return (
        <div className="pt-32 max-w-[1400px] mx-auto px-8 pb-32">
            <header className="mb-16 fade-up">
                <h1 className="text-6xl font-display uppercase tracking-widest font-light mb-6 border-b-[0.5px] border-stone-400 pb-4">
                    All Talismans
                </h1>
                <div className="flex flex-wrap gap-8 items-center text-sm uppercase tracking-[0.2em]">
                    <button
                        onClick={() => setActiveCategory('')}
                        className={`pb-1 border-b transition-colors ${!activeCategory ? 'border-brand-secondary text-brand-secondary' : 'border-transparent text-brand-secondary/50 hover:text-brand-secondary'}`}
                    >
                        All View
                    </button>
                    {categories.map(cat => (
                        <button
                            key={cat.id}
                            onClick={() => setActiveCategory(cat.id.toString())}
                            className={`pb-1 border-b transition-colors ${activeCategory === cat.id.toString() ? 'border-brand-secondary text-brand-secondary' : 'border-transparent text-brand-secondary/50 hover:text-brand-secondary'}`}
                        >
                            {cat.name}
                        </button>
                    ))}
                </div>
            </header>

            {isLoading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                    {[...Array(8)].map((_, i) => (
                        <div key={i} className="aspect-square bg-brand-secondary/5 animate-pulse rounded-sm" />
                    ))}
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 fade-up">
                    {products.map(product => (
                        <ProductCard key={product.id} product={product} />
                    ))}
                    {products.length === 0 && (
                        <div className="col-span-full py-24 text-center font-display text-2xl uppercase tracking-widest opacity-50">
                            No talismans found for this category.
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default Shop;
