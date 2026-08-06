import React from 'react';
import { Link, Outlet } from 'react-router-dom';
import { Sparkles } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

export const About: React.FC = () => (
    <div className="pt-48 px-8 max-w-[1400px] mx-auto pb-32">
        <header className="max-w-4xl mb-32 fade-up">
            <span className="text-[10px] uppercase tracking-[0.5em] font-bold text-brand-accent block mb-6">Our Journey</span>
            <h1 className="text-6xl lg:text-8xl font-display uppercase tracking-tight font-light leading-none mb-12">Legacy of the <br /><span className="italic font-serif">Sacred Brush</span></h1>
            <p className="text-2xl font-light leading-relaxed opacity-80 border-l-2 border-brand-accent pl-10 py-4">
                Since 1928, the Lin family has been the keeper of energetic secrets. What began as a small workshop in the mountains has evolved into AuraGuard—a bridge between ancient wisdom and the modern soul.
            </p>
        </header>

        <section className="grid grid-cols-1 lg:grid-cols-2 gap-32 mb-32 items-center">
            <div className="order-2 lg:order-1 space-y-12 fade-up">
                <div className="space-y-6">
                    <h2 className="text-4xl font-display uppercase tracking-widest font-light">Three Generations of Mastery</h2>
                    <p className="font-light leading-loose text-lg opacity-70">
                        Our talismans are not products; they are outcomes of a lineage. Every cinnabar bead is inspected, every obsidian stone is purified, and every blessing is spoken with intention. We believe that an object's energy is only as pure as the hands that crafted it.
                    </p>
                </div>
                <div className="grid grid-cols-2 gap-12 pt-8">
                    <div>
                        <span className="block text-4xl font-display mb-2">12,000+</span>
                        <span className="uppercase tracking-widest text-[10px] opacity-50 font-bold">Blessed Objects</span>
                    </div>
                    <div>
                        <span className="block text-4xl font-display mb-2">96%</span>
                        <span className="uppercase tracking-widest text-[10px] opacity-50 font-bold">Positive Feedback</span>
                    </div>
                </div>
            </div>
            <div className="order-1 lg:order-2 aspect-[4/5] bg-brand-secondary/5 border border-stone-400 p-4 fade-up">
                <img src="/products/about-hero.jpg" className="w-full h-full object-cover" />
            </div>
        </section>

        <section className="py-24 border-t border-stone-400 fade-up">
            <h2 className="text-[10rem] font-display uppercase tracking-[0.1em] opacity-5 whitespace-nowrap mb-[-4rem]">Purity</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-16">
                <div className="space-y-4">
                    <h3 className="text-xl font-display uppercase tracking-widest font-bold text-brand-accent">01. Source</h3>
                    <p className="font-light opacity-70 text-sm leading-loose">We travel to remote quarries in the high plateaus to source our raw stones, ensuring they have never seen the pollution of industrial trade.</p>
                </div>
                <div className="space-y-4">
                    <h3 className="text-xl font-display uppercase tracking-widest font-bold text-brand-accent">02. Ritual</h3>
                    <p className="font-light opacity-70 text-sm leading-loose">Every piece stays in our monastery sanctuary for 7 days of vibrational cleansing before it enters your home.</p>
                </div>
                <div className="space-y-4">
                    <h3 className="text-xl font-display uppercase tracking-widest font-bold text-brand-accent">03. Impact</h3>
                    <p className="font-light opacity-70 text-sm leading-loose">A portion of every sale goes directly to the preservation of traditional craft schools in the rural provinces.</p>
                </div>
            </div>
        </section>
    </div>
);

