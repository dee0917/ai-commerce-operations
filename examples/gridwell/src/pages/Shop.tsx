import { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet-async';
import ProductCard from '../components/ProductCard';
import { fetchProducts, Product } from '../services/api';

const Shop = () => {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadProducts = async () => {
            const data = await fetchProducts();
            setProducts(data);
            setLoading(false);
        };
        loadProducts();
    }, []);

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <Helmet>
                <title>Shop All Collection | Gridwell</title>
                <meta name="description" content="Explore Gridwell's complete collection of minimalist storage solutions." />
            </Helmet>

            <div className="mb-12 border-b border-gray-100 pb-8">
                <h1 className="text-4xl font-display font-medium text-brand-dark mb-4">All Storage Solutions</h1>
                <p className="text-gray-500 max-w-2xl text-lg">Every object has its place. Discover our premium materials and architectural forms designed to seamlessly integrate into your space.</p>
            </div>

            {loading ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {Array.from({ length: 8 }).map((_, i) => (
                        <div key={i} className="bento-card h-80 animate-pulse bg-gray-200"></div>
                    ))}
                </div>
            ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 auto-rows-fr">
                    {products.map(product => (
                        <ProductCard key={product.id} product={product} />
                    ))}
                </div>
            )}
        </div>
    );
};

export default Shop;
