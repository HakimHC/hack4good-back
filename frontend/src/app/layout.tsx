import type { Metadata } from "next";
import { GeistSans } from 'geist/font/sans';
import "./globals.css";
import Navbar from "@/components/navbar";


export const metadata: Metadata = {
  title: "Planeat",
  description: "Plan a healthy diet",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={GeistSans.variable}>
        <Navbar />
        {children}
      </body>
    </html>
  );
}
