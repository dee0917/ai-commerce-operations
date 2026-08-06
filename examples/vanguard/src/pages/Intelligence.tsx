import React from 'react';

const IntelligenceTemplate: React.FC<{ title: string, subtitle: string, children: React.ReactNode }> = ({ title, subtitle, children }) => (
    <div className="bg-vanguard-obsidian min-h-screen py-20 px-4">
        <div className="max-w-4xl mx-auto">
            <div className="mb-16">
                <div className="font-mono text-vanguard-red text-xs font-bold tracking-[0.5em] uppercase mb-4">{subtitle}</div>
                <h1 className="text-5xl font-black text-white uppercase tracking-tighter mb-4">{title}</h1>
                <div className="h-1 w-20 bg-vanguard-red" />
            </div>
            <div className="grid gap-12 text-slate-400">
                {children}
            </div>
        </div>
    </div>
);

export const TacticalSupport: React.FC = () => (
    <IntelligenceTemplate title="Tactical Support" subtitle="Technical Assistance Ops">
        <div className="space-y-8">
            {[
                { q: "How do I maintain my titanium gear?", a: "Wash with mild soap and water. Titanium is naturally corrosion resistant, but avoiding abrasive cleaners will preserve the matte finish." },
                { q: "Is the RFID blocking permanent?", a: "Yes, our Cipher wallets use integrated aerospace-grade aluminum plates that provide life-long RFID protection." },
                { q: "Can I replace the bits in the Torque driver?", a: "The Torque driver is compatible with all standard 4mm (1/8\") hex bits. It ships with a set of 10 S2 steel bits." }
            ].map((item, i) => (
                <div key={i} className="border-b border-vanguard-slate/10 pb-8">
                    <h3 className="text-white font-mono text-lg font-bold uppercase mb-4 flex gap-4">
                        <span className="text-vanguard-red">Q:</span> {item.q}
                    </h3>
                    <p className="pl-10 text-sm leading-relaxed">{item.a}</p>
                </div>
            ))}
        </div>
    </IntelligenceTemplate>
);

export const SecurityProtocol: React.FC = () => (
    <IntelligenceTemplate title="Security Protocol" subtitle="Data & Identity Protection">
        <div className="bg-vanguard-industrial border border-vanguard-slate/20 p-10 font-mono text-sm leading-loose">
            <p className="mb-6"><span className="text-vanguard-red">[ENCRYPTION_LEVEL]:</span> AES-256 MIL-SPEC</p>
            <p className="mb-6"><span className="text-vanguard-red">[DATA_RETENTION]:</span> VOLATILE / 30 DAY CYCLE</p>
            <p className="mb-6"><span className="text-vanguard-red">[TRACKING_BLOCK]:</span> ACTIVE</p>
            <div className="h-px bg-vanguard-slate/20 my-10" />
            <p className="text-slate-500">
                Vanguard Gear operates on a need-to-know basis. We do not sell your operational data. Your purchase history is encrypted and accessible only to logistics officers for dispatch verification.
            </p>
        </div>
    </IntelligenceTemplate>
);
