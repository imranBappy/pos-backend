import { Button } from './ui/button';
import { Input } from './ui/input';
import { Search} from 'lucide-react';
const SearchInput = () => {
    return (
        <div className=" relative w-96 ">
            <Input className=' w-full pl-4  py-5 flex bottom-0 shadow-none outline-none rounded-full pr-12 ' type="text" placeholder="Search" />
            <Button variant={'ghost'} className='rounded-full py-5 absolute top-0 right-0 ' type="submit"><Search /></Button>
        </div>
    );
};

export default SearchInput;