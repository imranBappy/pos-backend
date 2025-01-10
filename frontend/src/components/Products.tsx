import React from 'react';
import Product from './Product';
import { ChevronRight } from 'lucide-react';
import { Button } from './ui/button';
import Link from 'next/link';

const Products = ({ title = "All Products" }) => {
    return (
        <div className='container mt-10 '>
            <div className='flex mb-5 justify-between items-center'>
                <h3 className='title'>{title}</h3>
                <Button variant={'link'} className=' text-blue'>
                    <Link href={'/'} className='flex gap-2 items-center font-lato'>
                        <span>More Products</span> <ChevronRight size={18} />
                    </Link>
                </Button>
            </div>
            <div className='    flex  gap-5 md:justify-between  justify-evenly flex-wrap '>
                <Product />
                <Product />
                <Product />
                <Product />
                <Product />
                <Product />
                <Product />
                <Product />
            </div>
        </div>
    );
};

export default Products;