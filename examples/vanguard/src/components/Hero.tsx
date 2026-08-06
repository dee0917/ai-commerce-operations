import React from 'react';
import { ArrowDownRight } from 'lucide-react';
import { motion } from 'framer-motion';

export const Hero: React.FC = () => {
    const heroImageUrl = "/images/hero-banner.png";

    return (
        <section className="relative min-h-[85vh] flex items-center overflow-hidden bg-vanguard-obsidian border-b border-vanguard-slate/20">
            {/* Background Graphic Elements */}
            <div className="absolute inset-0 z-0 opacity-10 pointer-events-none">
                <div className="absolute top-0 right-0 w-[500px] h-[500px] border border-vanguard-red/30 rounded-full -translate-y-1/2 translate-x-1/2" />
                <div className="absolute bottom-0 left-0 w-[800px] h-px bg-gradient-to-r from-transparent via-vanguard-red to-transparent" />
                <div className="absolute inset-0" style={{ backgroundImage: 'radial-gradient(#ffffff05 1px, transparent 1px)', backgroundSize: '40px 40px' }} />
            </div>

            <div className="grid lg:grid-cols-2 w-full max-w-[1800px] mx-auto z-10">
                {/* Left: Text Content */}
                <div className="flex flex-col justify-center px-8 lg:px-20 py-20 lg:py-0 order-2 lg:order-1">
                    <div className="mb-6 flex items-center gap-3">
                        <div className="h-px w-12 bg-vanguard-red" />
                        <span className="font-mono text-vanguard-red text-xs font-bold tracking-[0.3em] uppercase">Vanguard Mission Control</span>
                    </div>

                    <h1 className="text-5xl md:text-7xl lg:text-8xl font-black mb-8 leading-[0.9] text-white">
                        MASTER YOUR <br />
                        <span className="text-vanguard-red underline decoration-4 underline-offset-8">EVERYDAY</span> MISSION.
                    </h1>

                    <p className="text-slate-400 max-w-lg mb-12 text-sm md:text-base leading-relaxed">
                        Precision-engineered kits for the modern minimalist. Tactical efficiency meets aerospace craftsmanship. Curated for those who demand performance in every carry.
                    </p>

                    <div className="flex flex-col sm:flex-row gap-6">
                        <button className="btn-tactical flex items-center gap-3">
                            Deploy Your Kit
                            <ArrowDownRight size={20} />
                        </button>
                        <button className="font-mono text-xs uppercase tracking-widest border border-vanguard-slate/30 px-8 py-3 hover:bg-white hover:text-black transition-all">
                            View Database
                        </button>
                    </div>

                    <div className="mt-20 grid grid-cols-3 gap-8">
                        <div>
                            <div className="font-mono text-xl font-bold text-white">12</div>
                            <div className="font-mono text-[9px] uppercase tracking-widest text-slate-500">Core Tools</div>
                        </div>
                        <div className="border-l border-vanguard-slate/20 pl-8">
                            <div className="font-mono text-xl font-bold text-white">0.01mm</div>
                            <div className="font-mono text-[9px] uppercase tracking-widest text-slate-500">Precision Tolerance</div>
                        </div>
                        <div className="border-l border-vanguard-slate/20 pl-8">
                            <div className="font-mono text-xl font-bold text-white">∞</div>
                            <div className="font-mono text-[9px] uppercase tracking-widest text-slate-500">Lifetime Support</div>
                        </div>
                    </div>
                </div>

                {/* Right: Visual Section */}
                <div className="relative order-1 lg:order-2 h-[50vh] lg:h-auto overflow-hidden flex items-center justify-center">
                    <div className="absolute inset-0 bg-gradient-to-r from-vanguard-obsidian to-transparent z-10 hidden lg:block" />
                    <motion.div
                        initial={{ scale: 1.1, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ duration: 1.5, ease: 'easeOut' }}
                        className="w-full h-full"
                    >
                        <img
                            src={heroImageUrl}
                            alt="Vanguard EDC Collection"
                            className="w-full h-full object-cover grayscale-[20%] contrast-125"
                            loading="eager"
                        />
                    </motion.div>

                    {/* Functional Overlay Graphic */}
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[80%] aspect-square border border-white/5 pointer-events-none rounded-full" />
                    <div className="absolute bottom-10 right-10 z-20 hidden md:block">
                        <div className="bg-black/40 backdrop-blur-md p-4 border border-white/10 font-mono text-[10px] space-y-1">
                            <div className="flex gap-4">
                                <span className="text-slate-500">COORD:</span>
                                <span className="text-white">35.6895° N, 139.6917° E</span>
                            </div>
                            <div className="flex gap-4">
                                <span className="text-slate-500">STATUS:</span>
                                <span className="text-vanguard-red">OPERATIONAL</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};
