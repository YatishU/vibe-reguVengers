import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ESG Copilot",
  description: "AI-Driven ESG Compliance & Risk Drift Analyzer",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
