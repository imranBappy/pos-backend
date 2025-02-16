"use client"

import Product from './Product';
import { ChevronRight } from 'lucide-react';
import { Button } from './ui/button';
import Link from 'next/link';
import { useQuery } from '@apollo/client';
import Loading from './ui/loading';
import { PRODUCT_TYPE, PRODUCTS_QUERY } from '@/graphql/product';

const Products = ({ title = "All Products" }) => {
    const { loading, data } = useQuery(PRODUCTS_QUERY, {
        variables: {
            first: 8
        }
    })
    if (loading) return <Loading />
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
            <div className='flex  gap-5 md:justify-between  justify-evenly flex-wrap '>
                {
                    data?.products?.edges?.map((product: { node: PRODUCT_TYPE }) => <Product key={product.node.id} data={product.node} />)
                }
            </div>
        </div>
    );
};

export default Products;