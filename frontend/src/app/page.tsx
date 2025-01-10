import BannerCarousel from "@/components/Carousel";
import Categories from "@/components/Categories";
import Footer from "@/components/Footer";
import Navbar from "@/components/Navbar";
import Products from "@/components/Products";
// import { Button } from "@/components/ui/button";
// import { User } from 'lucide-react';

export default function Home() {
  return (
    <div>
      <Navbar />
      <BannerCarousel />
      <Categories title="Explore Popular Categories" />
      <Products title="Best Selling Products" />
      <Products />

      <Footer />
    </div>
  );
}
