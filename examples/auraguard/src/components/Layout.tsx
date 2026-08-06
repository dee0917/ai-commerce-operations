import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';
import CartDrawer from './CartDrawer';
import ScrollToTop from './ScrollToTop';
import { useScrollFade } from '../hooks/useScrollFade';

const Layout: React.FC = () => {
    // Re-run scroll observer on route change
    useScrollFade();

    return (
        <div className="min-h-screen flex flex-col">
            <ScrollToTop />
            <Header />
            <main className="flex-1">
                <Outlet />
            </main>
            <Footer />
            <CartDrawer />
        </div>
    );
};

export default Layout;
