import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { GlobalProvider } from "@/context/GlobalContext";
import ThemeScript from "@/components/ThemeScript";
import LayoutWrapper from "@/components/LayoutWrapper";

// Use Inter font with swap display for better loading
const font = Inter({
  subsets: ["latin"],
  display: "swap",
  fallback: ["system-ui", "sans-serif"],
});

export const metadata: Metadata = {
  title: "11+ Tutor - Free AI-Powered Grammar School Prep",
  description: "Free, open-source AI-powered 11+ exam preparation for grammar school entrance. Practice verbal reasoning, maths, and more.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <ThemeScript />
      </head>
      <body className={font.className}>
        <GlobalProvider>
          <LayoutWrapper>{children}</LayoutWrapper>
        </GlobalProvider>
      </body>
    </html>
  );
}
