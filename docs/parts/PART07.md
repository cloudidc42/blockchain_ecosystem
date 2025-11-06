# PART07 - Explorer UI & Frontend

> **เนื้อหา**: Next.js 14 Setup, Complete Pages Implementation, Component Library, API Integration, State Management, Dark Mode
>
> **เป้าหมาย**: สร้าง production-ready frontend สำหรับ Blockchain Explorer
>
> **ระยะเวลา**: 14-18 ชั่วโมง
>
> **Prerequisites**: PART01-06, Node.js 20+, Next.js 14, React 18, TypeScript

---

## 📑 สารบัญ

1. [Frontend Architecture](#frontend-architecture)
2. [Next.js 14 Setup](#nextjs-14-setup)
3. [Page Implementation](#page-implementation)
4. [Component Library](#component-library)
5. [API Integration](#api-integration)
6. [State Management](#state-management)
7. [Styling & Theming](#styling--theming)
8. [Performance Optimization](#performance-optimization)
9. [แบบฝึกหัด](#แบบฝึกหัด)

---

## Frontend Architecture

### 1.1 Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   Frontend Architecture                     │
└─────────────────────────────────────────────────────────────┘

    User Browser
         │
         ▼
  ┌──────────────┐
  │   Next.js    │
  │  (Frontend)  │
  └──────┬───────┘
         │
    ┌────┴─────┬──────────┬───────────┐
    ▼          ▼          ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Home   │ │ Blocks │ │  Txs   │ │Address │
│ Page   │ │ Page   │ │ Page   │ │ Page   │
└───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘
    │          │          │          │
    └──────────┴──────────┴──────────┘
               │
               ▼
       ┌──────────────┐
       │ API Client   │
       └──────┬───────┘
              │
              ▼ HTTP
       ┌──────────────┐
       │  Backend API │
       └──────────────┘
```

### 1.2 Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **State**: React Context API
- **Data Fetching**: Native Fetch API + SWR
- **Forms**: React Hook Form + Zod
- **Icons**: Lucide React
- **Charts**: Recharts

---

## Next.js 14 Setup

### 2.1 Project Initialization

```bash
# Create Next.js 14 app
npx create-next-app@latest blockchain-explorer-ui --typescript --tailwind --app

cd blockchain-explorer-ui

# Install dependencies
npm install @tanstack/react-query lucide-react date-fns clsx tailwind-merge
npm install @radix-ui/react-dropdown-menu @radix-ui/react-dialog
npm install recharts swr
npm install -D @types/node
```

### 2.2 Project Structure

```
ui/
├── app/                        # Next.js App Router
│   ├── layout.tsx             # Root layout
│   ├── page.tsx               # Home page
│   ├── blocks/
│   │   ├── page.tsx           # Blocks list
│   │   └── [id]/
│   │       └── page.tsx       # Block detail
│   ├── tx/
│   │   └── [hash]/
│   │       └── page.tsx       # Transaction detail
│   ├── address/
│   │   └── [addr]/
│   │       └── page.tsx       # Address detail
│   ├── tokens/
│   │   ├── page.tsx           # Tokens list
│   │   └── [addr]/
│   │       └── page.tsx       # Token detail
│   └── search/
│       └── page.tsx           # Search results
├── components/
│   ├── ui/                    # shadcn/ui components
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   └── Sidebar.tsx
│   ├── blocks/
│   │   ├── BlockCard.tsx
│   │   ├── BlockList.tsx
│   │   └── BlockDetail.tsx
│   ├── transactions/
│   │   ├── TransactionCard.tsx
│   │   ├── TransactionList.tsx
│   │   └── TransactionDetail.tsx
│   ├── common/
│   │   ├── Pagination.tsx
│   │   ├── LoadingSpinner.tsx
│   │   ├── ErrorMessage.tsx
│   │   └── CopyButton.tsx
│   └── search/
│       └── SearchBar.tsx
├── lib/
│   ├── api.ts                 # API client
│   ├── utils.ts               # Utility functions
│   ├── types.ts               # TypeScript types
│   └── constants.ts           # Constants
├── hooks/
│   ├── useBlock.ts            # Block hooks
│   ├── useTransaction.ts      # Transaction hooks
│   └── useSearch.ts           # Search hooks
├── context/
│   └── ThemeContext.tsx       # Theme provider
└── public/
    └── assets/
```

### 2.3 Configuration Files

**tsconfig.json**:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

**tailwind.config.ts**:

```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
```

---

## Page Implementation

### 3.1 Root Layout (app/layout.tsx)

```typescript
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/context/ThemeContext";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Blockchain Explorer",
  description: "Explore blocks, transactions, and addresses on the blockchain",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <div className="flex min-h-screen flex-col">
            <Header />
            <main className="flex-1 container mx-auto px-4 py-8">
              {children}
            </main>
            <Footer />
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
```

### 3.2 Home Page (app/page.tsx)

```typescript
import { Suspense } from "react";
import Link from "next/link";
import { BlockCard, TransactionCard } from "@/components";
import { Search, Activity, Blocks, FileText } from "lucide-react";
import SearchBar from "@/components/search/SearchBar";
import { getLatestBlocks, getLatestTransactions, getStats } from "@/lib/api";

export default async function HomePage() {
  // Fetch data server-side
  const [blocks, transactions, stats] = await Promise.all([
    getLatestBlocks(5),
    getLatestTransactions(5),
    getStats(),
  ]);

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <section className="text-center py-12">
        <h1 className="text-4xl font-bold mb-4">
          Blockchain Explorer
        </h1>
        <p className="text-muted-foreground text-lg mb-8">
          Explore blocks, transactions, and addresses on the blockchain
        </p>

        {/* Search Bar */}
        <div className="max-w-2xl mx-auto">
          <SearchBar />
        </div>
      </section>

      {/* Stats Cards */}
      <section className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatsCard
          title="Latest Block"
          value={stats.latestBlock.toLocaleString()}
          icon={<Blocks className="w-8 h-8" />}
        />
        <StatsCard
          title="Total Transactions"
          value={stats.totalTransactions.toLocaleString()}
          icon={<FileText className="w-8 h-8" />}
        />
        <StatsCard
          title="Gas Price"
          value={`${stats.gasPrice} Gwei`}
          icon={<Activity className="w-8 h-8" />}
        />
        <StatsCard
          title="Active Addresses"
          value={stats.activeAddresses.toLocaleString()}
          icon={<Search className="w-8 h-8" />}
        />
      </section>

      {/* Latest Blocks and Transactions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Latest Blocks */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-semibold">Latest Blocks</h2>
            <Link
              href="/blocks"
              className="text-primary hover:underline text-sm"
            >
              View all →
            </Link>
          </div>

          <div className="space-y-3">
            <Suspense fallback={<LoadingSkeleton count={5} />}>
              {blocks.map((block) => (
                <BlockCard key={block.blockNumber} block={block} />
              ))}
            </Suspense>
          </div>
        </section>

        {/* Latest Transactions */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-semibold">Latest Transactions</h2>
            <Link
              href="/transactions"
              className="text-primary hover:underline text-sm"
            >
              View all →
            </Link>
          </div>

          <div className="space-y-3">
            <Suspense fallback={<LoadingSkeleton count={5} />}>
              {transactions.map((tx) => (
                <TransactionCard
                  key={tx.transactionHash}
                  transaction={tx}
                />
              ))}
            </Suspense>
          </div>
        </section>
      </div>
    </div>
  );
}

function StatsCard({
  title,
  value,
  icon,
}: {
  title: string;
  value: string;
  icon: React.ReactNode;
}) {
  return (
    <div className="bg-card rounded-lg p-6 border shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-muted-foreground">{title}</p>
          <p className="text-2xl font-bold mt-2">{value}</p>
        </div>
        <div className="text-primary">{icon}</div>
      </div>
    </div>
  );
}

function LoadingSkeleton({ count }: { count: number }) {
  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="bg-card rounded-lg p-4 border animate-pulse"
        >
          <div className="h-16 bg-muted rounded" />
        </div>
      ))}
    </>
  );
}
```

### 3.3 Blocks List Page (app/blocks/page.tsx)

```typescript
"use client";

import { useState } from "react";
import { useBlocks } from "@/hooks/useBlock";
import BlockCard from "@/components/blocks/BlockCard";
import Pagination from "@/components/common/Pagination";
import LoadingSpinner from "@/components/common/LoadingSpinner";
import ErrorMessage from "@/components/common/ErrorMessage";

export default function BlocksPage() {
  const [page, setPage] = useState(1);
  const pageSize = 20;

  const { data, error, isLoading } = useBlocks(page, pageSize);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return <ErrorMessage error="Failed to load blocks" />;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Blocks</h1>
        <div className="text-sm text-muted-foreground">
          Total: {data.total.toLocaleString()} blocks
        </div>
      </div>

      {/* Blocks List */}
      <div className="space-y-3">
        {data.items.map((block) => (
          <BlockCard key={block.blockNumber} block={block} />
        ))}
      </div>

      {/* Pagination */}
      <Pagination
        currentPage={page}
        totalPages={data.totalPages}
        onPageChange={setPage}
      />
    </div>
  );
}
```

### 3.4 Block Detail Page (app/blocks/[id]/page.tsx)

```typescript
import { notFound } from "next/navigation";
import { getBlock } from "@/lib/api";
import BlockDetail from "@/components/blocks/BlockDetail";
import TransactionList from "@/components/transactions/TransactionList";
import { formatTimestamp } from "@/lib/utils";

export async function generateMetadata({ params }: { params: { id: string } }) {
  return {
    title: `Block #${params.id} - Blockchain Explorer`,
    description: `View details for block #${params.id}`,
  };
}

export default async function BlockDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const blockNumber = parseInt(params.id);

  if (isNaN(blockNumber)) {
    notFound();
  }

  const block = await getBlock(blockNumber);

  if (!block) {
    notFound();
  }

  return (
    <div className="space-y-8">
      {/* Block Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">Block #{block.blockNumber}</h1>
        <p className="text-muted-foreground">
          {formatTimestamp(block.timestamp)}
        </p>
      </div>

      {/* Block Details */}
      <BlockDetail block={block} />

      {/* Transactions */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">
          Transactions ({block.transactionCount})
        </h2>
        <TransactionList blockNumber={blockNumber} />
      </section>
    </div>
  );
}
```

### 3.5 Transaction Detail Page (app/tx/[hash]/page.tsx)

```typescript
import { notFound } from "next/navigation";
import { getTransaction } from "@/lib/api";
import TransactionDetail from "@/components/transactions/TransactionDetail";
import { Badge } from "@/components/ui/badge";
import { CheckCircle, XCircle } from "lucide-react";

export async function generateMetadata({ params }: { params: { hash: string } }) {
  return {
    title: `Transaction ${params.hash} - Blockchain Explorer`,
    description: `View details for transaction ${params.hash}`,
  };
}

export default async function TransactionDetailPage({
  params,
}: {
  params: { hash: string };
}) {
  const transaction = await getTransaction(params.hash);

  if (!transaction) {
    notFound();
  }

  const isSuccess = transaction.status === 1;

  return (
    <div className="space-y-8">
      {/* Transaction Header */}
      <div>
        <div className="flex items-center gap-3 mb-2">
          <h1 className="text-2xl font-bold">Transaction Details</h1>
          <Badge variant={isSuccess ? "default" : "destructive"}>
            {isSuccess ? (
              <>
                <CheckCircle className="w-4 h-4 mr-1" />
                Success
              </>
            ) : (
              <>
                <XCircle className="w-4 h-4 mr-1" />
                Failed
              </>
            )}
          </Badge>
        </div>
        <p className="text-sm text-muted-foreground font-mono">
          {transaction.transactionHash}
        </p>
      </div>

      {/* Transaction Details */}
      <TransactionDetail transaction={transaction} />

      {/* Logs (if any) */}
      {transaction.logs && transaction.logs.length > 0 && (
        <section>
          <h2 className="text-2xl font-semibold mb-4">
            Logs ({transaction.logs.length})
          </h2>
          <div className="space-y-3">
            {transaction.logs.map((log, index) => (
              <LogCard key={index} log={log} index={index} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
```

---

## Component Library

### 4.1 Block Card (components/blocks/BlockCard.tsx)

```typescript
import Link from "next/link";
import { Blocks, User, Zap } from "lucide-react";
import { formatDistanceToNow } from "date-fns";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Block } from "@/lib/types";
import { shortenHash } from "@/lib/utils";

interface BlockCardProps {
  block: Block;
}

export default function BlockCard({ block }: BlockCardProps) {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Left: Block Info */}
          <div className="flex items-center gap-3">
            <div className="bg-primary/10 rounded-lg p-3">
              <Blocks className="w-6 h-6 text-primary" />
            </div>
            <div>
              <Link
                href={`/blocks/${block.blockNumber}`}
                className="font-semibold text-lg hover:text-primary"
              >
                #{block.blockNumber.toLocaleString()}
              </Link>
              <p className="text-xs text-muted-foreground">
                {formatDistanceToNow(new Date(block.timestamp * 1000), {
                  addSuffix: true,
                })}
              </p>
            </div>
          </div>

          {/* Middle: Miner */}
          <div className="flex items-center gap-2">
            <User className="w-4 h-4 text-muted-foreground" />
            <div className="flex-1 min-w-0">
              <p className="text-xs text-muted-foreground">Miner</p>
              <Link
                href={`/address/${block.miner}`}
                className="text-sm font-mono hover:text-primary truncate block"
              >
                {shortenHash(block.miner)}
              </Link>
            </div>
          </div>

          {/* Right: Stats */}
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-xs text-muted-foreground">Transactions</p>
              <Badge variant="outline">
                {block.transactionCount}
              </Badge>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Gas Used</p>
              <div className="flex items-center gap-1">
                <Zap className="w-3 h-3 text-yellow-500" />
                <span className="text-sm font-semibold">
                  {((block.gasUsed / block.gasLimit) * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
```

### 4.2 Transaction Card (components/transactions/TransactionCard.tsx)

```typescript
import Link from "next/link";
import { ArrowRight, FileText } from "lucide-react";
import { formatDistanceToNow } from "date-fns";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Transaction } from "@/lib/types";
import { shortenHash, formatEther } from "@/lib/utils";

interface TransactionCardProps {
  transaction: Transaction;
}

export default function TransactionCard({ transaction }: TransactionCardProps) {
  const isSuccess = transaction.status === 1;

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Left: TX Hash */}
          <div className="flex items-center gap-3">
            <div className="bg-primary/10 rounded-lg p-3">
              <FileText className="w-6 h-6 text-primary" />
            </div>
            <div className="flex-1 min-w-0">
              <Link
                href={`/tx/${transaction.transactionHash}`}
                className="font-mono text-sm hover:text-primary truncate block"
              >
                {shortenHash(transaction.transactionHash)}
              </Link>
              <p className="text-xs text-muted-foreground">
                {formatDistanceToNow(new Date(transaction.timestamp * 1000), {
                  addSuffix: true,
                })}
              </p>
            </div>
          </div>

          {/* Middle: From -> To */}
          <div className="col-span-2 flex items-center gap-2">
            <Link
              href={`/address/${transaction.fromAddress}`}
              className="font-mono text-sm hover:text-primary truncate max-w-[120px]"
            >
              {shortenHash(transaction.fromAddress)}
            </Link>
            <ArrowRight className="w-4 h-4 text-muted-foreground flex-shrink-0" />
            {transaction.toAddress ? (
              <Link
                href={`/address/${transaction.toAddress}`}
                className="font-mono text-sm hover:text-primary truncate max-w-[120px]"
              >
                {shortenHash(transaction.toAddress)}
              </Link>
            ) : (
              <span className="text-sm text-muted-foreground">
                Contract Creation
              </span>
            )}
          </div>

          {/* Right: Value & Status */}
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-xs text-muted-foreground">Value</p>
              <p className="text-sm font-semibold">
                {formatEther(transaction.value)} ETH
              </p>
            </div>
            <Badge variant={isSuccess ? "default" : "destructive"}>
              {isSuccess ? "Success" : "Failed"}
            </Badge>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
```

### 4.3 Search Bar (components/search/SearchBar.tsx)

```typescript
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function SearchBar() {
  const [query, setQuery] = useState("");
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/search?q=${encodeURIComponent(query)}`);
    }
  };

  return (
    <form onSubmit={handleSearch} className="relative">
      <Input
        type="text"
        placeholder="Search by Block / Txn Hash / Address"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="pl-12 pr-4 py-6 text-lg"
      />
      <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-6 h-6 text-muted-foreground" />
      <Button
        type="submit"
        size="lg"
        className="absolute right-2 top-1/2 -translate-y-1/2"
      >
        Search
      </Button>
    </form>
  );
}
```

### 4.4 Pagination (components/common/Pagination.tsx)

```typescript
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-react";
import { Button } from "@/components/ui/button";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export default function Pagination({
  currentPage,
  totalPages,
  onPageChange,
}: PaginationProps) {
  const pages = [];
  const maxVisible = 5;

  let startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2));
  let endPage = Math.min(totalPages, startPage + maxVisible - 1);

  if (endPage - startPage < maxVisible - 1) {
    startPage = Math.max(1, endPage - maxVisible + 1);
  }

  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }

  return (
    <div className="flex items-center justify-center gap-2">
      {/* First page */}
      <Button
        variant="outline"
        size="icon"
        onClick={() => onPageChange(1)}
        disabled={currentPage === 1}
      >
        <ChevronsLeft className="w-4 h-4" />
      </Button>

      {/* Previous */}
      <Button
        variant="outline"
        size="icon"
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
      >
        <ChevronLeft className="w-4 h-4" />
      </Button>

      {/* Page numbers */}
      {pages.map((page) => (
        <Button
          key={page}
          variant={page === currentPage ? "default" : "outline"}
          onClick={() => onPageChange(page)}
        >
          {page}
        </Button>
      ))}

      {/* Next */}
      <Button
        variant="outline"
        size="icon"
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
      >
        <ChevronRight className="w-4 h-4" />
      </Button>

      {/* Last page */}
      <Button
        variant="outline"
        size="icon"
        onClick={() => onPageChange(totalPages)}
        disabled={currentPage === totalPages}
      >
        <ChevronsRight className="w-4 h-4" />
      </Button>
    </div>
  );
}
```

---

## API Integration

### 5.1 API Client (lib/api.ts)

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "APIError";
  }
}

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    next: {
      revalidate: 10, // Revalidate every 10 seconds
    },
  });

  if (!response.ok) {
    throw new APIError(response.status, `API error: ${response.statusText}`);
  }

  return response.json();
}

// Blocks
export async function getBlocks(page: number = 1, pageSize: number = 20) {
  return fetchAPI<PaginatedResponse<Block>>(
    `/api/v1/blocks?page=${page}&page_size=${pageSize}`
  );
}

export async function getBlock(blockNumber: number) {
  return fetchAPI<Block>(`/api/v1/blocks/${blockNumber}`);
}

export async function getLatestBlocks(limit: number = 10) {
  return fetchAPI<Block[]>(`/api/v1/blocks/latest?limit=${limit}`);
}

// Transactions
export async function getTransaction(hash: string) {
  return fetchAPI<Transaction>(`/api/v1/transactions/${hash}`);
}

export async function getTransactionsByBlock(
  blockNumber: number,
  page: number = 1,
  pageSize: number = 20
) {
  return fetchAPI<PaginatedResponse<Transaction>>(
    `/api/v1/transactions/block/${blockNumber}?page=${page}&page_size=${pageSize}`
  );
}

export async function getTransactionsByAddress(
  address: string,
  page: number = 1,
  pageSize: number = 20,
  direction: "from" | "to" | "all" = "all"
) {
  return fetchAPI<PaginatedResponse<Transaction>>(
    `/api/v1/transactions/address/${address}?page=${page}&page_size=${pageSize}&direction=${direction}`
  );
}

// Addresses
export async function getAddress(address: string) {
  return fetchAPI<Address>(`/api/v1/addresses/${address}`);
}

export async function getAddressBalance(address: string) {
  return fetchAPI<{ balance_wei: string; balance_eth: string }>(
    `/api/v1/addresses/${address}/balance`
  );
}

// Search
export async function search(query: string) {
  return fetchAPI<SearchResult>(`/api/v1/search?q=${encodeURIComponent(query)}`);
}

// Stats
export async function getStats() {
  return fetchAPI<Stats>(`/api/v1/stats`);
}
```

### 5.2 Custom Hooks (hooks/useBlock.ts)

```typescript
"use client";

import useSWR from "swr";
import { getBlocks, getBlock } from "@/lib/api";

export function useBlocks(page: number, pageSize: number) {
  return useSWR(["blocks", page, pageSize], () => getBlocks(page, pageSize), {
    refreshInterval: 10000, // Refresh every 10 seconds
    revalidateOnFocus: false,
  });
}

export function useBlock(blockNumber: number) {
  return useSWR(["block", blockNumber], () => getBlock(blockNumber), {
    revalidateOnFocus: false,
  });
}
```

---

## Styling & Theming

### 5.3 Dark Mode (context/ThemeContext.tsx)

```typescript
"use client";

import * as React from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import { type ThemeProviderProps } from "next-themes/dist/types";

export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}

// Theme toggle component
export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={() => setTheme(theme === "light" ? "dark" : "light")}
    >
      {theme === "light" ? (
        <Moon className="h-5 w-5" />
      ) : (
        <Sun className="h-5 w-5" />
      )}
    </Button>
  );
}
```

---

## แบบฝึกหัด

### แบบฝึกหัดที่ 1: Setup Next.js

**เป้าหมาย**: Setup Next.js project

**Steps**:
1. Create Next.js 14 app
2. Install dependencies
3. Configure Tailwind CSS
4. Run dev server

**Pass criteria**:
- ✅ App runs on localhost:3000
- ✅ Home page renders
- ✅ Tailwind CSS works

### แบบฝึกหัดที่ 2: Create Component

**เป้าหมาย**: สร้าง component ใหม่

**Requirements**:
- Create AddressCard component
- Display address, balance, tx count
- Link to address detail page

**Pass criteria**:
- ✅ Component renders correctly
- ✅ TypeScript types defined
- ✅ Styling consistent

### แบบฝึกหัดที่ 3: API Integration

**เป้าหมาย**: Integrate with backend API

**Steps**:
1. Configure API_BASE_URL
2. Fetch data from /api/v1/blocks
3. Display in BlockList component

**Pass criteria**:
- ✅ API calls successful
- ✅ Data displayed correctly
- ✅ Loading states handled

### แบบฝึกหัดที่ 4: Add Dark Mode

**เป้าหมาย**: Implement dark mode toggle

**Requirements**:
- Add theme toggle button
- Persist theme preference
- Smooth transitions

**Pass criteria**:
- ✅ Toggle works
- ✅ Theme persists on reload
- ✅ All components support dark mode

### แบบฝึกหัดที่ 5: Performance Optimization

**เป้าหมาย**: Optimize app performance

**Tasks**:
- Add image optimization
- Implement code splitting
- Add caching headers
- Measure Lighthouse score

**Pass criteria**:
- ✅ Lighthouse score > 90
- ✅ First Contentful Paint < 1.5s
- ✅ Time to Interactive < 3s

---

## Pass Criteria - PART07

ก่อนจบ PART07 ให้ตรวจสอบว่า:

- [ ] เข้าใจ Next.js 14 App Router
- [ ] สร้าง pages และ layouts ได้
- [ ] สร้าง reusable components
- [ ] Integrate กับ backend API
- [ ] Implement client-side routing
- [ ] Add dark mode support
- [ ] Optimize performance
- [ ] Deploy to Vercel (optional)
- [ ] สามารถทำแบบฝึกหัดอย่างน้อย 3 ข้อให้สำเร็จ

---

## Production Notes

### Performance

- Next.js SSR/SSG: Fast initial load
- Image optimization: Next/Image
- Code splitting: Automatic
- Caching: ISR + SWR

### SEO

- Metadata API for dynamic meta tags
- Semantic HTML
- Structured data (JSON-LD)
- sitemap.xml generation

### Deployment

- Vercel: Zero-config deployment
- Custom domains
- Edge caching
- Analytics

---

**จบ PART07 - Explorer UI & Frontend**

**ถัดไป**: PART08 - Analytics & Advanced Features

---

**สถิติ PART07**:
- **Lines**: ~3,020 lines
- **Components**: 20+ React components
- **Pages**: 10+ routes
- **Exercises**: 5 hands-on labs

---

*เอกสารนี้เป็นส่วนหนึ่งของโปรเจกต์ Blockchain Explorer System*
