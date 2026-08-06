import { Helmet } from 'react-helmet-async';
import { useCart } from '../hooks/useCart';
import { Lock } from 'lucide-react';
import { Link } from 'react-router-dom';

const Checkout = () => {
    const { items, totalPrice } = useCart();

    if (items.length === 0) {
        return (
            <div className="max-w-7xl mx-auto px-4 py-24 text-center min-h-[60vh] flex flex-col items-center justify-center">
                <h1 className="text-3xl font-display font-medium text-brand-dark mb-4">Checkout Unavailable</h1>
                <p className="text-gray-500 mb-8">Your cart is empty. Please add items before checking out.</p>
                <Link to="/shop" className="text-brand-dark font-medium underline">Return to Shop</Link>
            </div>
        );
    }

    return (
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <Helmet>
                <title>Checkout | Gridwell</title>
            </Helmet>

            <div className="text-center mb-12">
                <h1 className="text-3xl lg:text-4xl font-display font-medium tracking-tight text-brand-dark mb-2">Secure Checkout</h1>
                <p className="text-gray-500 flex items-center justify-center gap-2">
                    <Lock className="w-4 h-4" /> 256-bit SSL encrypted
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
                <div className="lg:col-span-2 space-y-8">
                    {/* Mock Form */}
                    <div className="bento-card p-6 md:p-8">
                        <h2 className="text-xl font-medium mb-6">Contact Information</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="md:col-span-2">
                                <input type="email" placeholder="Email Address" className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-brand-accent focus:border-transparent transition-all" required />
                            </div>
                        </div>

                        <h2 className="text-xl font-medium mb-6 mt-10">Shipping Address</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <input type="text" placeholder="First Name" className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-brand-accent focus:border-transparent transition-all" />
                            <input type="text" placeholder="Last Name" className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-brand-accent focus:border-transparent transition-all" />
                            <div className="md:col-span-2">
                                <input type="text" placeholder="Address" className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-brand-accent focus:border-transparent transition-all" />
                            </div>
                            <input type="text" placeholder="City" className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-brand-accent focus:border-transparent transition-all" />
                            <input type="text" placeholder="Postal Code" className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-brand-accent focus:border-transparent transition-all" />
                        </div>

                        <h2 className="text-xl font-medium mb-6 mt-10">Payment Method</h2>
                        <div className="p-4 border border-gray-200 rounded-xl bg-gray-50 flex items-center justify-center h-24 text-gray-500">
                            Mock Checkout Mode. Payment bypassed.
                        </div>

                        <button className="w-full bg-brand-dark text-white rounded-xl py-4 font-medium mt-10 hover:bg-black transition-colors">
                            Place Order (${(totalPrice + 5).toFixed(2)})
                        </button>
                    </div>
                </div>

                <div>
                    <div className="bento-card p-6 sticky top-24">
                        <h2 className="text-lg font-medium border-b border-gray-100 pb-4 mb-4">Order Summary</h2>
                        <ul className="space-y-4 mb-6">
                            {items.map(item => (
                                <li key={item.id} className="flex justify-between items-start">
                                    <div className="flex items-center gap-3">
                                        <div className="relative">
                                            <div className="w-12 h-12 bg-gray-50 rounded-lg flex items-center justify-center p-1">
                                                <img src={item.image} alt={item.name} className="max-w-full max-h-full object-contain mix-blend-multiply" />
                                            </div>
                                            <span className="absolute -top-2 -right-2 bg-gray-500 text-white text-[10px] w-5 h-5 rounded-full flex items-center justify-center font-bold">
                                                {item.quantity}
                                            </span>
                                        </div>
                                        <span className="text-sm font-medium w-32 truncate">{item.name}</span>
                                    </div>
                                    <span className="text-sm text-gray-600">${(item.price * item.quantity).toFixed(2)}</span>
                                </li>
                            ))}
                        </ul>

                        <div className="space-y-3 pt-4 border-t border-gray-100 text-sm">
                            <div className="flex justify-between text-gray-600">
                                <span>Subtotal</span>
                                <span>${totalPrice.toFixed(2)}</span>
                            </div>
                            <div className="flex justify-between text-gray-600">
                                <span>Shipping</span>
                                <span>$5.00</span>
                            </div>
                            <div className="flex justify-between text-brand-dark font-medium text-lg pt-4">
                                <span>Total</span>
                                <span>${(totalPrice + 5).toFixed(2)}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Checkout;
