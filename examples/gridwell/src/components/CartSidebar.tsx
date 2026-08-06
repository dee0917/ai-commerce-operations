import { X, Trash2, Plus, Minus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../hooks/useCart';

interface CartSidebarProps {
    isOpen: boolean;
    onClose: () => void;
}

const CartSidebar: React.FC<CartSidebarProps> = ({ isOpen, onClose }) => {
    const { items, removeItem, updateQuantity, totalPrice } = useCart();
    const navigate = useNavigate();

    if (!isOpen) return null;

    const handleCheckout = () => {
        onClose();
        navigate('/checkout');
    };

    return (
        <>
            <div
                className="fixed inset-0 bg-brand-dark/20 backdrop-blur-sm z-50 transition-opacity"
                onClick={onClose}
                aria-hidden="true"
            />

            <div className="fixed inset-y-0 right-0 max-w-md w-full bg-white shadow-2xl z-50 flex flex-col transform transition-transform duration-300 ease-in-out">
                <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
                    <h2 className="text-xl font-display font-medium">Your Cart</h2>
                    <button onClick={onClose} className="p-2 text-gray-400 hover:text-brand-dark transition-colors">
                        <X className="w-5 h-5" />
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto p-6">
                    {items.length === 0 ? (
                        <div className="flex flex-col items-center justify-center h-full text-center space-y-4">
                            <div className="w-16 h-16 bg-brand-light rounded-full flex items-center justify-center text-gray-400">
                                <X className="w-8 h-8" />
                            </div>
                            <p className="text-gray-500">Your cart is perfectly clean.<br />Let's add some organization.</p>
                            <button
                                onClick={onClose}
                                className="text-brand-accent hover:text-brand-dark font-medium transition-colors"
                            >
                                Continue Shopping
                            </button>
                        </div>
                    ) : (
                        <ul className="space-y-6">
                            {items.map((item) => (
                                <li key={item.id} className="flex gap-4">
                                    <div className="w-24 h-24 bg-brand-light rounded-2xl flex-shrink-0 flex items-center justify-center p-2">
                                        <img src={item.image} alt={item.name} className="max-w-full max-h-full object-contain mix-blend-multiply" />
                                    </div>

                                    <div className="flex-1 flex flex-col">
                                        <div className="flex justify-between items-start">
                                            <h3 className="text-sm font-medium text-brand-dark line-clamp-2 pr-4">{item.name}</h3>
                                            <button
                                                onClick={() => removeItem(item.id)}
                                                className="text-gray-400 hover:text-red-500 transition-colors"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </button>
                                        </div>

                                        <div className="mt-auto flex items-center justify-between">
                                            <div className="flex items-center border border-gray-200 rounded-lg">
                                                <button
                                                    onClick={() => updateQuantity(item.id, item.quantity - 1)}
                                                    className="px-2 py-1 text-gray-500 hover:text-brand-dark disabled:opacity-50"
                                                    disabled={item.quantity <= 1}
                                                >
                                                    <Minus className="w-3 h-3" />
                                                </button>
                                                <span className="text-sm font-medium w-6 text-center">{item.quantity}</span>
                                                <button
                                                    onClick={() => updateQuantity(item.id, item.quantity + 1)}
                                                    className="px-2 py-1 text-gray-500 hover:text-brand-dark"
                                                >
                                                    <Plus className="w-3 h-3" />
                                                </button>
                                            </div>

                                            <span className="font-medium text-brand-dark">${(item.price * item.quantity).toFixed(2)}</span>
                                        </div>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>

                {items.length > 0 && (
                    <div className="border-t border-gray-100 p-6 bg-brand-light">
                        <div className="flex justify-between items-center mb-4">
                            <span className="text-gray-500">Subtotal</span>
                            <span className="text-xl font-display font-medium text-brand-dark">${totalPrice.toFixed(2)}</span>
                        </div>
                        <button
                            onClick={handleCheckout}
                            className="w-full bg-brand-dark text-white py-4 rounded-2xl font-medium hover:bg-black transition-colors"
                        >
                            Proceed to Checkout
                        </button>
                    </div>
                )}
            </div>
        </>
    );
};

export default CartSidebar;
