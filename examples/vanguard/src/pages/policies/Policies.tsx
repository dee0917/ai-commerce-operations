import React from 'react';

interface PolicyTemplateProps {
    title: string;
    lastUpdated?: string;
    children: React.ReactNode;
}

const PolicyTemplate: React.FC<PolicyTemplateProps> = ({ title, lastUpdated = 'MARCH 2026', children }) => (
    <div className="bg-vanguard-obsidian min-h-screen py-20 px-4">
        <div className="max-w-3xl mx-auto">
            <div className="mb-12">
                <div className="font-mono text-vanguard-red text-[10px] font-bold tracking-[0.4em] uppercase mb-4">Protocol Document</div>
                <h1 className="text-4xl font-black text-white uppercase tracking-tighter mb-4">{title}</h1>
                <div className="font-mono text-[9px] text-slate-500 uppercase tracking-widest">Last Modified: {lastUpdated}</div>
            </div>

            <div className="prose prose-invert prose-slate max-w-none font-sans text-slate-400 leading-relaxed space-y-8">
                {children}
            </div>

            <div className="mt-20 pt-10 border-t border-vanguard-slate/10 font-mono text-[10px] text-slate-600 uppercase">
                © VANGUARD GEAR // ENCRYPTED POLICY DATA // END OF FILE
            </div>
        </div>
    </div>
);

export const PrivacyPolicy: React.FC = () => (
    <PolicyTemplate title="Privacy Protocol">
        <section>
            <h2 className="text-white font-mono text-lg font-bold uppercase mb-4">1. Data Encryption</h2>
            <p>All communication within the Vanguard platform is processed through high-level encryption protocols. Your identity as an operative is protected by multiple layers of security.</p>
        </section>
        <section>
            <h2 className="text-white font-mono text-lg font-bold uppercase mb-4">2. Mission Logs</h2>
            <p>We retain transaction mission logs only for the duration required to ensure successful logistics deployment. No trace of your operational gear list is stored beyond the mission lifecycle without consent.</p>
        </section>
        <section>
            <h2 className="text-white font-mono text-lg font-bold uppercase mb-4">3. Counter-Surveillance</h2>
            <p>Our systems ignore all standard tracking beacons. We do not participate in commercial data harvesting networks.</p>
        </section>
    </PolicyTemplate>
);

export const TermsOfService: React.FC = () => (
    <PolicyTemplate title="Terms of Engagement">
        <section>
            <h2 className="text-white font-mono text-lg font-bold uppercase mb-4">1. Deployment of Gear</h2>
            <p>By initializing a purchase, you agree to these terms of engagement. Vanguard is not responsible for misuse of tactical hardware beyond its intended functional scope.</p>
        </section>
        <section>
            <h2 className="text-white font-mono text-lg font-bold uppercase mb-4">2. Modification Rights</h2>
            <p>We reserve the right to modify gear specifications to ensure peak operational readiness. Prices are subject to tactical adjustment based on material availability.</p>
        </section>
    </PolicyTemplate>
);

export const ShippingPolicy: React.FC = () => (
    <PolicyTemplate title="Logistics & Dispatch">
        <section>
            <h2 className="text-white font-mono text-lg font-bold uppercase mb-4">1. Secure Dispatch</h2>
            <p>All units are dispatched via secure logistics channels. Tracking IDs are encrypted and provided once the drop has been initialized.</p>
        </section>
        <section>
            <h2 className="text-white font-mono text-lg font-bold uppercase mb-4">2. Field Returns</h2>
            <p>Gear may be returned for refurbishment within 30 solar days if the equipment shows signs of manufacturing failure. Normal field wear is not grounds for return.</p>
        </section>
    </PolicyTemplate>
);
