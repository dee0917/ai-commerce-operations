import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './hooks/useAuth';
import { CartProvider } from './hooks/useCart';
import { WishlistProvider } from './hooks/useWishlist';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';

import Home from './pages/Home';
import Shop from './pages/Shop';
import Wishlist from './pages/Wishlist';
import ProductDetail from './pages/ProductDetail';
import { About, Contact, Checkout, AccountLayout, DashboardPage, LoginPage, RegisterPage, OrdersPage, ProfilePage } from './pages/Misc';
import { FAQ, Privacy, Terms, Shipping, Returns, Payment } from './pages/Policies';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <CartProvider>
          <WishlistProvider>
            <Routes>
              <Route path="/" element={<Layout />}>
                <Route index element={<Home />} />
                <Route path="shop" element={<Shop />} />
                <Route path="wishlist" element={<Wishlist />} />
                <Route path="product/:slug" element={<ProductDetail />} />
                <Route path="about" element={<About />} />
                <Route path="contact" element={<Contact />} />
                <Route path="checkout" element={<Checkout />} />

                {/* Policies */}
                <Route path="policies/faq" element={<FAQ />} />
                <Route path="policies/privacy" element={<Privacy />} />
                <Route path="policies/terms" element={<Terms />} />
                <Route path="policies/shipping" element={<Shipping />} />
                <Route path="policies/returns" element={<Returns />} />
                <Route path="policies/payment" element={<Payment />} />

                {/* Account */}
                <Route path="account/login" element={<LoginPage />} />
                <Route path="account/register" element={<RegisterPage />} />
                <Route path="account" element={<ProtectedRoute><AccountLayout /></ProtectedRoute>}>
                  <Route index element={<Navigate to="dashboard" />} />
                  <Route path="dashboard" element={<DashboardPage />} />
                  <Route path="orders" element={<OrdersPage />} />
                  <Route path="profile" element={<ProfilePage />} />
                </Route>
              </Route>
            </Routes>
          </WishlistProvider>
        </CartProvider>
      </AuthProvider>
    </BrowserRouter>
  );
};

export default App;
