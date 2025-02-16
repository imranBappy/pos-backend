import { Button } from "@/components/ui/button"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuGroup,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
    Avatar,
    AvatarFallback,
    AvatarImage,
} from "@/components/ui/avatar"
import { USER_TYPE } from '@/graphql/accounts';
import Link from 'next/link';
type PropsType = USER_TYPE | null
function Profile({ user }: { user: PropsType }) {

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <div className='flex items-center' >
                    <Avatar className="">
                        <AvatarImage src={user?.photo} alt="Imran" />
                        <AvatarFallback className="bg-black text-white">{user?.name[0]}</AvatarFallback>
                    </Avatar>
                    <Button variant={'link'} className='text-white font-playfair text-base'>{user?.name}</Button>
                </div>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-56">
                <DropdownMenuLabel>My Account</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuGroup>
                    <DropdownMenuItem>
                        <Link className="w-full" href={'/customer/profile'}>Profile</Link>
                    </DropdownMenuItem>
                    <DropdownMenuItem>
                        <Link className="w-full" href={`/customer/orders`}>
                            Orders
                        </Link>
                    </DropdownMenuItem>
                </DropdownMenuGroup>
                <DropdownMenuSeparator />
                <DropdownMenuItem>
                    Log out
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    )
}

export default Profile