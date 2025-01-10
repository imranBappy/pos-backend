import React from 'react';
import { ChevronRight } from 'lucide-react';
import { Button } from './ui/button';
import Link from 'next/link';
import Category from './Category';

const Categories = ({ title = "All Products" }) => {
    return (
        <div className='container mt-12 '>
            <div className='flex mb-8 justify-between items-center'>
                <h3 className='title'>{title}</h3>
                <Button variant={'link'} className=' text-blue'>
                    <Link href={'/'} className='flex gap-2 items-center font-lato'>
                        <span>More Category</span> <ChevronRight size={18} />
                    </Link>
                </Button>
            </div>
            <div className='flex  md:justify-between justify-around flex-wrap '>
                <Category />
                <Category />
                <Category />
                <Category />
                <Category />
                <Category />
            </div>
        </div>
    );
};

export default Categories;