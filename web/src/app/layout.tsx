import '@/app/globals.css';
import type { ReactNode } from 'react';

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="h-full bg-gray-900 text-white">
      <head />
      <body className="min-h-screen flex flex-col">
        {children}
      </body>
    </html>
  );
}
