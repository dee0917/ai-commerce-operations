import { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet-async';
import { ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import ProductCard from '../components/ProductCard';
import { fetchProducts, Product } from '../services/api';

const Home = () => {
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
        <div className="bg-brand-light min-h-screen pb-20">
            <Helmet>
                <title>Gridwell | Storage with the geometry of calm.</title>
                <meta name="description" content="Premium storage and home-organization systems. Gridwell brings structural order to every corner of your home." />
            </Helmet>

            {/* ─── HERO BENTO ─── */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-10 pb-6">
                <div className="grid grid-cols-1 md:grid-cols-12 gap-4 md:gap-5 auto-rows-auto">

                    {/* LEFT: main hero cell — 7 of 12 columns, tall */}
                    <div
                        className="md:col-span-7 md:row-span-2 relative rounded-2xl overflow-hidden min-h-[480px] md:min-h-[580px] flex flex-col justify-end"
                        style={{ border: '1px solid rgba(27,46,34,0.10)' }}
                    >
                        {/* Background: real hero photo */}
                        <img
                            src="/images/hero-gridwell.jpg"
                            alt="Japandi storage shelves with ceramic vessels"
                            className="absolute inset-0 w-full h-full object-cover"
                            loading="eager"
                        />

                        {/* Scrim: left-to-right gradient so text is legible */}
                        <div className="hero-scrim absolute inset-0" />

                        {/* Text content — anchored to bottom-left */}
                        <div className="relative z-10 p-8 md:p-12 pb-10">
                            {/* Category label — ONE eyebrow, restrained */}
                            <p
                                className="text-xs font-sans font-medium tracking-[0.18em] uppercase text-white/60 mb-5"
                                style={{ letterSpacing: '0.18em' }}
                            >
                                Home Organization
                            </p>

                            {/* Headline: DM Serif Display, italic emphasis on one word */}
                            <h1 className="font-display text-4xl md:text-5xl lg:text-6xl leading-[1.05] text-white mb-5 max-w-sm">
                                Storage with the{' '}
                                <em className="not-italic italic" style={{ paddingBottom: '0.1em', display: 'inline-block' }}>
                                    geometry
                                </em>{' '}
                                of calm.
                            </h1>

                            {/* Subtext: 16 words, concrete */}
                            <p className="text-white/70 text-base md:text-lg leading-relaxed mb-8 max-w-xs font-sans font-light">
                                Considered organizers that hold their shape and their place, season after season.
                            </p>

                            {/* Primary CTA: high contrast white bg / dark text */}
                            <Link
                                to="/shop"
                                className="inline-flex items-center gap-2 bg-white text-brand-dark px-6 py-3 font-sans font-medium text-sm hover:bg-brand-light transition-colors"
                                style={{ borderRadius: '8px' }}
                            >
                                Shop the Grid
                                <ArrowRight className="w-4 h-4" />
                            </Link>
                        </div>
                    </div>

                    {/* RIGHT COLUMN: 5 of 12 columns, two cells stacked */}
                    {loading ? (
                        <>
                            <div className="md:col-span-5 h-64 md:h-auto animate-pulse bg-brand-surface rounded-2xl" style={{ minHeight: '280px', border: '1px solid rgba(27,46,34,0.08)' }} />
                            <div className="md:col-span-5 h-64 md:h-auto animate-pulse bg-brand-surface rounded-2xl" style={{ border: '1px solid rgba(27,46,34,0.08)' }} />
                        </>
                    ) : (
                        <>
                            {/* TOP-RIGHT: Featured product — tall */}
                            <div className="md:col-span-5">
                                <ProductCard product={products[1]} featured={false} />
                            </div>

                            {/* BOTTOM-RIGHT: two small cells side-by-side */}
                            <div className="md:col-span-5 grid grid-cols-2 gap-4 md:gap-5">
                                <ProductCard product={products[0]} />
                                <ProductCard product={products[2]} />
                            </div>
                        </>
                    )}
                </div>
            </section>

            {/* ─── THE ART OF ORGANIZATION (unchanged structure, new colors only) ─── */}
            <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
                <div className="flex justify-between items-end mb-8">
                    <div>
                        <h2 className="text-2xl md:text-3xl font-display font-normal mb-1.5 text-brand-dark">
                            The Art of Organization
                        </h2>
                        <p className="text-brand-muted text-sm font-sans">Everyday essentials, precisely considered.</p>
                    </div>
                    <Link
                        to="/shop"
                        className="hidden sm:flex text-brand-accent font-sans font-medium text-sm hover:opacity-70 transition-opacity items-center gap-1"
                    >
                        View All <ArrowRight className="w-4 h-4" />
                    </Link>
                </div>

                {loading ? (
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
                        {Array.from({ length: 4 }).map((_, i) => (
                            <div key={i} className="bento-card h-80 animate-pulse bg-brand-surface" />
                        ))}
                    </div>
                ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-5">
                        {products.slice(3, 7).map(product => (
                            <ProductCard key={product.id} product={product} />
                        ))}
                    </div>
                )}
            </section>
        </div>
    );
};

export default Home;
