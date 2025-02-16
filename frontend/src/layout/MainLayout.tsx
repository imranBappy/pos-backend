import { ThemeProvider } from "@/components/provider/theme-provider";
import ApolloClientProvider from "@/lib/ApolloClientProvider"
import { Toaster } from "@/components/ui/toaster"
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import ButtomCart from "@/components/ButtomCart";

export default function MainLayout({ children }: { children: React.ReactNode }) {
    return (
        <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
        >
            <ApolloClientProvider>
                <Navbar />
                <main>
                    {children}
                </main>
                <Footer />
                <ButtomCart />
                <Toaster />
            </ApolloClientProvider>
        </ThemeProvider>
    )
}
