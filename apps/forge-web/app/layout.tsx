import React from 'react';

export const metadata = {
  title: 'ONGISA - Codebase & GitHub Statistical Analyzer',
  description: 'Omar Nashiru-deen GitHub Statistical Analyzer & Architecture Engine',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-950 text-gray-100 min-h-screen">
        {children}
      </body>
    </html>
  );
}