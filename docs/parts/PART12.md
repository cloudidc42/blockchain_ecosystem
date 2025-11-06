# PART12 - Testing & Quality Assurance

> **เนื้อหา**: Unit Testing, Integration Testing, E2E Testing, Performance Testing, Load Testing, Test Coverage
>
> **เป้าหมาย**: สร้าง comprehensive testing strategy สำหรับ Blockchain Explorer
>
> **ระยะเวลา**: 10-12 ชั่วโมง
>
> **Prerequisites**: PART01-11, pytest, Jest, Playwright

---

## 📑 สารบัญ

1. [Testing Strategy](#testing-strategy)
2. [Unit Testing](#unit-testing)
3. [Integration Testing](#integration-testing)
4. [E2E Testing](#e2e-testing)
5. [Performance Testing](#performance-testing)
6. [Load Testing](#load-testing)
7. [Test Coverage & Quality](#test-coverage--quality)
8. [แบบฝึกหัด](#แบบฝึกหัด)

---

## Testing Strategy

### 1.1 Testing Pyramid

```
┌─────────────────────────────────────────────────────────────┐
│                    Testing Pyramid                          │
└─────────────────────────────────────────────────────────────┘

                    ┌──────────┐
                    │   E2E    │  ← 10% (Slow, Expensive)
                    └──────────┘
                ┌──────────────────┐
                │   Integration    │  ← 20% (Medium Speed)
                └──────────────────┘
        ┌──────────────────────────────┐
        │        Unit Tests            │  ← 70% (Fast, Cheap)
        └──────────────────────────────┘
```

### 1.2 Test Coverage Goals

- **Unit Tests**: 80%+ coverage
- **Integration Tests**: Critical paths covered
- **E2E Tests**: Happy paths + critical user journeys
- **Performance**: Response time < SLA
- **Load**: Handle peak traffic

### 1.3 Testing Tools

**Backend (Python)**:
- pytest: Unit & integration testing
- pytest-cov: Coverage reporting
- pytest-asyncio: Async testing
- Locust: Load testing

**Frontend (TypeScript)**:
- Jest: Unit testing
- React Testing Library: Component testing
- Playwright: E2E testing
- Lighthouse: Performance testing

---

## Unit Testing

### 2.1 Python Unit Tests (Backend)

```python
"""Unit tests for block service."""
import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from services.block_service import BlockService
from models.block import Block


class TestBlockService:
    """Test suite for BlockService."""

    @pytest.fixture
    def mock_db(self):
        """Mock database session."""
        return Mock()

    @pytest.fixture
    def service(self, mock_db):
        """Create BlockService instance."""
        return BlockService(mock_db)

    def test_get_latest_blocks(self, service, mock_db):
        """Test getting latest blocks."""
        # Arrange
        mock_blocks = [
            Block(block_number=100, block_hash="0x123"),
            Block(block_number=99, block_hash="0x456"),
        ]
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = mock_blocks

        mock_db.query.return_value = mock_query

        # Act
        result = service.get_latest_blocks(limit=2)

        # Assert
        assert len(result) == 2
        assert result[0].block_number == 100
        mock_db.query.assert_called_once_with(Block)

    def test_get_block_by_number_found(self, service, mock_db):
        """Test getting block by number - found."""
        # Arrange
        expected_block = Block(block_number=100, block_hash="0x123")

        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = expected_block

        mock_db.query.return_value = mock_query

        # Act
        result = service.get_block_by_number(100)

        # Assert
        assert result == expected_block
        assert result.block_number == 100

    def test_get_block_by_number_not_found(self, service, mock_db):
        """Test getting block by number - not found."""
        # Arrange
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None

        mock_db.query.return_value = mock_query

        # Act
        result = service.get_block_by_number(999)

        # Assert
        assert result is None

    @pytest.mark.parametrize("block_number,expected_calls", [
        (100, 1),
        (200, 1),
        (0, 1),
    ])
    def test_get_block_various_numbers(
        self, service, mock_db, block_number, expected_calls
    ):
        """Test getting blocks with various numbers."""
        # Arrange
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = Block(block_number=block_number)

        mock_db.query.return_value = mock_query

        # Act
        result = service.get_block_by_number(block_number)

        # Assert
        assert result.block_number == block_number
        assert mock_db.query.call_count == expected_calls
```

### 2.2 Async Tests

```python
"""Async unit tests."""
import pytest
import asyncio
from unittest.mock import AsyncMock, Mock

from indexer.indexer import BlockchainIndexer


@pytest.mark.asyncio
class TestBlockchainIndexer:
    """Test async indexer."""

    @pytest.fixture
    async def indexer(self):
        """Create indexer instance."""
        mock_web3 = Mock()
        indexer = BlockchainIndexer(mock_web3)
        yield indexer

    @pytest.mark.asyncio
    async def test_process_block_success(self, indexer):
        """Test successful block processing."""
        # Arrange
        mock_block = {
            'number': 100,
            'hash': '0x123',
            'transactions': []
        }

        indexer.block_extractor.get_block = AsyncMock(return_value=mock_block)
        indexer.block_processor.process_block = AsyncMock()

        # Act
        await indexer.process_block(100)

        # Assert
        indexer.block_extractor.get_block.assert_called_once_with(100)
        indexer.block_processor.process_block.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_block_error_handling(self, indexer):
        """Test error handling in block processing."""
        # Arrange
        indexer.block_extractor.get_block = AsyncMock(
            side_effect=Exception("Network error")
        )

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await indexer.process_block(100)

        assert "Network error" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_concurrent_processing(self, indexer):
        """Test processing multiple blocks concurrently."""
        # Arrange
        blocks = [{'number': i, 'hash': f'0x{i}'} for i in range(10)]

        indexer.block_extractor.get_block = AsyncMock(
            side_effect=blocks
        )
        indexer.block_processor.process_block = AsyncMock()

        # Act
        tasks = [indexer.process_block(i) for i in range(10)]
        await asyncio.gather(*tasks)

        # Assert
        assert indexer.block_extractor.get_block.call_count == 10
```

### 2.3 TypeScript Unit Tests (Frontend)

```typescript
// BlockCard.test.tsx
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import BlockCard from '@/components/blocks/BlockCard';
import { Block } from '@/lib/types';

describe('BlockCard', () => {
  const mockBlock: Block = {
    blockNumber: 12345,
    blockHash: '0xabcdef1234567890',
    parentHash: '0x9876543210fedcba',
    timestamp: 1700000000,
    miner: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb8',
    gasLimit: 30000000,
    gasUsed: 15000000,
    transactionCount: 150,
  };

  it('renders block number correctly', () => {
    render(<BlockCard block={mockBlock} />);

    expect(screen.getByText('#12,345')).toBeInTheDocument();
  });

  it('displays gas usage percentage', () => {
    render(<BlockCard block={mockBlock} />);

    // Gas usage: 15M / 30M = 50%
    expect(screen.getByText('50.0%')).toBeInTheDocument();
  });

  it('formats miner address', () => {
    render(<BlockCard block={mockBlock} />);

    // Should show shortened address
    expect(screen.getByText(/0x742d...0bEb8/)).toBeInTheDocument();
  });

  it('links to block detail page', () => {
    render(<BlockCard block={mockBlock} />);

    const link = screen.getByRole('link', { name: /#12,345/ });
    expect(link).toHaveAttribute('href', '/blocks/12345');
  });

  it('displays transaction count badge', () => {
    render(<BlockCard block={mockBlock} />);

    expect(screen.getByText('150')).toBeInTheDocument();
  });
});

// Hook tests
import { renderHook, waitFor } from '@testing-library/react';
import { useBlocks } from '@/hooks/useBlock';

describe('useBlocks', () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it('fetches blocks successfully', async () => {
    const mockData = {
      items: [mockBlock],
      total: 1,
      page: 1,
      totalPages: 1,
    };

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    });

    const { result } = renderHook(() => useBlocks(1, 20));

    await waitFor(() => {
      expect(result.current.data).toEqual(mockData);
    });
  });

  it('handles fetch error', async () => {
    (global.fetch as jest.Mock).mockRejectedValueOnce(
      new Error('Network error')
    );

    const { result } = renderHook(() => useBlocks(1, 20));

    await waitFor(() => {
      expect(result.current.error).toBeDefined();
    });
  });
});
```

---

## Integration Testing

### 3.1 API Integration Tests

```python
"""API integration tests."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import get_db, Base
from models.block import Block


# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture
def db():
    """Create test database."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    """Create test client."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def test_get_blocks_empty(client):
    """Test getting blocks when database is empty."""
    response = client.get("/api/v1/blocks/")

    assert response.status_code == 200
    data = response.json()
    assert data['items'] == []
    assert data['total'] == 0


def test_get_blocks_with_data(client, db):
    """Test getting blocks with data."""
    # Create test blocks
    blocks = [
        Block(block_number=i, block_hash=f"0x{i}", parent_hash=f"0x{i-1}",
              timestamp=1700000000+i, miner="0x123", gas_limit=30000000,
              gas_used=15000000, transaction_count=10)
        for i in range(1, 11)
    ]
    db.add_all(blocks)
    db.commit()

    # Test
    response = client.get("/api/v1/blocks/?page=1&page_size=5")

    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) == 5
    assert data['total'] == 10
    assert data['page'] == 1
    assert data['totalPages'] == 2


def test_get_block_by_number(client, db):
    """Test getting single block."""
    # Create test block
    block = Block(
        block_number=100,
        block_hash="0xabc",
        parent_hash="0x999",
        timestamp=1700000000,
        miner="0x123",
        gas_limit=30000000,
        gas_used=15000000,
        transaction_count=10
    )
    db.add(block)
    db.commit()

    # Test
    response = client.get("/api/v1/blocks/100")

    assert response.status_code == 200
    data = response.json()
    assert data['blockNumber'] == 100
    assert data['blockHash'] == "0xabc"


def test_get_block_not_found(client):
    """Test getting non-existent block."""
    response = client.get("/api/v1/blocks/999999")

    assert response.status_code == 404


def test_rate_limiting(client):
    """Test rate limiting."""
    # Make 101 requests (assuming limit is 100)
    responses = []
    for _ in range(101):
        response = client.get("/api/v1/blocks/")
        responses.append(response.status_code)

    # Last request should be rate limited
    assert responses[-1] == 429
```

### 3.2 Database Integration Tests

```python
"""Database integration tests."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import Base
from models.block import Block
from models.transaction import Transaction


@pytest.fixture
def db_session():
    """Create test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()


def test_create_block(db_session):
    """Test creating a block."""
    block = Block(
        block_number=1,
        block_hash="0x123",
        parent_hash="0x000",
        timestamp=1700000000,
        miner="0xabc",
        gas_limit=30000000,
        gas_used=15000000,
        transaction_count=5
    )

    db_session.add(block)
    db_session.commit()

    # Query back
    queried_block = db_session.query(Block).filter_by(block_number=1).first()

    assert queried_block is not None
    assert queried_block.block_hash == "0x123"


def test_block_transaction_relationship(db_session):
    """Test block-transaction relationship."""
    # Create block
    block = Block(
        block_number=1,
        block_hash="0x123",
        parent_hash="0x000",
        timestamp=1700000000,
        miner="0xabc",
        gas_limit=30000000,
        gas_used=15000000,
        transaction_count=2
    )
    db_session.add(block)
    db_session.commit()

    # Create transactions
    tx1 = Transaction(
        transaction_hash="0xtx1",
        block_number=1,
        block_hash="0x123",
        transaction_index=0,
        timestamp=1700000000,
        from_address="0x111",
        to_address="0x222",
        value=1000000000000000000,
        gas_limit=21000,
        nonce=0
    )
    tx2 = Transaction(
        transaction_hash="0xtx2",
        block_number=1,
        block_hash="0x123",
        transaction_index=1,
        timestamp=1700000000,
        from_address="0x333",
        to_address="0x444",
        value=2000000000000000000,
        gas_limit=21000,
        nonce=0
    )

    db_session.add_all([tx1, tx2])
    db_session.commit()

    # Query transactions for block
    txs = db_session.query(Transaction).filter_by(block_number=1).all()

    assert len(txs) == 2
    assert txs[0].transaction_hash == "0xtx1"
    assert txs[1].transaction_hash == "0xtx2"
```

---

## E2E Testing

### 4.1 Playwright E2E Tests

```typescript
// e2e/blocks.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Blocks Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/blocks');
  });

  test('should display blocks list', async ({ page }) => {
    // Wait for blocks to load
    await page.waitForSelector('[data-testid="block-card"]');

    // Check if at least one block is displayed
    const blocks = await page.locator('[data-testid="block-card"]').count();
    expect(blocks).toBeGreaterThan(0);
  });

  test('should navigate to block detail', async ({ page }) => {
    // Click first block
    await page.click('[data-testid="block-card"]:first-child a');

    // Should navigate to detail page
    await page.waitForURL(/\/blocks\/\d+/);

    // Check if block details are displayed
    await expect(page.locator('h1')).toContainText('Block #');
  });

  test('should paginate blocks', async ({ page }) => {
    // Click next page
    await page.click('[aria-label="Next page"]');

    // URL should update
    await expect(page).toHaveURL(/page=2/);

    // Should load different blocks
    const firstBlockNumber = await page
      .locator('[data-testid="block-number"]')
      .first()
      .textContent();

    expect(firstBlockNumber).toBeTruthy();
  });

  test('should filter blocks', async ({ page }) => {
    // Enter miner address in filter
    await page.fill('[data-testid="miner-filter"]', '0x1234');

    // Click filter button
    await page.click('[data-testid="apply-filter"]');

    // Should show filtered results
    const miners = await page
      .locator('[data-testid="block-miner"]')
      .allTextContents();

    miners.forEach(miner => {
      expect(miner.toLowerCase()).toContain('0x1234');
    });
  });
});

test.describe('Transaction Detail', () => {
  test('should display transaction details', async ({ page }) => {
    // Go to specific transaction
    const txHash = '0x1234567890abcdef';
    await page.goto(`/tx/${txHash}`);

    // Check transaction hash
    await expect(page.locator('[data-testid="tx-hash"]'))
      .toContainText(txHash);

    // Check status badge
    await expect(page.locator('[data-testid="tx-status"]'))
      .toBeVisible();

    // Check from/to addresses
    await expect(page.locator('[data-testid="tx-from"]'))
      .toBeVisible();
    await expect(page.locator('[data-testid="tx-to"]'))
      .toBeVisible();
  });
});

test.describe('Search', () => {
  test('should search for block by number', async ({ page }) => {
    await page.goto('/');

    // Enter block number
    await page.fill('[data-testid="search-input"]', '12345');

    // Submit search
    await page.press('[data-testid="search-input"]', 'Enter');

    // Should navigate to block detail
    await expect(page).toHaveURL('/blocks/12345');
  });

  test('should search for transaction by hash', async ({ page }) => {
    await page.goto('/');

    const txHash = '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890';

    await page.fill('[data-testid="search-input"]', txHash);
    await page.press('[data-testid="search-input"]', 'Enter');

    await expect(page).toHaveURL(`/tx/${txHash}`);
  });

  test('should handle search not found', async ({ page }) => {
    await page.goto('/');

    await page.fill('[data-testid="search-input"]', 'invalid-query');
    await page.press('[data-testid="search-input"]', 'Enter');

    // Should show error message
    await expect(page.locator('[data-testid="error-message"]'))
      .toContainText('Not found');
  });
});
```

### 4.2 E2E Test Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'test-results/junit.xml' }]
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

---

## Performance Testing

### 5.1 Lighthouse CI

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI

on: [push]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v9
        with:
          urls: |
            http://localhost:3000
            http://localhost:3000/blocks
            http://localhost:3000/blocks/12345
          uploadArtifacts: true
          temporaryPublicStorage: true
```

**lighthouserc.json**:

```json
{
  "ci": {
    "collect": {
      "startServerCommand": "npm run start",
      "url": ["http://localhost:3000"]
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", {"minScore": 0.9}],
        "categories:accessibility": ["error", {"minScore": 0.9}],
        "categories:best-practices": ["error", {"minScore": 0.9}],
        "categories:seo": ["error", {"minScore": 0.9}]
      }
    },
    "upload": {
      "target": "temporary-public-storage"
    }
  }
}
```

### 5.2 API Performance Tests

```python
"""API performance tests."""
import pytest
import time
from statistics import mean, stdev

from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_api_response_time():
    """Test API response time."""
    response_times = []

    # Make 100 requests
    for _ in range(100):
        start = time.time()
        response = client.get("/api/v1/blocks/")
        elapsed = time.time() - start

        assert response.status_code == 200
        response_times.append(elapsed)

    # Calculate statistics
    avg_time = mean(response_times)
    std_time = stdev(response_times)
    max_time = max(response_times)

    print(f"\nResponse Time Statistics:")
    print(f"  Average: {avg_time*1000:.2f}ms")
    print(f"  Std Dev: {std_time*1000:.2f}ms")
    print(f"  Max: {max_time*1000:.2f}ms")

    # Assertions
    assert avg_time < 0.1, f"Average response time {avg_time}s exceeds 100ms"
    assert max_time < 0.5, f"Max response time {max_time}s exceeds 500ms"


def test_concurrent_requests():
    """Test handling concurrent requests."""
    import concurrent.futures

    def make_request():
        return client.get("/api/v1/blocks/")

    # Make 50 concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(make_request) for _ in range(50)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    # All should succeed
    assert all(r.status_code == 200 for r in results)
```

---

## Load Testing

### 6.1 Locust Load Tests

```python
"""Load testing with Locust."""
from locust import HttpUser, task, between
import random


class BlockchainExplorerUser(HttpUser):
    """Simulated user for load testing."""

    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks

    @task(3)
    def view_latest_blocks(self):
        """View latest blocks (most common action)."""
        self.client.get("/api/v1/blocks/")

    @task(2)
    def view_specific_block(self):
        """View specific block."""
        block_number = random.randint(1, 100000)
        self.client.get(f"/api/v1/blocks/{block_number}")

    @task(1)
    def search_transaction(self):
        """Search for transaction."""
        tx_hash = "0x" + "a" * 64
        self.client.get(f"/api/v1/transactions/{tx_hash}")

    @task(1)
    def view_address(self):
        """View address details."""
        address = "0x" + "b" * 40
        self.client.get(f"/api/v1/addresses/{address}")

    def on_start(self):
        """Called when user starts."""
        # Could do login here if needed
        pass
```

**Run Locust**:

```bash
# Run with web UI
locust -f load_tests.py --host=http://localhost:8000

# Headless mode (for CI)
locust -f load_tests.py \
  --host=http://localhost:8000 \
  --users 100 \
  --spawn-rate 10 \
  --run-time 5m \
  --headless \
  --only-summary
```

### 6.2 k6 Load Tests

```javascript
// k6-load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '1m', target: 50 },   // Ramp up
    { duration: '3m', target: 100 },  // Stay at 100
    { duration: '1m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% requests < 500ms
    errors: ['rate<0.1'],             // Error rate < 10%
  },
};

const BASE_URL = 'http://localhost:8000';

export default function () {
  // Test 1: Get latest blocks
  let res = http.get(`${BASE_URL}/api/v1/blocks/`);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  errorRate.add(res.status !== 200);

  sleep(1);

  // Test 2: Get specific block
  const blockNumber = Math.floor(Math.random() * 100000);
  res = http.get(`${BASE_URL}/api/v1/blocks/${blockNumber}`);
  check(res, {
    'status is 200 or 404': (r) => r.status === 200 || r.status === 404,
  });

  sleep(1);
}
```

---

## Test Coverage & Quality

### 7.1 Coverage Configuration

**pytest.ini**:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

addopts =
    --cov=.
    --cov-report=html
    --cov-report=xml
    --cov-report=term-missing
    --cov-fail-under=80
    -v
    --strict-markers
    --tb=short

markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    e2e: marks tests as end-to-end tests
```

**Run tests with coverage**:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_block_service.py

# Run with specific marker
pytest -m integration

# Run in parallel
pytest -n auto
```

### 7.2 Quality Metrics

```python
"""Code quality checks."""
# flake8, black, mypy, pylint

# Run all checks
def run_quality_checks():
    """Run all code quality checks."""
    import subprocess

    checks = [
        # Linting
        ["flake8", "."],

        # Type checking
        ["mypy", "app/"],

        # Code formatting
        ["black", "--check", "."],

        # Import sorting
        ["isort", "--check-only", "."],

        # Security
        ["bandit", "-r", "app/"],
    ]

    for check in checks:
        print(f"Running: {' '.join(check)}")
        result = subprocess.run(check)
        if result.returncode != 0:
            print(f"❌ {check[0]} failed")
            return False

    print("✅ All quality checks passed")
    return True
```

### 7.3 CI Test Pipeline

```yaml
# .github/workflows/test.yml
name: Test Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run linters
        run: |
          flake8 .
          black --check .
          mypy app/

      - name: Run unit tests
        run: pytest tests/unit --cov

      - name: Run integration tests
        run: pytest tests/integration --cov --cov-append

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          fail_ci_if_error: true

      - name: Generate coverage badge
        run: coverage-badge -o coverage.svg -f

      - name: Archive coverage results
        uses: actions/upload-artifact@v3
        with:
          name: coverage-report
          path: htmlcov/
```

---

## แบบฝึกหัด

### แบบฝึกหัดที่ 1: Write Unit Tests

**เป้าหมาย**: เขียน unit tests สำหรับ TransactionService

**Requirements**:
- Test get_transaction_by_hash
- Test get_transactions_by_block
- Test error handling
- Coverage > 80%

**Pass criteria**:
- ✅ All tests pass
- ✅ Coverage >= 80%
- ✅ No flaky tests

### แบบฝึกหัดที่ 2: Integration Testing

**เป้าหมาย**: เขียน integration tests สำหรับ API

**Requirements**:
- Test all major endpoints
- Test pagination
- Test filtering
- Test error cases

**Pass criteria**:
- ✅ All endpoints tested
- ✅ Tests pass consistently
- ✅ No database leaks

### แบบฝึกหัดที่ 3: E2E Testing

**เป้าหมาย**: เขียน E2E tests ด้วย Playwright

**Requirements**:
- Test user journey: Search → Block → Transaction
- Test responsive design
- Test accessibility

**Pass criteria**:
- ✅ Tests pass on all browsers
- ✅ Screenshots on failure
- ✅ Accessibility score > 90

### แบบฝึกหัดที่ 4: Performance Testing

**เป้าหมาย**: Run performance tests

**Requirements**:
- Lighthouse score > 90
- API response time < 200ms (p95)
- No memory leaks

**Pass criteria**:
- ✅ All metrics meet targets
- ✅ No performance regressions
- ✅ Report generated

### แบบฝึกหัดที่ 5: Load Testing

**เป้าหมาย**: Test system under load

**Requirements**:
- 100 concurrent users
- 5 minute duration
- Error rate < 1%

**Pass criteria**:
- ✅ System handles load
- ✅ Response times acceptable
- ✅ No errors

---

## Pass Criteria - PART12

ก่อนจบ PART12 ให้ตรวจสอบว่า:

- [ ] เข้าใจ testing pyramid และ strategy
- [ ] เขียน unit tests ได้ (coverage > 80%)
- [ ] เขียน integration tests
- [ ] เขียน E2E tests ด้วย Playwright
- [ ] Run performance tests
- [ ] Run load tests
- [ ] Setup CI/CD testing pipeline
- [ ] สามารถทำแบบฝึกหัดอย่างน้อย 3 ข้อให้สำเร็จ

---

## Production Notes

### Testing Checklist

**Before Release**:
- [ ] Unit test coverage > 80%
- [ ] All integration tests pass
- [ ] E2E tests pass on all browsers
- [ ] Performance tests meet SLA
- [ ] Load tests successful
- [ ] Security tests pass
- [ ] Accessibility score > 90

### Continuous Testing

**On Every Commit**:
- Run unit tests
- Run linters
- Check code coverage

**On Every PR**:
- Run full test suite
- Performance regression tests
- Security scan

**Nightly**:
- Full E2E test suite
- Load tests
- Integration tests

**Weekly**:
- Performance benchmarks
- Security audit
- Dependency updates

---

**จบ PART12 - Testing & Quality Assurance**

**ถัดไป**: TUTORIAL.md - Complete Step-by-Step Guide

---

**สถิติ PART12**:
- **Lines**: ~2,200 lines
- **Test examples**: 40+ complete tests
- **Testing tools**: 10+ frameworks covered
- **Exercises**: 5 hands-on labs

---

*เอกสารนี้เป็นส่วนหนึ่งของโปรเจกต์ Blockchain Explorer System*
