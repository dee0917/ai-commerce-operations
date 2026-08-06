import { useState } from 'react';
import { Helmet } from 'react-helmet-async';
import { Link } from 'react-router-dom';
import { Plus, Minus, Mail, Clock, ShieldCheck, ArrowRight } from 'lucide-react';

const faqs = [
    {
        q: 'How long does shipping take?',
        a: 'Orders ship within 1 to 2 business days. Standard delivery lands in 3 to 5 business days, and shipping is free on every order over $50. You will get a tracking link by email the moment your parcel leaves us.',
    },
    {
        q: 'What is your return policy?',
        a: 'You have a 30-day window from delivery to return anything that did not earn its place in your home. Items should be unused and in their original packaging. Start a return from your order email and we cover the return label.',
    },
    {
        q: 'Are the materials durable?',
        a: 'Every piece is made from premium materials chosen to last: matte tinplate, food-safe silicone, water-resistant fabrics, and full-grain leather. Hardware-class products carry our lifetime warranty against manufacturing defects.',
    },
    {
        q: 'Do the products come fully assembled?',
        a: 'Yes. Gridwell organizers arrive ready to use straight out of the box. Nothing needs tools, screws, or guesswork. Unpack it, place it, and the space sorts itself.',
    },
    {
        q: 'How do I clean and care for my organizers?',
        a: 'Most pieces wipe clean with a damp cloth and mild soap. Silicone ties and mesh pouches are fully washable. Avoid harsh solvents on leather and tinplate so the finish keeps its calm, matte character.',
    },
    {
        q: 'Can I track my order after it ships?',
        a: 'Of course. As soon as your order is dispatched we send a tracking number to the email on your order. You can follow each step from our warehouse to your door.',
    },
    {
        q: 'Which payment methods do you accept?',
        a: 'We accept all major cards and common digital wallets at a secure, SSL-encrypted checkout. Your payment details are never stored on our servers.',
    },
    {
        q: 'Do you ship internationally?',
        a: 'We currently ship across the region with calculated rates shown at checkout before you pay. International coverage is expanding, so check your address at checkout for the latest options.',
    },
];

const FAQItem = ({ item, isOpen, onToggle }: { item: typeof faqs[0]; isOpen: boolean; onToggle: () => void }) => (
    <div className="border-b border-gray-100 last:border-b-0">
        <button
            onClick={onToggle}
            className="w-full flex items-center justify-between gap-4 py-5 text-left group"
            aria-expanded={isOpen}
        >
            <span className="font-display font-medium text-base md:text-lg text-brand-dark group-hover:text-brand-accent transition-colors">
                {item.q}
            </span>
            <span className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-light flex items-center justify-center text-brand-dark">
                {isOpen ? <Minus className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
            </span>
        </button>
        <div className={`grid transition-all duration-300 ease-out ${isOpen ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0'}`}>
            <div className="overflow-hidden">
                <p className="text-gray-600 leading-relaxed pb-6 pr-12 max-w-[60ch]">{item.a}</p>
            </div>
        </div>
    </div>
);

const FAQ = () => {
    const [openIndex, setOpenIndex] = useState<number | null>(0);

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16">
            <Helmet>
                <title>Help & FAQ | Gridwell</title>
                <meta name="description" content="Answers on shipping, returns, materials, and care for Gridwell storage and organization products." />
            </Helmet>

            <div className="mb-12 md:mb-16">
                <h1 className="text-4xl md:text-5xl font-display font-medium text-brand-dark tracking-tight mb-4 leading-[1.1]">
                    Help & FAQ
                </h1>
                <p className="text-gray-500 text-lg max-w-2xl">
                    Everything you need to know about ordering, shipping, and caring for your Gridwell pieces. Still stuck? We are a short message away.
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-10 lg:gap-16 items-start">
                {/* Left sticky support panel */}
                <aside className="lg:col-span-1 lg:sticky lg:top-24">
                    <div className="bento-card p-7">
                        <h2 className="font-display font-medium text-xl text-brand-dark mb-1">Need a hand?</h2>
                        <p className="text-gray-500 text-sm mb-6">Real people, calm answers.</p>

                        <div className="space-y-5">
                            <div className="flex items-start gap-3">
                                <div className="w-9 h-9 rounded-full bg-brand-light flex items-center justify-center text-brand-dark flex-shrink-0">
                                    <Mail className="w-4 h-4" />
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-brand-dark">Email us</p>
                                    <a href="mailto:hello@gridwell.co" className="text-sm text-brand-accent hover:underline">hello@gridwell.co</a>
                                </div>
                            </div>

                            <div className="flex items-start gap-3">
                                <div className="w-9 h-9 rounded-full bg-brand-light flex items-center justify-center text-brand-dark flex-shrink-0">
                                    <Clock className="w-4 h-4" />
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-brand-dark">Support hours</p>
                                    <p className="text-sm text-gray-500">Mon to Fri, 9am to 6pm</p>
                                </div>
                            </div>

                            <div className="flex items-start gap-3">
                                <div className="w-9 h-9 rounded-full bg-brand-light flex items-center justify-center text-brand-dark flex-shrink-0">
                                    <ShieldCheck className="w-4 h-4" />
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-brand-dark">Secure checkout</p>
                                    <p className="text-sm text-gray-500">256-bit SSL encrypted</p>
                                </div>
                            </div>
                        </div>

                        <div className="mt-7 pt-6 border-t border-gray-100">
                            <p className="text-xs font-medium uppercase tracking-wider text-gray-400 mb-3">Helpful links</p>
                            <div className="space-y-2.5">
                                <Link to="/shop" className="flex items-center justify-between text-sm text-brand-dark hover:text-brand-accent transition-colors group">
                                    Browse all storage <ArrowRight className="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 transition-opacity" />
                                </Link>
                                <Link to="/" className="flex items-center justify-between text-sm text-brand-dark hover:text-brand-accent transition-colors group">
                                    Back to home <ArrowRight className="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 transition-opacity" />
                                </Link>
                            </div>
                        </div>
                    </div>
                </aside>

                {/* Right accordion */}
                <div className="lg:col-span-2">
                    <div className="bento-card px-6 md:px-8 py-2">
                        {faqs.map((item, i) => (
                            <FAQItem
                                key={i}
                                item={item}
                                isOpen={openIndex === i}
                                onToggle={() => setOpenIndex(openIndex === i ? null : i)}
                            />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default FAQ;
