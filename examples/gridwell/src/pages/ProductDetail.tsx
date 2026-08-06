import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { ArrowLeft, ShoppingBag, Truck, ShieldCheck, RefreshCcw } from 'lucide-react';
import { fetchProductById, Product } from '../services/api';
import { useCart } from '../hooks/useCart';

const ProductDetail = () => {
    const { id } = useParams<{ id: string }>();
    const [product, setProduct] = useState<Product | null>(null);
    const [loading, setLoading] = useState(true);
    const { addItem } = useCart();

    useEffect(() => {
        const loadProduct = async () => {
            if (!id) return;
            const data = await fetchProductById(id);
            setProduct(data || null);
            setLoading(false);
        };
        loadProduct();
    }, [id]);

    if (loading) {
        return (
            <div className="max-w-7xl mx-auto px-4 py-12 flex h-[60vh] items-center justify-center">
                <div className="w-12 h-12 border-4 border-brand-light border-t-brand-dark rounded-full animate-spin"></div>
            </div>
        );
    }

    if (!product) {
        return (
            <div className="max-w-7xl mx-auto px-4 py-24 text-center">
                <h1 className="text-3xl font-display font-medium text-brand-dark mb-4">Product Not Found</h1>
                <p className="text-gray-500 mb-8">The item you are looking for has been moved or doesn't exist.</p>
                <Link to="/shop" className="text-brand-dark font-medium underline">Return to Shop</Link>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <Helmet>
                <title>{product.name} | Gridwell</title>
                <meta name="description" content={product.description} />
                {/* Dynamic Schema.org SEO for Product as required */}
                <script type="application/ld+json">
                    {JSON.stringify({
                        "@context": "https://schema.org/",
                        "@type": "Product",
                        "name": product.name,
                        "image": [product.image],
                        "description": product.description,
                        "sku": `GW-${product.id}`,
                        "offers": {
                            "@type": "Offer",
                            "url": `https://sg-gridwell.vercel.app/product/${product.id}`,
                            "priceCurrency": "USD",
                            "price": product.price,
                            "itemCondition": "https://schema.org/NewCondition",
                            "availability": "https://schema.org/InStock"
                        }
                    })}
                </script>
            </Helmet>

            <Link
                to="/shop"
                className="inline-flex items-center text-sm font-medium text-gray-500 hover:text-brand-dark transition-colors mb-12"
            >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to all items
            </Link>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 lg:gap-16 items-start">
                {/* Product image, single, large, no void */}
                <div className="bento-card bg-gray-50 lg:sticky lg:top-24 aspect-[4/5] overflow-hidden">
                    <img
                        src={product.image}
                        alt={product.name}
                        className="w-full h-full object-cover"
                    />
                </div>

                {/* Product Info — top-aligned, evenly spaced, no center float */}
                <div className="flex flex-col">
                    <span className="text-xs tracking-widest text-brand-accent uppercase mb-3 block font-medium">{product.category}</span>
                    <h1 className="text-3xl md:text-4xl lg:text-5xl font-display font-medium text-brand-dark tracking-tight mb-4 leading-[1.1]">
                        {product.name}
                    </h1>
                    <p className="text-2xl font-medium text-gray-900 mb-6">${product.price.toFixed(2)}</p>
                    <p className="text-gray-600 leading-relaxed text-lg mb-8 max-w-[52ch]">
                        {product.description}
                    </p>

                    <button
                        onClick={() => addItem(product)}
                        className="w-full bg-brand-dark text-white hover:bg-black active:scale-[0.99] transition-all px-10 py-4 rounded-xl flex items-center justify-center gap-2 font-medium text-lg shadow-md hover:shadow-xl"
                    >
                        <ShoppingBag className="w-5 h-5" />
                        Add to Bag
                    </button>

                    {/* Material / what's-in-it detail, fills the column so there is no void */}
                    <div className="mt-10 space-y-px rounded-2xl overflow-hidden border border-gray-100">
                        {[
                            ['Material', 'Premium, built to last'],
                            ['Ships in', '1 to 2 business days'],
                            ['Category', product.category],
                            ['SKU', `GW-${product.id}`],
                        ].map(([label, value]) => (
                            <div key={label} className="flex justify-between items-center bg-white px-5 py-3.5 text-sm">
                                <span className="text-gray-500">{label}</span>
                                <span className="text-brand-dark font-medium">{value}</span>
                            </div>
                        ))}
                    </div>

                    {/* Trust row — labeled, inline, balanced */}
                    <div className="grid grid-cols-3 gap-3 mt-8 pt-8 border-t border-gray-100">
                        {[
                            [<Truck className="w-5 h-5" />, 'Free Shipping', 'Over $50'],
                            [<RefreshCcw className="w-5 h-5" />, 'Easy Returns', '30-day window'],
                            [<ShieldCheck className="w-5 h-5" />, 'Warranty', 'Lifetime cover'],
                        ].map(([icon, title, sub], i) => (
                            <div key={i} className="flex flex-col items-center text-center gap-2">
                                <div className="w-11 h-11 bg-brand-light rounded-full flex items-center justify-center text-brand-dark">
                                    {icon}
                                </div>
                                <div>
                                    <h4 className="font-medium text-sm leading-tight">{title}</h4>
                                    <p className="text-xs text-gray-500 mt-0.5">{sub}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProductDetail;
