import React from 'react';

export const metadata = {
  title: 'Forge Dashboard',
  description: 'AI-Powered Codebase Analysis & Refactoring',
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