import React from 'react';
import { Button } from './ui/button';
import Image from 'next/image';
import noImage from '@/assets/image.jpg'

import { CATEGORY_TYPE } from '@/graphql/product';
import Link from 'next/link';

const Category = ({ data }: { data: CATEGORY_TYPE }) => {
    return (
        <Link href={`/shop?category=${data.id}`} className="group basis-48 flex items-center flex-col  cursor-pointer shadow-none">
            <div className="p-2  max-w-32  md:max-w-44  ">
                <Image
                    src={data.photo || noImage}
                    className="rounded-full w-full"
                    alt="Product Image"
                    width={500}
                    height={500}
                />
            </div>
            <Button
                variant="link"
                className="text-blue font-oswald md:text-lg text-base  w-full group-hover:underline"
            >
                {data.name}
            </Button>
        </Link>

    );
};

export default Category;