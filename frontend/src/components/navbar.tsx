// components/Navbar.js
import Link from 'next/link';
import { Button } from './ui/button';
import { ShoppingCart } from "lucide-react"
import Image from 'next/image';

const Navbar = () => {
  return (
    <div className='flex flex-row items-center justify-between py-3 border-b px-20'>
			<div>
				<Image
					src={'/planeat.png'}
					alt='Logo'
					width={175}
					height={100}
				/>
			</div>
			<div className='flex flex-row items-center gap-4'>
				<Button className='rounded-full font-semibold'>Log in</Button>
				<Button variant={'secondary'} className='rounded-full flex flex-row items-center justify-center gap-3 font-semibold'>
					<ShoppingCart size={16} /> 0
				</Button>
			</div>
    </div>
  );
}

export default Navbar;
