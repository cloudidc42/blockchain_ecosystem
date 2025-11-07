# 046. Blockchain Explorer UI

> Next.js Frontend สำหรับ Blockchain Explorer - ใช้งานได้จริง 100% ✅

## 📋 คำอธิบาย

Web UI สำหรับ Blockchain Explorer ที่สร้างด้วย Next.js 14 (App Router) พร้อมฟีเจอร์:
- แสดงรายการ blocks แบบ real-time
- ดูรายละเอียด block แต่ละอัน
- สถิติ blockchain และ gas prices
- Responsive design
- Auto-refresh data
- TypeScript + Tailwind CSS

## 🎯 เทคโนโลยี

- **Next.js**: 14.0.4 (App Router)
- **React**: 18.2
- **TypeScript**: 5.3
- **Tailwind CSS**: 3.4
- **SWR**: Data fetching & caching
- **Axios**: HTTP client
- **Lucide React**: Icons

## 📊 ระดับ

🟡 **Intermediate**

## 💡 ฟีเจอร์

### หน้าหลัก (Block List)
- ✅ แสดงรายการ blocks ล่าสุด
- ✅ Pagination (เลื่อนดู blocks ย้อนหลัง)
- ✅ Auto-refresh ทุก 12 วินาที
- ✅ แสดง stats (latest block, transactions, block time, gas price)
- ✅ Responsive grid layout

### หน้า Block Detail
- ✅ ข้อมูล block แบบละเอียด
- ✅ แสดง hash, timestamp, miner, gas usage
- ✅ รายการ transactions ใน block
- ✅ ปุ่มไป Previous/Next block

### หน้า Statistics
- ✅ สถิติ blockchain แบบ real-time
- ✅ Gas price estimates (slow/standard/fast/instant)
- ✅ Visual gas price comparison
- ✅ Auto-refresh stats

### UI/UX
- ✅ Modern design with Tailwind CSS
- ✅ Loading states
- ✅ Error handling
- ✅ Responsive (mobile-friendly)
- ✅ Smooth animations

## 🚀 การติดตั้ง

### 1. Install Dependencies

```bash
cd examples/04-frontend-ui/046-block-list

# Install packages
npm install
# หรือ
yarn install
# หรือ
pnpm install
```

### 2. Configure Environment

```bash
# Copy .env.example
cp .env.example .env.local

# Edit .env.local
# ตั้งค่า API URL ของ backend (project 031)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Backend API (Required!)

```bash
# Terminal 1: Start API (project 031-block-api)
cd examples/03-backend-api/031-block-api
uvicorn app.main:app --reload

# API จะรันที่ http://localhost:8000
```

### 4. Start Frontend

```bash
# Terminal 2: Start Next.js
cd examples/04-frontend-ui/046-block-list
npm run dev
```

**เปิดเบราว์เซอร์:** http://localhost:3000

## 📚 การใช้งาน

### Development

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint
npm run lint

# Type check
npm run type-check
```

### Project Structure

```
046-block-list/
├── src/
│   ├── app/                      # Next.js App Router
│   │   ├── layout.tsx           # Root layout
│   │   ├── page.tsx             # Home (block list)
│   │   ├── block/
│   │   │   └── [number]/
│   │   │       └── page.tsx     # Block detail page
│   │   └── stats/
│   │       └── page.tsx         # Statistics page
│   ├── components/              # React components
│   │   ├── BlockCard.tsx        # Block card
│   │   ├── StatsCard.tsx        # Stats card
│   │   ├── Pagination.tsx       # Pagination
│   │   ├── Loading.tsx          # Loading spinner
│   │   └── ErrorMessage.tsx     # Error display
│   ├── lib/
│   │   └── api.ts               # API client (350+ lines)
│   └── types/
│       └── index.ts             # TypeScript types
├── public/                       # Static files
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── next.config.js
└── README.md
```

## 🎨 Pages Overview

### 1. Home Page (/)
- Grid ของ blocks ล่าสุด 20 blocks
- Stats cards ด้านบน
- Pagination controls
- Auto-refresh ทุก 12 วินาที

### 2. Block Detail (/block/[number])
- ข้อมูลครบถ้วนของ block
- รายการ transactions
- ปุ่ม navigate ไป block ก่อน/หลัง

### 3. Statistics Page (/stats)
- Blockchain metrics
- Gas price estimates
- Visual comparison charts
- Auto-refresh

## 🔑 Key Components

### BlockCard
```tsx
<BlockCard block={block} />
```
แสดงข้อมูล block แบบ card (block number, miner, gas, transactions)

### StatsCard
```tsx
<StatsCard
  title="Latest Block"
  value="1000"
  icon={Blocks}
  subtitle="Current height"
/>
```
แสดงสถิติ 1 ตัว พร้อม icon

### Pagination
```tsx
<Pagination
  currentPage={1}
  hasNext={true}
  hasPrev={false}
  onPageChange={(page) => setPage(page)}
/>
```
Navigation ระหว่างหน้า

