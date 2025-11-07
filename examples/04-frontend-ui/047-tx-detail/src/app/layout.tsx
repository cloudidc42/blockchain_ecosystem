import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Blockchain Explorer - Transaction Detail',
  description: 'View detailed information about blockchain transactions',
};

export default function RootLayout({
  children,
}: {
  children: React.Node;
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        <header className="bg-blue-600 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold">⛓️ Blockchain Explorer</h1>
                <p className="text-blue-100 text-sm mt-1">Transaction Detail Viewer</p>
              </div>
              <nav className="flex items-center space-x-6">
                <a href="/" className="hover:text-blue-200">Home</a>
                <a href="/blocks" className="hover:text-blue-200">Blocks</a>
                <a href="/transactions" className="hover:text-blue-200">Transactions</a>
              </nav>
            </div>
          </div>
        </header>

        <main>{children}</main>

        <footer className="bg-gray-800 text-gray-300 mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="text-center">
              <p className="text-sm">
                © 2024 Blockchain Explorer. Built with Next.js 14 & TypeScript
              </p>
              <p className="text-xs mt-2 text-gray-400">
                Project 047: Transaction Detail Page
              </p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
