import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Stitch Tablemate - AI Restaurant Finder",
  description: "Find the perfect restaurant using AI-powered recommendations.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen bg-background antialiased selection:bg-accent selection:text-white`}>
        {children}
      </body>
    </html>
  );
}
