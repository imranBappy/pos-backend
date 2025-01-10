import React from 'react';
import { Button } from './ui/button';
import Image from 'next/image';
import prdImg from '@/assets/prd.webp'

const Category = () => {
    return (
        <div className="group basis-48 flex items-center flex-col  cursor-pointer shadow-none">
            <div className="p-2  max-w-32  md:max-w-44  ">
                <Image
                    src={prdImg}
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
                Computer
            </Button>
        </div>

    );
};

export default Category;