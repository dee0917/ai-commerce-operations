import React from 'react';
import { Link } from 'react-router-dom';
import { ShoppingBag } from 'lucide-react';
import { Product } from '../services/api';
import { useCart } from '../hooks/useCart';

interface ProductCardProps {
    product: Product;
    featured?: boolean;
}

const ProductCard: React.FC<ProductCardProps> = ({ product, featured = false }) => {
    const { addItem } = useCart();

    const handleAddToCart = (e: React.MouseEvent) => {
        e.preventDefault(); // prevent navigation when clicking button inside Link
        addItem(product);
    };

    return (
        <Link
            to={`/product/${product.id}`}
            className={`group bento-card bento-hover flex flex-col ${featured ? 'md:col-span-2 md:row-span-2' : ''}`}
        >
            <div className={`relative bg-gray-50 flex items-center justify-center p-6 ${featured ? 'h-80 md:h-[400px]' : 'h-64'}`}>
                <img
                    src={product.image}
                    alt={product.name}
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                    loading={featured ? "eager" : "lazy"}
                />
                <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm px-2.5 py-1 text-xs font-sans font-medium text-brand-dark" style={{ borderRadius: '4px' }}>
                    ${product.price.toFixed(2)}
                </div>
            </div>

            <div className="p-5 flex flex-col flex-grow justify-between border-t border-gray-50">
                <div>
                    <h3 className="font-display font-medium text-lg leading-tight mb-1">{product.name}</h3>
                    <p className="text-gray-500 text-sm line-clamp-2 mt-2">{product.description}</p>
                </div>

                <button
                    onClick={handleAddToCart}
                    className="mt-4 w-full flex items-center justify-center gap-2 bg-brand-dark hover:bg-brand-accent text-white py-2.5 font-sans font-medium text-sm transition-colors"
                    style={{ borderRadius: '8px' }}
                >
                    <ShoppingBag className="w-4 h-4" />
                    Add to Cart
                </button>
            </div>
        </Link>
    );
};

export default ProductCard;
