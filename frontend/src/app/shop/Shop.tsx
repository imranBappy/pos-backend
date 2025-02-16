"use client"
import React, { useState } from 'react';
import RangeFilter from '@/components/filters/RangeFilter';
import Filter from '@/components/filters/SearchFilter';
import FilterProducts from '@/components/FilterProducts';
import { useQuery } from '@apollo/client';
import { CATEGORIES_QUERY, CATEGORY_TYPE, PRODUCT_TYPE, PRODUCTS_QUERY } from '@/graphql/product';
import Loading from '@/components/ui/loading';
import { OPTION_TYPE } from '@/components/input';
import useStore from '@/stores';
import { useSearchParams } from 'next/navigation';


const Shop = () => {
    const searchParams = useSearchParams()
    const category = searchParams.get('category')
    const [selectedCategory, setCategory] = useState<string[]>(category ? [category] : [])
    const [priceRange, setPriceRage] = useState(3000)
    const searchQuery = useStore((state) => state.query)
    const { data: productRes } = useQuery(PRODUCTS_QUERY, {
        variables: {
            first: 8,
            category: selectedCategory.join(","),
            priceLte: priceRange,
            search: searchQuery
        },
        nextFetchPolicy: 'no-cache',
        notifyOnNetworkStatusChange: true,
        fetchPolicy: 'network-only'
    })
    const products: PRODUCT_TYPE[] = productRes?.products?.edges?.map(({ node }: { node: PRODUCT_TYPE }) => ({
        id: `${node.id}`,
        name: node.name,
        price: node.price,
        priceRange: node.priceRange,
        offerPrice: node.offerPrice
    }))

    const { loading, data: categoryRes } = useQuery(CATEGORIES_QUERY, {
        variables: { first: 100, },
    });
    const categories: OPTION_TYPE[] = categoryRes?.categories?.edges?.map(({ node }: { node: CATEGORY_TYPE }) => ({ value: `${node.id}`, label: node.name }))
    const handleSelect = (id: string) => {
        setCategory((preState) => [...preState.filter((item) => item != id), id])
    }
    const handRemove = (id: string) => {
        setCategory((preState) => [...preState.filter((item) => item != id)])
    }


    if (loading) return <Loading />
    return (
        <div className='container'>
            <div className='flex my-8 gap-5'>
                <div className='w-96 flex flex-col gap-5'>
                    <RangeFilter rangeState={[priceRange, setPriceRage]} name='Price Range' />
                    <Filter selectedItems={selectedCategory} onRemove={handRemove} onSelect={handleSelect} name='Category' items={categories} />
                </div>
                <div className='w-full'>
                    <FilterProducts products={products} />
                </div>
            </div>
        </div>
    );
};

export default Shop;