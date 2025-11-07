import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Link from 'next/link';
import { Blocks } from 'lucide-react';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Blockchain Explorer',
  description: 'Explore blockchain data - blocks, transactions, and addresses',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gray-50">
          {/* Header */}
          <header className="bg-white shadow-sm border-b border-gray-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
              <div className="flex items-center justify-between">
                <Link href="/" className="flex items-center gap-2">
                  <Blocks className="w-8 h-8 text-primary-600" />
                  <h1 className="text-2xl font-bold text-gray-900">
                    Blockchain Explorer
                  </h1>
                </Link>
                <nav className="flex items-center gap-6">
                  <Link
                    href="/"
                    className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
                  >
                    Blocks
                  </Link>
                  <Link
                    href="/stats"
                    className="text-gray-600 hover:text-gray-900 font-medium transition-colors"
                  >
                    Statistics
                  </Link>
                </nav>
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main>{children}</main>

          {/* Footer */}
          <footer className="bg-white border-t border-gray-200 mt-12">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
              <div className="text-center text-sm text-gray-500">
                <p>Blockchain Explorer v1.0.0</p>
                <p className="mt-1">
                  Built with Next.js, TypeScript & Tailwind CSS
                </p>
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
