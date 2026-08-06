import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import { CartProvider } from './hooks/useCart';
import Navbar from './components/Navbar';
import ScrollToTop from './components/ScrollToTop';
import Home from './pages/Home';
import Shop from './pages/Shop';
import ProductDetail from './pages/ProductDetail';
import Checkout from './pages/Checkout';
import FAQ from './pages/FAQ';

function App() {
    return (
        <HelmetProvider>
            <CartProvider>
                <Router>
                    <ScrollToTop />
                    <div className="min-h-screen flex flex-col font-sans text-brand-dark">
                        <Navbar />
                        <main className="flex-grow">
                            <Routes>
                                <Route path="/" element={<Home />} />
                                <Route path="/shop" element={<Shop />} />
                                <Route path="/product/:id" element={<ProductDetail />} />
                                <Route path="/checkout" element={<Checkout />} />
                                <Route path="/faq" element={<FAQ />} />
                            </Routes>
                        </main>
                        <footer className="bg-white border-t border-gray-100 mt-20 py-12">
                            <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-gray-500">
                                <p>&copy; {new Date().getFullYear()} Gridwell. Organization meets visual harmony.</p>
                                <nav className="flex items-center gap-6">
                                    <Link to="/shop" className="hover:text-brand-dark transition-colors">Shop</Link>
                                    <Link to="/faq" className="hover:text-brand-dark transition-colors">Help & FAQ</Link>
                                </nav>
                            </div>
                        </footer>
                    </div>
                </Router>
            </CartProvider>
        </HelmetProvider>
    );
}

export default App;
