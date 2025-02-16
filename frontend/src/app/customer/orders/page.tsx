import { Button } from "@/components/ui/button";
import OrderProduct from "./components/OrderProduct";

const page = () => {
    return (
        <div className='flex flex-wrap gap-6 flex-col w-full mt-5 '>
            <div className="w-full">
                <div className="mb-5">
                    <h6 className=" font-lato text-lg">Your Order ID: <span className=" text-blue ">37143345035541</span> (1 items)</h6>
                    <Button className=" mt-2 uppercase hover:bg-green hover:text-white rounded-sm border-green text-green  " variant={'outline'}>Complated</Button>
                </div>
                <div className="flex  gap-5 md:justify-between  justify-evenly flex-wrap">
                    <OrderProduct />
                </div>
            </div>
            <div className="w-full">
                <div className="mb-5">
                    <h6 className=" font-lato text-lg mt-0">Your Order ID: <span className=" text-blue ">37143345035541</span> (1 items)</h6>
                    <Button className=" mt-2 uppercase hover:bg-green hover:text-white rounded-sm border-green text-green  " variant={'outline'}>Complated</Button>
                </div>
                <div className="flex  gap-5 md:justify-between  justify-evenly flex-wrap">
                    <OrderProduct />
                    <OrderProduct />
                    <OrderProduct />
                    <OrderProduct />
                    <OrderProduct />

                </div>
            </div>

        </div>
    );
};

export default page;