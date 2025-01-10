import { ShoppingCart } from 'lucide-react';

const CartButton = ({ count = 0 }) => {
    return (
        <div className='relative cursor-pointer ' >
            <ShoppingCart size={25} />
            {
                count ? <div className=' absolute -top-[12px] -right-[16px] bg-primary shadow-sm   font-oswald text-gray w-[25px] h-[25px]  rounded-full flex items-center justify-center'>{count}</div> : ""
            }

        </div>
    );
};

export default CartButton;