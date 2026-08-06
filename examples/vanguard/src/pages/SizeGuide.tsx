import React from 'react';

export const SizeGuide: React.FC = () => {
    return (
        <div className="bg-vanguard-obsidian min-h-screen py-20 px-4">
            <div className="max-w-4xl mx-auto">
                <div className="mb-16 border-b border-vanguard-slate/20 pb-8">
                    <div className="font-mono text-vanguard-red text-xs font-bold tracking-[0.5em] uppercase mb-4">Tactical Measurements</div>
                    <h1 className="text-5xl font-black text-white uppercase tracking-tighter mb-4">Sizing & Dimensions</h1>
                    <p className="text-slate-500 font-mono text-xs uppercase">Precision is our primary objective. High-tolerance gear requires exact fitting.</p>
                </div>

                <div className="space-y-16">
                    {/* Item 1: Pens */}
                    <div className="grid md:grid-cols-3 gap-8">
                        <div className="md:col-span-1">
                            <h2 className="font-mono text-xl font-bold text-white uppercase underline decoration-vanguard-red">Writing Tools</h2>
                        </div>
                        <div className="md:col-span-2 overflow-x-auto">
                            <table className="w-full text-left font-mono text-[11px] text-slate-400">
                                <thead className="text-white uppercase">
                                    <tr className="border-b border-vanguard-slate/20">
                                        <th className="py-4">MODEL</th>
                                        <th className="py-4">LENGTH</th>
                                        <th className="py-4">DIAMETER</th>
                                        <th className="py-4">WEIGHT</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-vanguard-slate/10">
                                    <tr>
                                        <td className="py-4">STINGER BA</td>
                                        <td className="py-4">120MM</td>
                                        <td className="py-4">11MM</td>
                                        <td className="py-4">42G</td>
                                    </tr>
                                    <tr>
                                        <td className="py-4">PHANTOM TI</td>
                                        <td className="py-4">135MM</td>
                                        <td className="py-4">10MM</td>
                                        <td className="py-4">35G</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    {/* Item 2: Wallets */}
                    <div className="grid md:grid-cols-3 gap-8">
                        <div className="md:col-span-1">
                            <h2 className="font-mono text-xl font-bold text-white uppercase underline decoration-vanguard-red">Carry Systems</h2>
                        </div>
                        <div className="md:col-span-2 space-y-8">
                            <div className="p-6 bg-vanguard-industrial border border-vanguard-slate/20">
                                <h3 className="text-white font-mono text-xs font-bold uppercase mb-4">Cipher Series Capacity</h3>
                                <p className="text-sm leading-relaxed mb-4">Designed for the minimal operative. Optimized for 1-12 credit cards and up to 5 bills with the integrated money clip.</p>
                                <div className="grid grid-cols-2 gap-4 font-mono text-[10px] text-slate-500">
                                    <div>FOOTPRINT: 86MM X 54MM</div>
                                    <div>THICKNESS: 6MM (EMPTY)</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Item 3: Pouches */}
                    <div className="grid md:grid-cols-3 gap-8">
                        <div className="md:col-span-1">
                            <h2 className="font-mono text-xl font-bold text-white uppercase underline decoration-vanguard-red">Deployment Pouches</h2>
                        </div>
                        <div className="md:col-span-2">
                            <div className="aspect-video bg-vanguard-industrial border border-vanguard-slate/10 flex items-center justify-center relative overflow-hidden">
                                <div className="absolute inset-0 opacity-10 bg-[url('https://www.transparenttextures.com/patterns/blueprint.png')]" />
                                <div className="text-vanguard-red font-mono text-[10px] uppercase border border-vanguard-red px-4 py-2 bg-black/50 backdrop-blur-sm">Diagram: Cell Pouch Internal Volume</div>
                            </div>
                            <p className="mt-6 text-sm text-slate-400 leading-relaxed font-sans">
                                Cell Tech Pouch: 2.5L Internal Deployment Volume. External dimensions optimized for 24-hour mission backpacks. Fits all standard battery packs and technical diagnostic tools.
                            </p>
                        </div>
                    </div>
                </div>

                <div className="mt-24 pt-12 border-t border-vanguard-slate/10 text-center">
                    <p className="font-mono text-[9px] text-slate-600 uppercase tracking-widest leading-loose">
                        All measurements are taken under lab conditions (25°C, 30% Humidity).<br />
                        Tolerances: ±0.05mm for CNC machined hardware.
                    </p>
                </div>
            </div>
        </div>
    );
};
