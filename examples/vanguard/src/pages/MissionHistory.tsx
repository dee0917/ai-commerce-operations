import React from 'react';

export const MissionHistory: React.FC = () => {
    return (
        <div className="bg-vanguard-obsidian min-h-screen py-20 px-4">
            <div className="max-w-4xl mx-auto">
                <div className="mb-16 border-l-4 border-vanguard-red pl-8">
                    <div className="font-mono text-vanguard-red text-xs font-bold tracking-[0.5em] uppercase mb-4">Classified Archive</div>
                    <h1 className="text-5xl md:text-7xl font-black text-white uppercase tracking-tighter mb-4">Mission History</h1>
                    <p className="text-slate-500 font-mono text-xs uppercase tracking-widest">System Record: 2021 - 2026 // Authorized Access Only</p>
                </div>

                <div className="space-y-20">
                    {[
                        {
                            year: "2026",
                            mission: "PROJECT VANGUARD INITIALIZATION",
                            status: "ACTIVE",
                            intel: "Deployment of the Obsidian Grid ecosystem. Curating the first generation of aerospace-grade EDC hardware for the global minimalist explorer."
                        },
                        {
                            year: "2024",
                            mission: "OP: TITANIUM SHIELD",
                            status: "SUCCESS",
                            intel: "R&D phase for the Apex Carabiner series. Field tested in rugged alpine environments and urban tactical scenarios. Achieved 0.01mm tolerance benchmarks."
                        },
                        {
                            year: "2022",
                            mission: "THE CIPHER ENCRYPTION",
                            status: "SUCCESS",
                            intel: "Development of the RFID-blocking chassis for the Cipher Wallet line. Integrated real 3K carbon fiber with aerospace aluminum frameworks."
                        },
                        {
                            year: "2021",
                            mission: "GENESIS ZERO",
                            status: "RECORDED",
                            intel: "Founding of Vanguard Gear in a small precision CNC workshop. The mission was clear: Build better tools for those who refuse to compromise."
                        }
                    ].map((entry, i) => (
                        <div key={i} className="relative group">
                            <div className="absolute -left-12 top-0 h-full w-px bg-vanguard-slate/20 group-hover:bg-vanguard-red transition-colors hidden md:block" />
                            <div className="grid md:grid-cols-4 gap-8">
                                <div className="md:col-span-1">
                                    <span className="font-mono text-3xl font-black text-vanguard-red">{entry.year}</span>
                                </div>
                                <div className="md:col-span-3">
                                    <h3 className="text-xl font-bold text-white mb-4 uppercase tracking-tight">{entry.mission}</h3>
                                    <div className="inline-block px-3 py-1 border border-vanguard-slate/30 font-mono text-[9px] text-slate-400 mb-6 font-bold tracking-widest uppercase">Status: {entry.status}</div>
                                    <p className="text-slate-400 leading-relaxed text-sm md:text-base border-t border-vanguard-slate/10 pt-6">
                                        {entry.intel}
                                    </p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="mt-32 p-8 bg-vanguard-industrial border border-vanguard-slate/20 text-center">
                    <h4 className="font-mono text-[10px] text-vanguard-red uppercase tracking-[0.3em] mb-4">End of Transmission</h4>
                    <p className="text-slate-500 text-[10px] uppercase">New mission intelligence is updated periodically by the vanguard council.</p>
                </div>
            </div>
        </div>
    );
};
