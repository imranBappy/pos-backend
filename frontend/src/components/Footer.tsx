import Image from 'next/image';
import React from 'react';
import Logo from '@/assets/logo.png'
import { Phone, MapPinHouse, Mail, Facebook, Twitter, Youtube, Instagram, Linkedin } from 'lucide-react';
import { Button } from './ui/button';
import Link from 'next/link';
const Footer = () => {
    const year = new Date().getFullYear()
    return (
        <footer className=' bg-gray-light  dark:bg-gray-deep   mt-10 border-t'>
            <div className="container md:px-0 px-5">
                <div className='py-5 flex flex-wrap justify-between gap-5'>
                    <div>
                        <Image src={Logo} alt='B Soft' width={100} height={100} />
                        <ul className=' mt-5'>
                            <li className='flex  gap-1 items-center'>
                                <Phone size={15} />
                                <Button variant={'link'} className=' px-1  font-oswald text-gray dark:text-gray-light'>
                                    <Link href={"#"}>  +8801601-605023   </Link>
                                </Button>
                                {/* <Button variant={'link'} className='px-1 font-oswald text-gray dark:text-gray-light'>
                                    <Link href={"#"}>  +8801601-605023   </Link>
                                </Button> */}
                            </li>
                            <li className='flex  gap-1 items-center'>
                                <MapPinHouse size={15} />
                                <Button variant={'link'} className=' px-1  font-oswald text-gray dark:text-gray-light '>
                                    <Link href={"#"}>  Mirpur-07, Dhaka-1216  </Link>
                                </Button>
                            </li>
                            <li className='flex  gap-1 items-center'>
                                <Mail size={15} />
                                <Button variant={'link'} className=' px-1  font-oswald text-gray dark:text-gray-light'>
                                    <Link href={"#"}>support@b-soft.xyz</Link>
                                </Button>
                            </li>
                        </ul>
                    </div>
                    <div>
                        <h4 className=' font-playfair font-semibold  text-lg mt-5'>User Area</h4>
                        <ul className=' mt-2'>
                            <li className='flex  gap-1 items-center'>
                                <Button variant={'link'} className=' px-1  font-oswald text-gray dark:text-gray-light'>
                                    <Link href={"/shop"}>  All Products   </Link>
                                </Button>

                            </li>
                            <li className='flex  gap-1 items-center'>
                                <Button variant={'link'} className=' px-1  font-oswald text-gray dark:text-gray-light'>
                                    <Link href={"/account"}>  My Account  </Link>
                                </Button>
                            </li>
                            <li className='flex  gap-1 items-center'>
                                <Button variant={'link'} className=' px-1  font-oswald text-gray dark:text-gray-light'>
                                    <Link href={"/cart"}>  Cart  </Link>
                                </Button>
                            </li>
                        </ul>
                    </div>
                    <div>
                        <h4 className=' font-playfair font-semibold  text-lg mt-5'>Useful Links</h4>
                        <ul className=' mt-2'>
                            <li className='flex  gap-1 items-center'>
                                <Button variant={'link'} className=' px-1  font-oswald text-gray dark:text-gray-light'>
                                    <Link href={"/contact"}> Contact Us   </Link>
                                </Button>

                            </li>
                            <li className='flex  gap-1 items-center'>
                                <Button variant={'link'} className=' px-1  font-oswald text-gray dark:text-gray-light'>
                                    <Link href={"/privicy"}> Privicy Policy   </Link>
                                </Button>
                            </li>
                            <li className='flex  gap-1 items-center'>
                                <Button variant={'link'} className=' px-1  font-oswald text-gray dark:text-gray-light'>
                                    <Link href={"/terms"}>  Terms and Conditions </Link>
                                </Button>
                            </li>
                        </ul>
                    </div>

                </div>
            </div>
            <div className='border-t min-h-16'>
                <div className='container md:px-0 px-5 py-4 min-h-16 flex items-center justify-between flex-wrap gap-2'>
                    <p className='  text-gray dark:text-gray-light font-lato '  >© {year} Bsoft. All rights reserved.</p>
                    <div className='flex gap-2 items-center'>
                        <Link href={'#'}>
                            <Button size={'icon'} variant={'ghost'} >
                                <Facebook />
                            </Button>
                        </Link>
                        <Link href={'#'}>
                            <Button size={'icon'} variant={'ghost'} >
                                <Instagram />
                            </Button>
                        </Link>
                        <Link href={'#'}>
                            <Button size={'icon'} variant={'ghost'} >
                                <Twitter />
                            </Button>
                        </Link>
                        <Link href={'#'}>
                            <Button size={'icon'} variant={'ghost'} >
                                <Youtube />
                            </Button>
                        </Link>
                        <Link href={'#'}>
                            <Button size={'icon'} variant={'ghost'} >
                                <Linkedin />
                            </Button>
                        </Link>
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;