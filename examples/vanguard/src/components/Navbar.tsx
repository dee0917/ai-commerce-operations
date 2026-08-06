import React from 'react';
import { ShoppingBag, Target, Menu, Search } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useCart } from '../hooks/useCart';

export const Navbar: React.FC<{ onOpenCart: () => void }> = ({ onOpenCart }) => {
    const totalItems = useCart((state) => state.totalItems());

    return (
        <nav className="sticky top-0 z-50 w-full bg-vanguard-obsidian/90 backdrop-blur-md border-b border-vanguard-slate/20">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-20">
                    <div className="flex items-center gap-4">
                        <button className="p-2 hover:bg-vanguard-slate/20 rounded-full lg:hidden">
                            <Menu size={24} />
                        </button>
                        <Link to="/" className="flex items-center gap-2 group">
                            <div className="bg-vanguard-red p-1.5 rounded-sm group-hover:rotate-12 transition-transform">
                                <Target size={24} className="text-white" />
                            </div>
                            <span className="font-mono text-xl font-bold tracking-widest text-white">VANGUARD</span>
                        </Link>
                    </div>

                    <div className="hidden lg:flex items-center space-x-8">
                        <Link to="/shop" className="font-mono text-sm uppercase tracking-widest hover:text-vanguard-red transition-colors">Shop All</Link>
                        <Link to="/categories/core-essentials" className="font-mono text-sm uppercase tracking-widest hover:text-vanguard-red transition-colors">Essentials</Link>
                        <Link to="/categories/technical-carry" className="font-mono text-sm uppercase tracking-widest hover:text-vanguard-red transition-colors">Carry</Link>
                    </div>

                    <div className="flex items-center space-x-4">
                        <button className="p-2 hover:bg-vanguard-slate/20 rounded-full transition-colors hidden sm:block">
                            <Search size={20} />
                        </button>
                        <button
                            onClick={onOpenCart}
                            className="relative p-2 hover:bg-vanguard-slate/20 rounded-full transition-colors group"
                        >
                            <ShoppingBag size={24} />
                            {totalItems > 0 && (
                                <span className="absolute -top-1 -right-1 bg-vanguard-red text-white text-[10px] font-bold h-5 w-5 rounded-full flex items-center justify-center animate-pulse">
                                    {totalItems}
                                </span>
                            )}
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    );
};