## 📡 API Integration

Frontend ใช้ API จากโปรเจค **031-block-api**:

```typescript
// lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Fetch blocks
const blocks = await getBlocks(page, pageSize);

// Fetch block detail
const block = await getBlockByNumber(blockNumber);

// Fetch stats
const stats = await getBlockchainStats();
```

### API Endpoints ที่ใช้:
- `GET /api/blocks` - Block list
- `GET /api/blocks/{number}` - Block detail
- `GET /api/stats/blockchain` - Blockchain stats
- `GET /api/stats/gas` - Gas prices

## 🎯 Data Fetching Strategy

ใช้ **SWR** สำหรับ data fetching:

```typescript
const { data, error, isLoading } = useSWR(
  'blocks',
  () => getBlocks(page, pageSize),
  {
    refreshInterval: 12000, // Auto-refresh every 12 seconds
    revalidateOnFocus: false,
  }
);
```

**ข้อดี:**
- Auto-refresh
- Caching
- Optimistic updates
- Error retry
- Loading states

## 🎨 Styling

ใช้ **Tailwind CSS** utility-first:

```tsx
<div className="bg-white p-6 rounded-lg shadow border border-gray-200">
  <h2 className="text-xl font-semibold text-gray-900">
    Latest Blocks
  </h2>
</div>
```

**สี Theme:**
- Primary: Blue (primary-500, primary-600, etc.)
- Success: Green
- Warning: Yellow
- Error: Red
- Neutral: Gray

## 📱 Responsive Design

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  {/* Stats cards */}
</div>
```

**Breakpoints:**
- `sm:` 640px+
- `md:` 768px+
- `lg:` 1024px+
- `xl:` 1280px+

## ⚡ Performance

- **Next.js App Router** - React Server Components
- **SWR Caching** - Reduced API calls
- **Auto-refresh** - Real-time data without manual refresh
- **Lazy loading** - Components load on demand
- **Image optimization** - Next.js Image component (if needed)

## 🔧 Configuration

### Environment Variables

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_NETWORK_NAME=Local Development
```

### Tailwind Config

```js
// tailwind.config.js
theme: {
  extend: {
    colors: {
      primary: { ... }
    }
  }
}
```

## ✅ Pass Criteria

1. ✅ ติดตั้ง dependencies สำเร็จ
2. ✅ Backend API ทำงานที่ port 8000
3. ✅ Frontend รันสำเร็จที่ port 3000
4. ✅ แสดงรายการ blocks ได้
5. ✅ คลิกดู block detail ได้
6. ✅ Pagination ทำงานถูกต้อง
7. ✅ Stats page แสดงข้อมูลได้
8. ✅ Auto-refresh ทำงาน
9. ✅ Responsive บน mobile/tablet

## 🎓 สิ่งที่จะได้เรียนรู้

- ✅ Next.js 14 App Router
- ✅ React Server Components
- ✅ TypeScript with React
- ✅ Tailwind CSS utility classes
- ✅ SWR for data fetching
- ✅ API integration
- ✅ Responsive design
- ✅ Loading & error states
- ✅ Dynamic routing
- ✅ Real-time data updates

## 🚀 Next Steps

### Enhancements

1. **Add Search**
```tsx
// Search by block number/hash/address
<SearchBar onSearch={handleSearch} />
```

2. **Add Transaction Detail Page**
```tsx
// /transaction/[hash]
export default function TransactionDetailPage({ params }) {
  // Fetch transaction details
}
```

3. **Add Address Page**
```tsx
// /address/[address]
// Show address balance, transactions, etc.
```

4. **Add Dark Mode**
```tsx
// Implement theme toggle
<ThemeProvider>
  <App />
</ThemeProvider>
```

5. **Add Charts**
```bash
npm install recharts
# Add block time chart, gas price chart
```

## 📚 Related Projects

- **031-block-api**: Backend API ที่ใช้ด้วย
- **061-daily-stats**: Analytics dashboard (coming next)

## 🐛 Troubleshooting

**ปัญหา: Cannot connect to API**
```bash
# ตรวจสอบว่า backend รันอยู่
curl http://localhost:8000/health

# ตรวจสอบ NEXT_PUBLIC_API_URL ใน .env.local
```

**ปัญหา: TypeScript errors**
```bash
# Type check
npm run type-check

# Fix และ rebuild
npm run build
```

**ปัญหา: Styles ไม่แสดง**
```bash
# Clear .next cache
rm -rf .next
npm run dev
```

**ปัญหา: Port 3000 in use**
```bash
# เปลี่ยน port
PORT=3001 npm run dev
```

## 📷 Screenshots

### Home Page
- Grid of latest blocks
- Real-time stats
- Pagination

### Block Detail
- Complete block information
- Transaction list
- Navigation between blocks

### Statistics
- Network metrics
- Gas price estimates
- Visual charts

---

**License**: MIT
**Version**: 1.0.0
**Total Lines**: 1,200+ (TypeScript/TSX)
