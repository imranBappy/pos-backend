import Image from 'next/image';
import React from 'react';
import Logo from '@/assets/logo.png'
import { Button } from './ui/button';
import Link from 'next/link';
import { User, Search } from 'lucide-react';
import { CartButton } from '@/components';
import SearchInput from './SearchInput';
import ThemeButton from './ThemeButton';

// #FFC400
// #0074D9
// #FF5733
// #F4F4F4
// #333333
// #00B894
// #FF6F61
// #28A745
// #DC3545
// #FFC107

const Navbar = () => {
    return (
        <div className="navbar border-b h-[80px] dark:bg-gray-deep ">
            <div className="container">
                <div className="navbar-wrap  h-[80px]  flex items-center justify-between">
                    <div className="logo">
                        <Link href={'/'}>
                            <Image src={Logo} width={100} height={100} alt='' />
                        </Link>
                    </div>
                    <div className="search hidden md:block">
                        <SearchInput />
                    </div>
                    <div className="account-cart flex items-center gap-3">
                        <div>
                            <Button className=' md:hidden px-3  font-oswald  text-base' variant={'ghost'}>
                                <Link href={'/login'} className='flex items-center gap-2' >
                                    <Search className="text-4xl" />
                                    <span>Search</span>
                                </Link>
                            </Button>
                            <Button className=' font-oswald  px-3 text-base' variant={'ghost'}>
                                <Link href={'/login'} className='flex items-center gap-2' >
                                    <User className="text-4xl" />
                                    <span>Sing in</span>
                                </Link>
                            </Button>
                        </div>
                        <CartButton count={0} />
                        <ThemeButton />
                    </div>
                </div>
            </div>
        </div >
    );
};

export default Navbar;