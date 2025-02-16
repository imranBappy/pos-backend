"use client"

import Product from './Product';

import { PRODUCT_TYPE } from '@/graphql/product';

const FilterProducts = ({ products }: { products: PRODUCT_TYPE[] }) => {
    return (
        <div className='flex  gap-5  md:justify-start  justify-evenly flex-wrap '>
            {
                products?.map((product: PRODUCT_TYPE) => <Product key={product.id} data={product} />)
            }
        </div>
    );
};

export default FilterProducts;