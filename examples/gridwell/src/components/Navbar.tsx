import { useState } from 'react';
import { Link } from 'react-router-dom';
import { ShoppingBag, Menu, X } from 'lucide-react';
import { useCart } from '../hooks/useCart';
import CartSidebar from './CartSidebar';

const Navbar = () => {
    const { totalItems } = useCart();
    const [isSidebarOpen, setSidebarOpen] = useState(false);
    const [isMobileMenuOpen, setMobileMenuOpen] = useState(false);

    return (
        <>
            <nav className="sticky top-0 z-50 bg-brand-light/80 backdrop-blur-md border-b border-brand-dark/10">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <div className="flex items-center">
                            <Link to="/" className="text-lg font-display font-normal tracking-tight text-brand-dark">
                                Gridwell<span className="text-brand-accent">.</span>
                            </Link>
                        </div>

                        <div className="hidden md:flex flex-1 justify-center space-x-8">
                            <Link to="/" className="text-sm font-sans text-brand-dark/60 hover:text-brand-dark transition-colors">Home</Link>
                            <Link to="/shop" className="text-sm font-sans text-brand-dark/60 hover:text-brand-dark transition-colors">Shop</Link>
                            <Link to="/faq" className="text-sm font-sans text-brand-dark/60 hover:text-brand-dark transition-colors">Help</Link>
                        </div>

                        <div className="flex items-center space-x-4">
                            <button
                                onClick={() => setSidebarOpen(true)}
                                className="relative p-2 text-gray-600 hover:text-brand-dark transition-colors"
                                aria-label="Cart"
                            >
                                <ShoppingBag className="w-5 h-5" />
                                {totalItems > 0 && (
                                    <span className="absolute top-1 right-1 bg-brand-accent text-white text-[10px] font-sans font-bold h-4 w-4 rounded-full flex items-center justify-center">
                                        {totalItems}
                                    </span>
                                )}
                            </button>

                            <button
                                className="md:hidden p-2 text-gray-600"
                                onClick={() => setMobileMenuOpen(!isMobileMenuOpen)}
                            >
                                {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
                            </button>
                        </div>
                    </div>
                </div>

                {/* Mobile menu */}
                {isMobileMenuOpen && (
                    <div className="md:hidden bg-white border-b border-gray-100 px-4 py-4 space-y-2">
                        <Link to="/" className="block py-2 text-base font-medium text-gray-800" onClick={() => setMobileMenuOpen(false)}>Home</Link>
                        <Link to="/shop" className="block py-2 text-base font-medium text-gray-800" onClick={() => setMobileMenuOpen(false)}>Shop All</Link>
                        <Link to="/faq" className="block py-2 text-base font-medium text-gray-800" onClick={() => setMobileMenuOpen(false)}>Help & FAQ</Link>
                    </div>
                )}
            </nav>

            <CartSidebar isOpen={isSidebarOpen} onClose={() => setSidebarOpen(false)} />
        </>
    );
};

export default Navbar;
