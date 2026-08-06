import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Home } from './pages/Home';
import { Shop } from './pages/Shop';
import { ProductDetail } from './pages/ProductDetail';
import { Cart } from './pages/Cart';
import { Checkout } from './pages/Checkout';
import { MissionHistory } from './pages/MissionHistory';
import { SizeGuide } from './pages/SizeGuide';
import { FAQ } from './pages/FAQ';
import { TacticalSupport, SecurityProtocol } from './pages/Intelligence';
import { PrivacyPolicy, TermsOfService, ShippingPolicy } from './pages/policies/Policies';
import { CartDrawer } from './components/CartDrawer';
import { ScrollToTop } from './components/ScrollToTop';
import { Toaster } from 'react-hot-toast';

function App() {
  const [isCartOpen, setIsCartOpen] = useState(false);

  return (
    <Router>
      <ScrollToTop />
      <div className="min-h-screen flex flex-col">
        <Toaster position="bottom-right" />
        <Navbar onOpenCart={() => setIsCartOpen(true)} />
        <CartDrawer isOpen={isCartOpen} onClose={() => setIsCartOpen(false)} />

        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/shop" element={<Shop />} />
            <Route path="/product/:slug" element={<ProductDetail />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/checkout" element={<Checkout />} />
            <Route path="/categories/:slug" element={<Shop />} />
            <Route path="/mission-history" element={<MissionHistory />} />
            <Route path="/size-guide" element={<SizeGuide />} />
            <Route path="/faq" element={<FAQ />} />
            <Route path="/intelligence/support" element={<TacticalSupport />} />
            <Route path="/intelligence/security" element={<SecurityProtocol />} />
            <Route path="/policies/privacy" element={<PrivacyPolicy />} />
            <Route path="/policies/terms" element={<TermsOfService />} />
            <Route path="/policies/shipping" element={<ShippingPolicy />} />
          </Routes>
        </main>

        <footer className="bg-black py-20 border-t border-vanguard-slate/20">
          <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-4 gap-12">
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center gap-2 mb-6">
                <div className="bg-vanguard-red p-1 rounded-sm">
                  <div className="w-6 h-6 border-2 border-white rounded-full flex items-center justify-center">
                    <div className="w-1.5 h-1.5 bg-white rounded-full" />
                  </div>
                </div>
                <span className="font-mono text-xl font-bold tracking-widest text-white">VANGUARD GEAR</span>
              </div>
              <p className="text-slate-500 text-sm max-w-sm mb-8 leading-relaxed">
                Hardware for the modern age. We specialize in precision tools and EDC systems designed for survivability and minimalist efficiency.
              </p>
              <div className="flex gap-4">
                {['INSTAGRAM', 'X-TWITTER', 'COMM CHANNEL'].map((link) => (
                  <a key={link} href="#" className="font-mono text-[10px] text-slate-400 hover:text-vanguard-red transition-colors tracking-widest">{link}</a>
                ))}
              </div>
            </div>

            <div>
              <h4 className="font-mono text-xs font-bold text-white uppercase tracking-widest mb-6 underline decoration-vanguard-red">Inventory</h4>
              <ul className="space-y-3 font-mono text-[11px] text-slate-500 uppercase tracking-widest">
                <li><Link to="/categories/core-essentials" className="hover:text-vanguard-red transition-colors">Core Essentials</Link></li>
                <li><Link to="/categories/technical-carry" className="hover:text-vanguard-red transition-colors">Technical Carry</Link></li>
                <li><Link to="/categories/precision-tools" className="hover:text-vanguard-red transition-colors">Precision Tools</Link></li>
                <li><Link to="/shop" className="hover:text-vanguard-red transition-colors">Limited Drops</Link></li>
              </ul>
            </div>

            <div>
              <h4 className="font-mono text-xs font-bold text-white uppercase tracking-widest mb-6 underline decoration-vanguard-red">Intelligence</h4>
              <ul className="space-y-3 font-mono text-[11px] text-slate-500 uppercase tracking-widest">
                <li><Link to="/intelligence/support" className="hover:text-vanguard-red transition-colors">Tactical Support</Link></li>
                <li><Link to="/faq" className="hover:text-vanguard-red transition-colors">FAQ / Field Manual</Link></li>
                <li><Link to="/size-guide" className="hover:text-vanguard-red transition-colors">Size & Dimensions</Link></li>
                <li><Link to="/mission-history" className="hover:text-vanguard-red transition-colors">Mission History</Link></li>
              </ul>
            </div>
          </div>

          <div className="max-w-7xl mx-auto px-4 mt-20 pt-8 border-t border-vanguard-slate/10 flex flex-col md:flex-row justify-between items-center gap-6">
            <p className="font-mono text-[10px] text-slate-600 uppercase tracking-tighter">
              © 2026 VANGUARD GEAR // SYSTEM VERSION: 5.0.1 // ALL RIGHTS RESERVED.
            </p>
            <div className="flex gap-8 font-mono text-[10px] text-slate-600 uppercase transition-colors">
              <Link to="/policies/privacy" className="hover:text-white">Privacy Protocol</Link>
              <Link to="/policies/terms" className="hover:text-white">Terms of Ops</Link>
              <Link to="/policies/shipping" className="hover:text-white">Logistics Info</Link>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
