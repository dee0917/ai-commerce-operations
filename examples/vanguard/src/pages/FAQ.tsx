import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, Mail, Clock, ShieldCheck, ChevronRight } from 'lucide-react';
import { clsx } from 'clsx';

interface QA {
    q: string;
    a: string;
}

const faqData: QA[] = [
    {
        q: "When will my gear be dispatched?",
        a: "Most mission-ready gear ships within 24 to 48 hours of order confirmation. Limited drops are built to order and may require additional logistical prep time, noted on the product page.",
    },
    {
        q: "How do I track my order?",
        a: "Once your kit leaves the depot you receive a tracking ID by email. Every shipment is insured and routed through our standard secure logistics partner.",
    },
    {
        q: "What does aerospace-grade titanium mean?",
        a: "We primarily machine Grade 5 (Ti-6Al-4V) titanium for its superior strength-to-weight ratio, corrosion resistance, and natural bio-compatibility. It is the same alloy class used in airframe and surgical hardware.",
    },
    {
        q: "Is the carbon fiber real?",
        a: "Yes. We use genuine 3K twill carbon fiber sourced from certified suppliers, layered and pressure-cured rather than the printed film finish found on cheaper EDC.",
    },
    {
        q: "What does the lifetime guarantee cover?",
        a: "We stand behind the hardware. If your gear fails from a structural manufacturing defect, we repair or replace it at no cost. Normal wear, loss, and abuse outside intended use are not covered.",
    },
    {
        q: "Can I return field-tested gear?",
        a: "Returns are accepted in pristine, un-deployed condition within 30 days of delivery. Once gear has been carried or used it is considered in the field and is non-returnable unless it arrived defective.",
    },
];

const helpfulLinks = [
    { label: "Size & Dimensions", to: "/size-guide" },
    { label: "Shipping & Logistics", to: "/policies/shipping" },
    { label: "Returns & Warranty", to: "/policies/terms" },
    { label: "Mission History", to: "/mission-history" },
];

