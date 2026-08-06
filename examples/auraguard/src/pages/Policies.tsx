import React from 'react';

const PolicyLayout: React.FC<{ title: string, children: React.ReactNode }> = ({ title, children }) => (
    <div className="pt-48 pb-32 px-8 max-w-3xl mx-auto min-h-screen">
        <h1 className="text-4xl lg:text-5xl font-display uppercase tracking-[0.2em] font-light mb-12 pb-6 border-b-[0.5px] border-stone-400">
            {title}
        </h1>
        <div className="prose prose-stone prose-lg max-w-none font-light leading-loose text-brand-secondary/90">
            {children}
        </div>
    </div>
);

export const FAQ: React.FC = () => (
    <PolicyLayout title="FAQ">
        <h2>Orders</h2>
        <p><strong>How long does it take to process an order?</strong> 1-3 business days as all pieces are meticulously checked and packed.</p>
        <p><strong>Can I modify my order after placing it?</strong> Yes, within 24 hours of placing the order.</p>

        <h2>Shipping & Returns</h2>
        <p>We ship worldwide. Custom boxes ensure safe travel. You may return unused talismans within 30 days. Customers are responsible for return shipping unless the item arrived defective.</p>

        <h2>Philosophy</h2>
        <p><strong>Are the talismans blessed?</strong> Yes, they are spiritually cleansed and blessed by Master Lin prior to being sent out.</p>
    </PolicyLayout>
);

export const Privacy: React.FC = () => (
    <PolicyLayout title="Privacy Policy">
        <h2>1. Information Collection</h2>
        <p>We hold our craft in high regard, and your trust even higher. We collect essential information such as names, emails, and secure payment details solely to fulfill your orders and enhance your experience.</p>

        <h2>2. Data Security</h2>
        <p>Your details are protected using industry-standard SSL encryption and secure payment gateways. We do not sell or trade your data.</p>
    </PolicyLayout>
);

export const Terms: React.FC = () => (
    <PolicyLayout title="Terms of Service">
        <h2>1. Terms of Sale</h2>
        <p>Upon placing an order with AuraGuard, you accept these terms. All prices are final and products reflect genuine artisanal variations.</p>
        <h2>2. Intellectual Property</h2>
        <p>The designs and written content on this website are the intellectual property of AuraGuard and Master Lin. Re-production without permission is prohibited.</p>
    </PolicyLayout>
);

export const Shipping: React.FC = () => (
    <PolicyLayout title="Shipping Policy">
        <p>Information on worldwide shipping options and times...</p>
    </PolicyLayout>
);

export const Returns: React.FC = () => (
    <PolicyLayout title="Returns Policy">
        <p>Information on our 30-day return policy...</p>
    </PolicyLayout>
);

export const Payment: React.FC = () => (
    <PolicyLayout title="Payment Methods">
        <p>We accept major credit cards and secure payment gateways...</p>
    </PolicyLayout>
);
