import React from 'react';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
    return (
        <footer className="bg-brand-primary border-[0.5px] border-stone-400/30 pt-24 pb-12 mt-32">
            <div className="max-w-7xl mx-auto px-8 grid grid-cols-1 md:grid-cols-4 gap-16 md:gap-8">
                <div className="md:col-span-2">
                    <Link to="/" className="font-display tracking-[0.25em] uppercase text-3xl block mb-6">
                        AuraGuard
                    </Link>
                    <p className="font-light tracking-wide max-w-sm text-sm leading-relaxed mb-8 opacity-80">
                        Authentic, hand-crafted feng shui talismans designed for modern life. Protect your energy.
                    </p>
                    <div className="flex gap-6">
                        <a href="#" className="uppercase tracking-[0.1em] text-xs hover:text-brand-accent transition-colors">Instagram</a>
                        <a href="#" className="uppercase tracking-[0.1em] text-xs hover:text-brand-accent transition-colors">Pinterest</a>
                    </div>
                </div>

                <div>
                    <h4 className="font-display uppercase tracking-widest text-lg mb-6 border-b-[0.5px] border-stone-400 pb-2 inline-block">Explore</h4>
                    <ul className="space-y-4 font-light text-sm">
                        <li><Link to="/shop" className="hover:text-brand-accent transition-colors block">All Talismans</Link></li>
                        <li><Link to="/about" className="hover:text-brand-accent transition-colors block">Our Heritage</Link></li>
                        <li><Link to="/contact" className="hover:text-brand-accent transition-colors block">Connect</Link></li>
                    </ul>
                </div>

                <div>
                    <h4 className="font-display uppercase tracking-widest text-lg mb-6 border-b-[0.5px] border-stone-400 pb-2 inline-block">Assistance</h4>
                    <ul className="space-y-4 font-light text-sm">
                        <li><Link to="/policies/faq" className="hover:text-brand-accent transition-colors block">FAQ</Link></li>
                        <li><Link to="/policies/shipping" className="hover:text-brand-accent transition-colors block">Shipping</Link></li>
                        <li><Link to="/policies/returns" className="hover:text-brand-accent transition-colors block">Returns</Link></li>
                        <li><Link to="/policies/privacy" className="hover:text-brand-accent transition-colors block">Privacy Policy</Link></li>
                        <li><Link to="/policies/terms" className="hover:text-brand-accent transition-colors block">Terms of Service</Link></li>
                    </ul>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-8 mt-24 flex flex-col md:flex-row justify-between items-center text-xs opacity-50 uppercase tracking-[0.15em] border-t-[0.5px] border-stone-400/30 pt-6">
                <p>&copy; {new Date().getFullYear()} AuraGuard. All rights reserved.</p>
                <div className="flex gap-6 mt-4 md:mt-0">
                    <Link to="/policies/privacy" className="hover:text-brand-accent transition-colors">Privacy</Link>
                    <Link to="/policies/terms" className="hover:text-brand-accent transition-colors">Terms</Link>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