export const Contact: React.FC = () => (
    <div className="pt-48 px-8 max-w-[1400px] mx-auto pb-32">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-32">
            <header className="fade-up">
                <span className="text-[10px] uppercase tracking-[0.5em] font-bold text-brand-accent block mb-6">Contact</span>
                <h1 className="text-7xl font-display uppercase tracking-tight font-light leading-none mb-12">Reach Our <br /><span className="italic font-serif">Sanctuary</span></h1>
                <p className="text-xl font-light leading-relaxed opacity-70 mb-16">
                    Our team is available to assist you with energy consultations, order tracking, and custom requests.
                </p>

                <div className="space-y-12">
                    <div>
                        <h4 className="uppercase tracking-widest text-[10px] font-bold opacity-40 mb-4">Email Address</h4>
                        <p className="text-2xl font-display hover:text-brand-accent transition-colors"><a href="mailto:guardians@auraguard.com">guardians@auraguard.com</a></p>
                    </div>
                    <div>
                        <h4 className="uppercase tracking-widest text-[10px] font-bold opacity-40 mb-4">Opening Hours</h4>
                        <p className="text-2xl font-display">Mon — Fri: 09:00 — 18:00 (GMT+8)</p>
                    </div>
                </div>
            </header>

            <form className="bg-[#EAE3DB] p-12 border border-stone-400 fade-up space-y-8" onSubmit={(e) => e.preventDefault()}>
                <div className="grid grid-cols-2 gap-8">
                    <div className="space-y-2">
                        <label className="uppercase tracking-widest text-[10px] font-bold">First Name</label>
                        <input type="text" className="w-full bg-transparent border-b border-stone-400 focus:border-brand-accent outline-none py-2 transition-colors" />
                    </div>
                    <div className="space-y-2">
                        <label className="uppercase tracking-widest text-[10px] font-bold">Last Name</label>
                        <input type="text" className="w-full bg-transparent border-b border-stone-400 focus:border-brand-accent outline-none py-2 transition-colors" />
                    </div>
                </div>
                <div className="space-y-2">
                    <label className="uppercase tracking-widest text-[10px] font-bold">Email Address</label>
                    <input type="email" className="w-full bg-transparent border-b border-stone-400 focus:border-brand-accent outline-none py-2 transition-colors" />
                </div>
                <div className="space-y-2">
                    <label className="uppercase tracking-widest text-[10px] font-bold">Inquiry Type</label>
                    <select className="w-full bg-transparent border-b border-stone-400 focus:border-brand-accent outline-none py-2 transition-colors appearance-none">
                        <option>General Support</option>
                        <option>Product Consultation</option>
                        <option>Custom Requests</option>
                        <option>Shipping & Returns</option>
                    </select>
                </div>
                <div className="space-y-2">
                    <label className="uppercase tracking-widest text-[10px] font-bold">Your Message</label>
                    <textarea rows={4} className="w-full bg-transparent border border-stone-400 focus:border-brand-accent outline-none p-4 mt-2 transition-colors resize-none"></textarea>
                </div>
                <button className="w-full bg-brand-secondary text-brand-primary py-4 uppercase tracking-[0.3em] font-bold text-xs hover:bg-brand-accent transition-all duration-500">
                    Send Message
                </button>
            </form>
        </div>
    </div>
);

export const Checkout: React.FC = () => (
    <div className="pt-48 px-8 max-w-4xl mx-auto pb-32">
        <header className="text-center mb-24">
            <h1 className="text-5xl font-display uppercase tracking-widest font-light mb-8">Sacred Checkout</h1>
            <ul className="flex justify-center items-center gap-12 text-[10px] font-bold tracking-[0.3em] opacity-40 uppercase">
                <li className="text-brand-accent opacity-100">01 Information</li>
                <li>/</li>
                <li>02 Shipping</li>
                <li>/</li>
                <li>03 Payment</li>
            </ul>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-24 items-start">
            <div className="space-y-12">
                <div className="space-y-6">
                    <h3 className="uppercase tracking-widest text-sm font-bold border-b border-stone-400 pb-2">Contact Details</h3>
                    <input type="email" placeholder="Email Address" className="w-full bg-transparent border-b border-stone-400 py-3 outline-none focus:border-brand-accent" />
                </div>
                <div className="space-y-6">
                    <h3 className="uppercase tracking-widest text-sm font-bold border-b border-stone-400 pb-2">Shipping Address</h3>
                    <div className="grid grid-cols-2 gap-4">
                        <input type="text" placeholder="First Name" className="w-full bg-transparent border-b border-stone-400 py-3 outline-none" />
                        <input type="text" placeholder="Last Name" className="w-full bg-transparent border-b border-stone-400 py-3 outline-none" />
                    </div>
                    <input type="text" placeholder="Address" className="w-full bg-transparent border-b border-stone-400 py-3 outline-none" />
                    <div className="grid grid-cols-2 gap-4">
                        <input type="text" placeholder="City" className="w-full bg-transparent border-b border-stone-400 py-3 outline-none" />
                        <input type="text" placeholder="Postcode" className="w-full bg-transparent border-b border-stone-400 py-3 outline-none" />
                    </div>
                </div>
                <Link to="/shop" className="block text-center bg-brand-secondary text-brand-primary py-4 uppercase tracking-[0.3em] font-bold text-xs hover:bg-brand-accent transition-all duration-500 shadow-xl">
                    Proceed to Shipping
                </Link>
            </div>

            <div className="bg-[#EAE3DB] p-10 border border-stone-400">
                <h3 className="uppercase tracking-widest text-sm font-bold mb-8">Order Summary</h3>
                <div className="space-y-6 opacity-60 text-sm font-light uppercase tracking-widest mb-8">
                    <div className="flex justify-between"><span>Subtotal</span><span>$0.00</span></div>
                    <div className="flex justify-between"><span>Shipping</span><span>Calculated at next step</span></div>
                </div>
                <div className="border-t border-stone-400 pt-6 flex justify-between font-display text-2xl">
                    <span>Total</span>
                    <span>$0.00</span>
                </div>
            </div>
        </div>
    </div>
);

