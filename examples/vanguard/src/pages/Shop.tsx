import React, { useEffect, useState } from 'react';
import { fetchProducts, fetchCategories } from '../services/api';
import { ProductCard } from '../components/ProductCard';
import type { WooProduct, WooCategory } from '../types';
import { SlidersHorizontal, LayoutGrid, List } from 'lucide-react';
import { clsx } from 'clsx';

export const Shop: React.FC = () => {
    const [products, setProducts] = useState<WooProduct[]>([]);
    const [categories, setCategories] = useState<WooCategory[]>([]);
    const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            const [productsData, categoriesData] = await Promise.all([
                fetchProducts({ category: selectedCategory || undefined, per_page: 20 }),
                fetchCategories()
            ]);
            setProducts(productsData);
            setCategories(categoriesData);
            setLoading(false);
        };
        loadData();
    }, [selectedCategory]);

    return (
        <div className="bg-vanguard-obsidian min-h-screen pb-20">
            {/* Header */}
            <div className="bg-vanguard-industrial border-b border-vanguard-slate/20 py-16 px-4">
                <div className="max-w-7xl mx-auto">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="h-px w-8 bg-vanguard-red" />
                        <span className="font-mono text-vanguard-red text-[10px] font-bold tracking-[0.4em] uppercase text-shadow-tactical">Inventory Access</span>
                    </div>
                    <h1 className="text-4xl md:text-5xl font-black text-white uppercase tracking-tighter">Battle-Ready Gear</h1>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 mt-12 grid lg:grid-cols-5 gap-12">
                {/* Sidebar Filters */}
                <aside className="lg:col-span-1 space-y-10">
                    <div>
                        <h3 className="font-mono text-xs font-bold text-white uppercase tracking-widest mb-6 flex items-center gap-2">
                            <SlidersHorizontal size={14} className="text-vanguard-red" />
                            Category Filter
                        </h3>
                        <ul className="space-y-3">
                            <li>
                                <button
                                    onClick={() => setSelectedCategory(null)}
                                    className={clsx(
                                        "font-mono text-[11px] uppercase tracking-widest transition-colors w-full text-left",
                                        !selectedCategory ? "text-vanguard-red font-bold" : "text-slate-500 hover:text-white"
                                    )}
                                >
                                    [ All Departments ]
                                </button>
                            </li>
                            {categories.map(cat => (
                                <li key={cat.id}>
                                    <button
                                        onClick={() => setSelectedCategory(cat.slug)}
                                        className={clsx(
                                            "font-mono text-[11px] uppercase tracking-widest transition-colors w-full text-left",
                                            selectedCategory === cat.slug ? "text-vanguard-red font-bold" : "text-slate-500 hover:text-white"
                                        )}
                                    >
                                        {cat.name}
                                    </button>
                                </li>
                            ))}
                        </ul>
                    </div>

                    <div className="pt-10 border-t border-vanguard-slate/10">
                        <div className="bg-vanguard-industrial/50 p-6 border border-vanguard-slate/10">
                            <h4 className="font-mono text-[10px] font-bold text-white uppercase mb-4 tracking-widest">Tactical Support</h4>
                            <p className="text-[10px] text-slate-500 leading-relaxed uppercase">
                                All gear is inspected and encrypted before dispatch. Guaranteed lifetime performance.
                            </p>
                        </div>
                    </div>
                </aside>

                {/* Product Grid */}
                <div className="lg:col-span-4">
                    <div className="flex justify-between items-center mb-8 pb-4 border-b border-vanguard-slate/10">
                        <span className="font-mono text-[10px] text-slate-500 uppercase">
                            {loading ? "Scanning..." : `${products.length} Results Found`}
                        </span>
                        <div className="flex items-center gap-4 text-slate-500">
                            <button className="p-1 hover:text-vanguard-red transition-colors"><LayoutGrid size={18} /></button>
                            <button className="p-1 hover:text-vanguard-red transition-colors opacity-30"><List size={18} /></button>
                        </div>
                    </div>

                    {loading ? (
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            {[...Array(6)].map((_, i) => (
                                <div key={i} className="aspect-[4/5] skeleton rounded-lg" />
                            ))}
                        </div>
                    ) : products.length === 0 ? (
                        <div className="py-20 text-center border border-dashed border-vanguard-slate/20">
                            <p className="font-mono text-xs text-slate-500 uppercase">No gear found in this department.</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            {products.map(product => (
                                <ProductCard key={product.id} product={product} />
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};