export const FAQ: React.FC = () => {
    const [open, setOpen] = useState<number>(0);

    return (
        <div className="bg-vanguard-obsidian min-h-screen">
            {/* Page header band */}
            <div className="border-b border-vanguard-slate/20 bg-vanguard-industrial/40">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-20">
                    <div className="flex items-center gap-3 mb-5">
                        <div className="h-px w-10 bg-vanguard-red" />
                        <span className="font-mono text-vanguard-red text-[10px] font-bold tracking-[0.4em] uppercase">Field Manual</span>
                    </div>
                    <h1 className="text-5xl md:text-7xl font-black text-white uppercase tracking-tighter">Support &amp; FAQ</h1>
                    <p className="text-slate-400 mt-5 max-w-xl text-sm md:text-base leading-relaxed">
                        Operational answers on dispatch, materials, and warranty. If something is not covered here, our team responds direct.
                    </p>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24 grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16">
                {/* Left: sticky support panel */}
                <aside className="lg:col-span-4">
                    <div className="lg:sticky lg:top-28 space-y-6">
                        <div className="border border-vanguard-slate/20 bg-vanguard-industrial/50 p-7">
                            <h2 className="font-mono text-xs font-bold text-white uppercase tracking-[0.25em] mb-6 pb-4 border-b border-vanguard-slate/15">
                                Tactical Support
                            </h2>
                            <ul className="space-y-6">
                                <li className="flex gap-4">
                                    <Mail size={18} className="text-vanguard-red shrink-0 mt-0.5" />
                                    <div>
                                        <div className="font-mono text-[9px] uppercase tracking-widest text-slate-500 mb-1">Comm Channel</div>
                                        <a href="mailto:support@vanguardgear.co" className="text-sm text-white hover:text-vanguard-red transition-colors break-all">
                                            support@vanguardgear.co
                                        </a>
                                    </div>
                                </li>
                                <li className="flex gap-4">
                                    <Clock size={18} className="text-vanguard-red shrink-0 mt-0.5" />
                                    <div>
                                        <div className="font-mono text-[9px] uppercase tracking-widest text-slate-500 mb-1">Operating Hours</div>
                                        <div className="text-sm text-slate-300">Mon to Fri, 09:00 to 18:00 SGT</div>
                                        <div className="text-[11px] text-slate-500 mt-0.5">Replies within one business day</div>
                                    </div>
                                </li>
                                <li className="flex gap-4">
                                    <ShieldCheck size={18} className="text-vanguard-red shrink-0 mt-0.5" />
                                    <div>
                                        <div className="font-mono text-[9px] uppercase tracking-widest text-slate-500 mb-1">Secure Checkout</div>
                                        <div className="text-sm text-slate-300">Encrypted payment, insured dispatch</div>
                                    </div>
                                </li>
                            </ul>
                        </div>

                        <div className="border border-vanguard-slate/20 bg-vanguard-industrial/50 p-7">
                            <h3 className="font-mono text-[10px] font-bold text-white uppercase tracking-[0.25em] mb-5">
                                Helpful Links
                            </h3>
                            <ul className="divide-y divide-vanguard-slate/15">
                                {helpfulLinks.map((link) => (
                                    <li key={link.to}>
                                        <Link
                                            to={link.to}
                                            className="flex items-center justify-between py-3 group"
                                        >
                                            <span className="font-mono text-[11px] uppercase tracking-widest text-slate-400 group-hover:text-white transition-colors">
                                                {link.label}
                                            </span>
                                            <ChevronRight size={14} className="text-slate-600 group-hover:text-vanguard-red group-hover:translate-x-1 transition-all" />
                                        </Link>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </aside>

                {/* Right: accordion */}
                <div className="lg:col-span-8">
                    <div className="border-t border-vanguard-slate/20">
                        {faqData.map((item, i) => {
                            const isOpen = open === i;
                            return (
                                <div key={i} className="border-b border-vanguard-slate/20">
                                    <button
                                        onClick={() => setOpen(isOpen ? -1 : i)}
                                        className="w-full flex items-start justify-between gap-6 py-7 text-left group"
                                        aria-expanded={isOpen}
                                    >
                                        <span className="flex gap-5">
                                            <span className="font-mono text-[11px] text-vanguard-red pt-1 tabular-nums">
                                                {String(i + 1).padStart(2, '0')}
                                            </span>
                                            <span className={clsx(
                                                "text-lg md:text-xl font-bold uppercase tracking-tight transition-colors",
                                                isOpen ? "text-white" : "text-slate-300 group-hover:text-white"
                                            )}>
                                                {item.q}
                                            </span>
                                        </span>
                                        <Plus
                                            size={20}
                                            className={clsx(
                                                "shrink-0 mt-1 transition-all duration-300",
                                                isOpen ? "rotate-45 text-vanguard-red" : "text-slate-500 group-hover:text-white"
                                            )}
                                        />
                                    </button>
                                    <div
                                        className={clsx(
                                            "grid transition-all duration-300 ease-out",
                                            isOpen ? "grid-rows-[1fr] opacity-100" : "grid-rows-[0fr] opacity-0"
                                        )}
                                    >
                                        <div className="overflow-hidden">
                                            <p className="text-slate-400 leading-relaxed text-sm md:text-base pb-8 pl-10 max-w-[60ch]">
                                                {item.a}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>

                    <div className="mt-14 p-8 md:p-10 bg-vanguard-industrial border border-vanguard-slate/15 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
                        <div>
                            <h4 className="text-white font-mono text-base font-bold uppercase tracking-tight mb-2">Still in the dark?</h4>
                            <p className="text-slate-500 text-sm">Our support team handles every message direct, no bots.</p>
                        </div>
                        <a href="mailto:support@vanguardgear.co" className="btn-tactical shrink-0 whitespace-nowrap">
                            Contact Support
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
};
