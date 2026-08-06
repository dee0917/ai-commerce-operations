export interface Product {
    id: string;
    name: string;
    price: number;
    description: string;
    image: string;
    category: string;
}

const mockProducts: Product[] = [
    {
        id: '1',
        name: 'Silicone Cable Organizer Tie',
        price: 20.10,
        description: 'Keep your workspace tidy with these premium silicone cable ties. Designed for durability and aesthetic harmony.',
        image: '/products/silicone-cable-organizer-tie.jpg',
        category: 'Desk'
    },
    {
        id: '2',
        name: 'Heavy Duty Vacuum Storage Bag',
        price: 27.00,
        description: 'Maximize your closet space effortlessly. Our heavy-duty bags protect against moisture and dust while compacting bulky items.',
        image: '/products/heavy-duty-vacuum-storage-bag.jpg',
        category: 'Home'
    },
    {
        id: '3',
        name: 'Matte Tinplate Organizer Box',
        price: 27.30,
        description: 'A sleek, minimalist matte box perfect for storing small essentials. Built to last with high-quality tinplate.',
        image: '/products/matte-tinplate-organizer-box.jpg',
        category: 'Desk'
    },
    {
        id: '4',
        name: 'Minimalist Mesh Zipper Pouch',
        price: 22.80,
        description: 'See your essentials at a glance. A refined take on the classic mesh pouch with a smooth-gliding premium zipper.',
        image: '/products/minimalist-mesh-zipper-pouch.jpg',
        category: 'Travel'
    },
    {
        id: '5',
        name: 'Bluetooth Smart Label Maker',
        price: 24.70,
        description: 'Organize everything with precision. Our smart label maker connects instantly to your phone for custom, elegant labels.',
        image: '/products/bluetooth-smart-label-maker.jpg',
        category: 'Tech'
    },
    {
        id: '6',
        name: 'Premium Leather Passport Holder',
        price: 22.30,
        description: 'Travel in style and keep your most important document secure with our buttery-soft leather passport holder.',
        image: '/products/premium-leather-passport-holder.jpg',
        category: 'Travel'
    },
    {
        id: '7',
        name: 'Transparent Coin Sorting Tube',
        price: 20.30,
        description: 'Turn loose change into a beautiful display. A minimalist cylinder that makes coin sorting satisfying.',
        image: '/products/transparent-coin-sorting-tube.jpg',
        category: 'Home'
    },
    {
        id: '8',
        name: 'Compact Travel Jewelry Case',
        price: 21.50,
        description: 'Zero tangles, pure elegance. Keep your necklaces, rings, and earrings perfectly organized on the go.',
        image: '/products/compact-travel-jewelry-case.jpg',
        category: 'Travel'
    },
    {
        id: '9',
        name: 'Hard Shell Glasses Case',
        price: 18.60,
        description: 'Ultimate protection wrapped in a matte, geometric shell. Keep your vision clear and lenses scratch-free.',
        image: '/products/hard-shell-glasses-case.jpg',
        category: 'Accessories'
    },
    {
        id: '10',
        name: 'Water-resistant Cosmetic Bag',
        price: 29.20,
        description: 'A spacious, wipe-clean beauty essential designed for both daily use and exotic getaways.',
        image: '/products/water-resistant-cosmetic-bag.jpg',
        category: 'Travel'
    }
];

const USE_MOCK = !import.meta.env.VITE_WOO_API_URL;

export const fetchProducts = async (): Promise<Product[]> => {
    if (USE_MOCK) {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 500));
        return mockProducts;
    }

    // Placeholder for real WooCommerce fetch
    return [];
};

export const fetchProductById = async (id: string): Promise<Product | undefined> => {
    if (USE_MOCK) {
        await new Promise(resolve => setTimeout(resolve, 300));
        return mockProducts.find(p => p.id === id);
    }

    return undefined;
};
