import React from 'react';
import { ProductCard } from './ProductCard';
import type { WooProduct } from '../types';

interface BentoGridProps {
    products: WooProduct[];
}

export const BentoGrid: React.FC<BentoGridProps> = ({ products }) => {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 px-4 py-12 max-w-7xl mx-auto">
            {products.map((product, index) => {
                // Create some visual variation in the bento grid
                let spanClass = "col-span-1";
                if (index === 0) spanClass = "md:col-span-2 md:row-span-2"; // First one is big
                if (index === 5) spanClass = "md:col-span-1 lg:col-span-2"; // Sixth one is wide

                return (
                    <div key={product.id} className={spanClass}>
                        <ProductCard product={product} />
                    </div>
                );
            })}
        </div>
    );
};
