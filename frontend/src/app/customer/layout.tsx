import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import Link from "next/link";

const CustomerLayout = ({ children }: { children: React.ReactNode }) => {
    return (
        <div className='container flex  gap-7'>
            <div className=" w-80 hidden md:block">
                <h4 className=" font-playfair text-2xl my-5 ">My Account</h4>
                <Separator />
                <ul className="flex flex-col  my-5">
                    <li  >
                        <Button variant={'link'} className="mx-0 px-0 pt-0 text-blue">
                            <Link href="#">My Account</Link>
                        </Button>
                    </li>
                    <li>
                        <Button variant={'link'} className="mx-0 px-0 text-blue">
                            <Link href="#">My Orders</Link>
                        </Button>
                    </li>
                    <li className="mt-3">
                        <Button variant={'outline'} className=" w-full rounded-none">
                            <Link href="#">Logout</Link>
                        </Button>
                    </li>
                </ul>
            </div>
            <div className="px-2">
                {
                    children
                }
            </div>
        </div>
    );
};

export default CustomerLayout;