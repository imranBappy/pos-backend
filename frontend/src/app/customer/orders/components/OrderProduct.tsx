import { Button } from "@/components/ui/button";
import Image from "next/image";
import prdImg from '@/assets/no-image.jpg'
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import {  TimerReset } from "lucide-react";

const OrderProduct = () => {
    return (
        <Card className=' basis-60 shadow-none hover:shadow dark:bg-gray-deep '>
            <CardHeader className='p-3 relative '>
                <Image src={prdImg} className='rounded-md' alt='Product Image' width={200} height={200} />
            </CardHeader>
            <CardContent className='px-4 pb-2'>
                <CardTitle className=' font-playfair font-semibold leading-5 line-clamp-2		'>
                    Premium Quality Winter Hoodie For Men
                </CardTitle>

                <p className=' mt-2 flex gap-2 items-center font-oswald '>
                    {/* <span className='  text-gray-400 line-through text-sm '>$100</span> */}
                    <span className='text-blue text-base'>$100</span>
                </p>
            </CardContent>
            <CardFooter className='px-3 pb-3'>
                <Button className=' text-[#333333] font-oswald  w-full' > <TimerReset /> Renew Product </Button>
            </CardFooter>
        </Card>
    );
};

export default OrderProduct;