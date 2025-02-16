"use client"
// import { ChevronRight } from 'lucide-react';
// import { Button } from './ui/button';
// import Link from 'next/link';
import Category from './Category';
import { useQuery } from '@apollo/client';
import { CATEGORIES_QUERY, CATEGORY_TYPE } from '@/graphql/product';
import Loading from './ui/loading';

const Categories = ({ title = "All Products" }) => {

    const { loading, data, } = useQuery(CATEGORIES_QUERY, {
        variables: {
            first: 5,
            isActive: true
        }
    })
    if (loading) return <Loading />
    return (
        <div className='container mt-12'>
            <div className='flex mb-8 justify-between items-center'>
                <h3 className='title'>{title}</h3>
                {/* <Button variant={'link'} className=' text-blue'>
                    <Link href={'/'} className='flex gap-2 items-center font-lato'>
                        <span>More Category</span> <ChevronRight size={18} />
                    </Link>
                </Button> */}
            </div>
            <div className='flex  md:justify-between justify-around flex-wrap '>
                {
                    data?.categories?.edges?.map((category: { node: CATEGORY_TYPE }) => <Category key={category.node.id} data={category.node} />)
                }
            </div>
        </div>
    );
};

export default Categories;