export const AccountLayout: React.FC<{ children?: React.ReactNode }> = ({ children }) => {
    return (
        <div className="pt-48 px-8 max-w-[1400px] mx-auto pb-32">
            <header className="mb-20">
                <span className="text-[10px] uppercase tracking-[0.5em] font-bold text-brand-accent block mb-4">Account</span>
                <h1 className="text-5xl lg:text-7xl font-display uppercase tracking-tight font-light">My <span className="italic font-serif">Sanctuary</span></h1>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-20">
                <aside className="lg:col-span-1 border-r border-stone-300 pr-12">
                    <nav>
                        <ul className="space-y-6 font-display text-2xl uppercase tracking-widest">
                            <li><Link to="/account/dashboard" className="hover:text-brand-accent transition-colors">Dashboard</Link></li>
                            <li><Link to="/account/orders" className="hover:text-brand-accent transition-colors">Order History</Link></li>
                            <li><Link to="/account/profile" className="hover:text-brand-accent transition-colors">Profile Details</Link></li>
                            <li className="pt-8 border-t border-stone-300">
                                <button className="text-sm font-bold uppercase tracking-[0.3em] opacity-40 hover:opacity-100 transition-opacity">Sign Out</button>
                            </li>
                        </ul>
                    </nav>
                </aside>
                <main className="lg:col-span-3">
                    {children || <Outlet />}
                </main>
            </div>
        </div>
    );
};

export const DashboardPage: React.FC = () => (
    <div className="space-y-12 fade-up">
        <header className="bg-brand-secondary text-brand-primary p-12 relative overflow-hidden">
            <div className="relative z-10 space-y-4">
                <h2 className="text-4xl font-display uppercase tracking-widest font-light">Welcome Back, Alex</h2>
                <p className="opacity-60 font-light tracking-wide max-w-sm">May your energy remain clear and your spirit guarded today.</p>
            </div>
            <Sparkles className="absolute -right-10 -bottom-10 w-48 h-48 opacity-10 text-brand-accent stroke-[0.5]" />
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="border border-stone-400 p-10 flex flex-col justify-between aspect-video">
                <h3 className="uppercase tracking-widest text-xs font-bold opacity-40">Recent Order</h3>
                <div className="space-y-2">
                    <p className="font-display text-3xl">#1002 — Processing</p>
                    <p className="text-sm opacity-60">Placed on March 01, 2026</p>
                </div>
                <Link to="/account/orders" className="text-xs uppercase tracking-[0.3em] font-bold border-b border-brand-secondary pb-1 self-start">View Details</Link>
            </div>
            <div className="border border-stone-400 p-10 flex flex-col justify-between aspect-video bg-[#EAE3DB]">
                <h3 className="uppercase tracking-widest text-xs font-bold opacity-40">Shipping Address</h3>
                <div className="space-y-1 text-sm font-light">
                    <p>123 Design Street</p>
                    <p>Taipei, 100</p>
                    <p>Taiwan</p>
                </div>
                <Link to="/account/profile" className="text-xs uppercase tracking-[0.3em] font-bold border-b border-brand-secondary pb-1 self-start">Edit Address</Link>
            </div>
        </div>
    </div>
);

export const LoginPage: React.FC = () => {
    const { signIn } = useAuth();

    return (
        <div className="pt-48 px-8 max-w-md mx-auto min-h-screen text-center flex flex-col justify-center">
            <header className="mb-16">
                <span className="text-[10px] uppercase tracking-[0.5em] font-bold text-brand-accent block mb-4">Access</span>
                <h1 className="text-5xl font-display uppercase tracking-widest font-light">Return to <br />Sanctuary</h1>
            </header>
            <div className="space-y-8 bg-[#EAE3DB] p-12 border border-stone-400">
                <div className="space-y-4 text-left">
                    <label className="uppercase tracking-widest text-[10px] font-bold">Email Address</label>
                    <input type="email" placeholder="demo@example.com" disabled className="w-full bg-transparent border-b border-stone-400 py-3 outline-none" />
                </div>
                <div className="space-y-4 text-left">
                    <label className="uppercase tracking-widest text-[10px] font-bold">Password</label>
                    <input type="password" placeholder="••••••••" disabled className="w-full bg-transparent border-b border-stone-400 py-3 outline-none" />
                </div>
                <button
                    onClick={() => signIn('demo@example.com', 'demo1234')}
                    className="w-full bg-brand-secondary text-brand-primary py-4 uppercase tracking-[0.3em] font-bold text-xs hover:bg-brand-accent transition-all duration-500"
                >
                    Authenticate
                </button>
            </div>
            <p className="mt-8 text-xs font-light opacity-50 uppercase tracking-widest">Demo Credentials Pre-filled</p>
        </div>
    );
};

