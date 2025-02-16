"use client"
import React, { useState, useEffect } from 'react';
import NoImage from '@/assets/no-image.jpg';
import Image from 'next/image';
import { jsonToImages } from '@/lib/utils';

interface ProductPhotoProps {
    images?: string
}

const ProductPhoto = ({ images }: ProductPhotoProps) => {
    const [selected, setSelected] = useState(0)
    const [allImages, setAllImages] = useState<string[]>([]);
    const selectdImage = allImages.length ? allImages[selected] : undefined;

    useEffect(() => {
        const fetchImages = async () => {
            const imagesArray = await jsonToImages(images);
            setAllImages(imagesArray || []);
        };
        fetchImages();
    }, [images]);

    return (
        <div className='flex flex-col gap-3'>
            <Image className='w-[500px] rounded-sm border ' src={selectdImage || NoImage} width={500} height={500} alt={'product.name'} />
            <div className='flex gap-2 justify-between'>
                {
                    allImages?.length ? allImages.map((link, i) => (
                        <Image onClick={() => setSelected(i)} key={i} className={`w-[65px] cursor-pointer rounded-sm  border ${selected === i ? " shadow" : ""}`} src={link} width={500} height={500} alt={'product.name'} />
                    )) :
                        <Image className='w-[65px] cursor-pointer rounded-sm shadow border' src={NoImage} width={500} height={500} alt={'product.name'} />
                }
            </div>
        </div>
    );
};

export default ProductPhoto;