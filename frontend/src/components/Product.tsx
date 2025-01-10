import React from 'react';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import Image from 'next/image';
import prdImg from '@/assets/prd.webp'
import { CheckCheck, ShoppingCart } from 'lucide-react';
import { Badge } from "@/components/ui/badge"

const Product = () => {
    return (
        <Card className=' basis-72 shadow-none hover:shadow dark:bg-gray-deep '>
            <CardHeader className='p-3 relative '>
                <div className=' absolute top-6 left-5 flex flex-col gap-2'>
                    <Badge className=' text-white justify-center items-center font-oswald'>-50%</Badge>
                    <Badge className='bg-orange text-white justify-center items-center font-oswald' >HOT</Badge>
                    {/* <Badge className='bg-blue text-white justify-center items-center'>NEW</Badge> */}
                </div>
                <Image src={prdImg} className='rounded-md' alt='Product Image' width={500} height={500} />
            </CardHeader>
            <CardContent className='px-4'>
                <CardTitle className=' font-playfair font-semibold'>
                    Microsoft Office 2021 Professional Plus License Key Price In BD
                </CardTitle>
                <p className=' mt-4 flex gap-2 items-center '> <CheckCheck size={20} className='text-blue ' /> <span className=' font-oswald'>In stock</span> </p>
                <p className=' mt-2 flex gap-2 items-center font-oswald '>
                    <span className='  text-gray-400 line-through text-sm '>$100</span>
                    <span className='text-blue text-base'>$100</span>
                </p>
            </CardContent>
            <CardFooter className='px-3 pb-3'>
                <Button className=' text-[#333333] font-oswald  w-full' > <ShoppingCart /> Add To Cart </Button>
            </CardFooter>
        </Card>
    );
};

export default Product;