export const RegisterPage: React.FC = () => (
    <div className="pt-48 px-8 max-w-md mx-auto min-h-screen text-center flex flex-col justify-center">
        <header className="mb-16">
            <h1 className="text-5xl font-display uppercase tracking-widest font-light">Join The Circle</h1>
            <p className="mt-6 font-light opacity-60">Registration is currently invitation-only during our high-vibration cycle.</p>
        </header>
        <Link to="/account/login" className="uppercase tracking-[0.3em] text-xs font-bold border-b border-brand-secondary pb-1">Back to Login</Link>
    </div>
);

export const OrdersPage: React.FC = () => (
    <div className="space-y-12 fade-up">
        <h2 className="text-4xl font-display uppercase tracking-widest font-light pb-6 border-b border-stone-300">Order History</h2>
        <div className="space-y-8">
            {[
                { id: '1002', date: 'March 01, 2026', total: '$120.00', status: 'Processing' },
                { id: '1001', date: 'Feb 15, 2026', total: '$113.00', status: 'Delivered' },
            ].map(order => (
                <div key={order.id} className="border border-stone-400 p-8 flex flex-col md:flex-row justify-between items-center gap-8">
                    <div className="space-y-1 text-center md:text-left">
                        <p className="font-display text-2xl">Order #{order.id}</p>
                        <p className="text-xs uppercase tracking-widest opacity-50">{order.date}</p>
                    </div>
                    <div className="flex gap-16 items-center">
                        <div className="text-center md:text-left">
                            <p className="text-[10px] uppercase tracking-widest font-bold opacity-40">Total</p>
                            <p className="font-medium">{order.total}</p>
                        </div>
                        <div className="text-center md:text-left">
                            <p className="text-[10px] uppercase tracking-widest font-bold opacity-40">Status</p>
                            <p className={order.status === 'Processing' ? 'text-brand-accent font-bold' : 'font-medium'}>{order.status}</p>
                        </div>
                    </div>
                    <button className="uppercase tracking-[0.2em] text-[10px] font-bold border border-brand-secondary px-6 py-2 hover:bg-brand-secondary hover:text-brand-primary transition-colors">Details</button>
                </div>
            ))}
        </div>
    </div>
);

export const ProfilePage: React.FC = () => (
    <div className="space-y-12 fade-up max-w-2xl">
        <h2 className="text-4xl font-display uppercase tracking-widest font-light pb-6 border-b border-stone-300">Profile Details</h2>
        <form className="space-y-10" onSubmit={e => e.preventDefault()}>
            <div className="grid grid-cols-2 gap-8">
                <div className="space-y-2">
                    <label className="uppercase tracking-widest text-[10px] font-bold">First Name</label>
                    <input type="text" defaultValue="Alex" className="w-full bg-transparent border-b border-stone-400 py-2 outline-none" />
                </div>
                <div className="space-y-2">
                    <label className="uppercase tracking-widest text-[10px] font-bold">Last Name</label>
                    <input type="text" defaultValue="Johnson" className="w-full bg-transparent border-b border-stone-400 py-2 outline-none" />
                </div>
            </div>
            <div className="space-y-2">
                <label className="uppercase tracking-widest text-[10px] font-bold">Email Address</label>
                <input type="email" defaultValue="demo@example.com" className="w-full bg-transparent border-b border-stone-400 py-2 outline-none" />
            </div>
            <div className="space-y-6 pt-6">
                <h3 className="uppercase tracking-widest text-sm font-bold opacity-40">Shipping Sanctuary</h3>
                <div className="space-y-2">
                    <label className="uppercase tracking-widest text-[10px] font-bold">Address</label>
                    <input type="text" defaultValue="123 Design Street" className="w-full bg-transparent border-b border-stone-400 py-2 outline-none" />
                </div>
                <div className="grid grid-cols-2 gap-8">
                    <div className="space-y-2">
                        <label className="uppercase tracking-widest text-[10px] font-bold">City</label>
                        <input type="text" defaultValue="Taipei" className="w-full bg-transparent border-b border-stone-400 py-2 outline-none" />
                    </div>
                    <div className="space-y-2">
                        <label className="uppercase tracking-widest text-[10px] font-bold">Postcode</label>
                        <input type="text" defaultValue="100" className="w-full bg-transparent border-b border-stone-400 py-2 outline-none" />
                    </div>
                </div>
            </div>
            <button className="bg-brand-secondary text-brand-primary px-12 py-4 uppercase tracking-[0.3em] font-bold text-xs hover:bg-brand-accent transition-all duration-500">
                Update Profile
            </button>
        </form>
    </div>
);
