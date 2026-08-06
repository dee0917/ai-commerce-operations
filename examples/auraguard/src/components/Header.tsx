import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ShoppingBag, User, Heart, Menu, X } from 'lucide-react';
import { useCart } from '../hooks/useCart';
import { useAuth } from '../hooks/useAuth';
import clsx from 'clsx';

const Header: React.FC = () => {
    const { user, isAuthenticated, signOut } = useAuth();
    const { itemCount, setIsDrawerOpen } = useCart();
    const [isScrolled, setIsScrolled] = useState(false);
    const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 50);
            if (isMobileMenuOpen) setIsMobileMenuOpen(false);
        };
        window.addEventListener('scroll', handleScroll, { passive: true });
        return () => window.removeEventListener('scroll', handleScroll);
    }, [isMobileMenuOpen]);

    const closeMobileMenu = () => setIsMobileMenuOpen(false);

    return (
        <>
            <header
                className={clsx(
                    "fixed w-full z-40 transition-all duration-500",
                    isScrolled ? "top-4 pointer-events-none" : "top-0 pointer-events-auto"
                )}
            >
                <div
                    className={clsx(
                        "mx-auto flex items-center justify-between transition-all duration-500",
                        isScrolled
                            ? "max-w-4xl bg-brand-primary/95 backdrop-blur-md shadow-2xl rounded-full px-8 py-3 pointer-events-auto border border-brand-secondary/5 border-b-[0.5px] border-b-stone-400"
                            : "max-w-[1400px] px-8 py-6"
                    )}
                >
                    <div className="flex-1 flex gap-8 items-center">
                        <Link to="/shop" className="text-sm font-bold tracking-[0.2em] uppercase hover:text-brand-accent transition-colors hidden lg:block">
                            Collection
                        </Link>
                        <Link to="/about" className="text-sm font-bold tracking-[0.2em] uppercase hover:text-brand-accent transition-colors hidden lg:block">
                            Heritage
                        </Link>
                        <Link to="/contact" className="text-sm font-bold tracking-[0.2em] uppercase hover:text-brand-accent transition-colors hidden lg:block">
                            Contact
                        </Link>
                        {/* Hamburger - mobile only */}
                        <button
                            className="lg:hidden hover:text-brand-accent transition-colors"
                            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                            aria-label="Toggle mobile menu"
                        >
                            {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                        </button>
                    </div>

                    <Link to="/" className="flex-1 text-center font-display tracking-[0.3em] uppercase text-2xl lg:text-3xl whitespace-nowrap">
                        AuraGuard
                    </Link>

                    <div className="flex-1 flex justify-end items-center gap-6">
                        <Link to="/wishlist" className="hover:text-brand-accent transition-transform hover:scale-110" onClick={closeMobileMenu}>
                            <Heart className="w-5 h-5" />
                        </Link>

                        <div className="relative group">
                            <button
                                className="flex items-center hover:scale-110 transition-transform"
                                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                            >
                                {!isAuthenticated ? (
                                    <User className="w-5 h-5" onClick={(e) => { e.preventDefault(); window.location.href = '/account/login' }} />
                                ) : (
                                    <div className="w-6 h-6 rounded-full bg-brand-secondary text-brand-primary flex items-center justify-center text-xs font-bold leading-none select-none">
                                        {user?.first_name?.[0] || 'U'}
                                    </div>
                                )}
                            </button>
                            {isAuthenticated && isUserMenuOpen && (
                                <div className="absolute right-0 top-full mt-4 w-48 bg-brand-primary border border-brand-secondary/10 shadow-2xl py-2 rounded-lg flex flex-col font-medium tracking-wide">
                                    <div className="px-4 py-3 border-b border-brand-secondary/10 font-display text-lg mb-2">
                                        Hi, {user?.first_name}
                                    </div>
                                    <Link to="/account/dashboard" className="px-4 py-2 hover:bg-brand-secondary/5 hover:text-brand-accent transition-colors text-sm">My Account</Link>
                                    <Link to="/account/orders" className="px-4 py-2 hover:bg-brand-secondary/5 hover:text-brand-accent transition-colors text-sm">Orders</Link>
                                    <Link to="/account/profile" className="px-4 py-2 hover:bg-brand-secondary/5 hover:text-brand-accent transition-colors text-sm">Profile</Link>
                                    <button
                                        onClick={signOut}
                                        className="px-4 py-2 text-left hover:bg-brand-secondary/5 hover:text-brand-accent transition-colors text-sm mt-2 border-t border-brand-secondary/10 pt-3"
                                    >
                                        Sign Out
                                    </button>
                                </div>
                            )}
                        </div>

                        <button
                            className="relative hover:text-brand-accent transition-transform hover:scale-110"
                            onClick={() => setIsDrawerOpen(true)}
                        >
                            <ShoppingBag className="w-5 h-5" />
                            {itemCount > 0 && (
                                <span className="absolute -top-1.5 -right-2 bg-brand-accent text-white text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center leading-none">
                                    {itemCount}
                                </span>
                            )}
                        </button>
                    </div>
                </div>
            </header>

            {/* Mobile menu overlay */}
            {isMobileMenuOpen && (
                <div className="fixed inset-0 z-30 lg:hidden" onClick={closeMobileMenu}>
                    <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" />
                    <nav
                        className="absolute top-0 left-0 w-[280px] h-full bg-brand-primary flex flex-col pt-24 px-8 gap-2 shadow-2xl"
                        onClick={e => e.stopPropagation()}
                    >
                        <div className="border-b border-stone-300 pb-6 mb-6">
                            <p className="text-[10px] uppercase tracking-[0.5em] font-bold text-brand-accent mb-2">Navigate</p>
                        </div>
                        <Link to="/shop" className="text-2xl font-display uppercase tracking-widest font-light py-3 hover:text-brand-accent transition-colors border-b border-stone-200" onClick={closeMobileMenu}>Collection</Link>
                        <Link to="/about" className="text-2xl font-display uppercase tracking-widest font-light py-3 hover:text-brand-accent transition-colors border-b border-stone-200" onClick={closeMobileMenu}>Heritage</Link>
                        <Link to="/contact" className="text-2xl font-display uppercase tracking-widest font-light py-3 hover:text-brand-accent transition-colors border-b border-stone-200" onClick={closeMobileMenu}>Contact</Link>
                        <Link to="/wishlist" className="text-2xl font-display uppercase tracking-widest font-light py-3 hover:text-brand-accent transition-colors border-b border-stone-200" onClick={closeMobileMenu}>Wishlist</Link>
                        <Link to="/account/login" className="text-2xl font-display uppercase tracking-widest font-light py-3 hover:text-brand-accent transition-colors" onClick={closeMobileMenu}>Account</Link>
                    </nav>
                </div>
            )}
        </>
    );
};

export default Header;
