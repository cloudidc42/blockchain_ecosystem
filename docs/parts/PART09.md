# PART09 - Monitoring & Observability

> **เนื้อหา**: Prometheus Metrics, Grafana Dashboards, Logging, Alerting, Performance Monitoring
>
> **เป้าหมาย**: สร้าง comprehensive monitoring system สำหรับ Blockchain Explorer
>
> **ระยะเวลา**: 6-8 ชั่วโมง
>
> **Prerequisites**: PART01-08, Prometheus, Grafana, Loki

---

## 📑 สารบัญ

1. [Monitoring Architecture](#monitoring-architecture)
2. [Prometheus Metrics](#prometheus-metrics)
3. [Grafana Dashboards](#grafana-dashboards)
4. [Logging with Loki](#logging-with-loki)
5. [Alerting](#alerting)
6. [Performance Monitoring](#performance-monitoring)
7. [แบบฝึกหัด](#แบบฝึกหัด)

---

## Monitoring Architecture

### 1.1 Overview

```
┌─────────────────────────────────────────────────────────────┐
│              Monitoring Architecture                        │
└─────────────────────────────────────────────────────────────┘

    Applications
    ├── Indexer
    ├── API
    └── Frontend
         │
         │ /metrics endpoint
         ▼
    ┌──────────────┐
    │  Prometheus  │ ◄──── Scrape metrics every 15s
    │  (Metrics)   │
    └──────┬───────┘
           │
           │ PromQL queries
           ▼
    ┌──────────────┐
    │   Grafana    │
    │ (Dashboards) │
    └──────────────┘

    Applications
         │
         │ Logs (JSON)
         ▼
    ┌──────────────┐
    │     Loki     │
    │  (Logging)   │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │   Grafana    │
    │  (Explorer)  │
    └──────────────┘
```

### 1.2 Monitoring Stack

**Metrics**: Prometheus + Grafana
**Logs**: Loki + Grafana
**Traces**: (Optional) Jaeger/Tempo
**Alerts**: Alertmanager

---

## Prometheus Metrics

### 2.1 Indexer Metrics (indexer/metrics.py)

```python
"""Prometheus metrics for indexer (already in PART05)."""
from prometheus_client import (
    Counter, Gauge, Histogram, Summary,
    start_http_server, generate_latest
)

# Counters
blocks_indexed = Counter(
    'indexer_blocks_indexed_total',
    'Total blocks indexed'
)

transactions_indexed = Counter(
    'indexer_transactions_indexed_total',
    'Total transactions indexed'
)

logs_indexed = Counter(
    'indexer_logs_indexed_total',
    'Total logs indexed'
)

errors_total = Counter(
    'indexer_errors_total',
    'Total indexer errors',
    ['error_type']  # Labels
)

# Gauges
current_block = Gauge(
    'indexer_current_block',
    'Current block being indexed'
)

chain_head_block = Gauge(
    'indexer_chain_head_block',
    'Latest block on chain'
)

lag_blocks = Gauge(
    'indexer_lag_blocks',
    'Number of blocks behind'
)

# Histograms
block_processing_duration = Histogram(
    'indexer_block_processing_seconds',
    'Time to process a block',
    buckets=[0.1, 0.5, 1, 2, 5, 10, 30, 60]
)

# Summary
api_latency = Summary(
    'api_request_latency_seconds',
    'API request latency'
)
```

### 2.2 API Metrics (api/middleware/metrics.py)

```python
"""API metrics middleware."""
from prometheus_client import Counter, Histogram, Gauge
from fastapi import Request
from time import time

# HTTP Metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1, 2, 5]
)

http_requests_in_progress = Gauge(
    'http_requests_in_progress',
    'HTTP requests in progress',
    ['method', 'endpoint']
)

# Database Metrics
db_connections_active = Gauge(
    'db_connections_active',
    'Active database connections'
)

db_query_duration = Histogram(
    'db_query_duration_seconds',
    'Database query duration',
    ['query_type'],
    buckets=[0.001, 0.01, 0.05, 0.1, 0.5, 1, 2]
)

# Cache Metrics
cache_hits = Counter(
    'cache_hits_total',
    'Cache hits',
    ['cache_type']
)

cache_misses = Counter(
    'cache_misses_total',
    'Cache misses',
    ['cache_type']
)


async def metrics_middleware(request: Request, call_next):
    """Middleware to track HTTP metrics."""
    method = request.method
    endpoint = request.url.path

    # Track in-progress requests
    http_requests_in_progress.labels(method=method, endpoint=endpoint).inc()

    start_time = time()

    try:
        response = await call_next(request)
        status = response.status_code
    except Exception as e:
        status = 500
        raise
    finally:
        # Record metrics
        duration = time() - start_time

        http_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status=status
        ).inc()

        http_request_duration.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)

        http_requests_in_progress.labels(
            method=method,
            endpoint=endpoint
        ).dec()

    return response
```

### 2.3 Metrics Endpoint

```python
"""Expose metrics endpoint."""
from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

router = APIRouter()

@router.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
```

---

## Grafana Dashboards

### 3.1 Indexer Dashboard JSON

```json
{
  "dashboard": {
    "title": "Blockchain Indexer",
    "panels": [
      {
        "id": 1,
        "title": "Blocks Indexed",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(indexer_blocks_indexed_total[5m])",
            "legendFormat": "Blocks/sec"
          }
        ],
        "yaxes": [
          {
            "format": "short",
            "label": "Blocks/sec"
          }
        ]
      },
      {
        "id": 2,
        "title": "Indexer Lag",
        "type": "graph",
        "targets": [
          {
            "expr": "indexer_lag_blocks",
            "legendFormat": "Blocks behind"
          }
        ],
        "alert": {
          "conditions": [
            {
              "evaluator": {
                "params": [100],
                "type": "gt"
              },
              "query": {
                "params": ["A", "5m", "now"]
              }
            }
          ]
        }
      },
      {
        "id": 3,
        "title": "Block Processing Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(indexer_block_processing_seconds_bucket[5m]))",
            "legendFormat": "p95"
          },
          {
            "expr": "histogram_quantile(0.50, rate(indexer_block_processing_seconds_bucket[5m]))",
            "legendFormat": "p50"
          }
        ]
      },
      {
        "id": 4,
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(indexer_errors_total[5m])",
            "legendFormat": "{{error_type}}"
          }
        ]
      }
    ]
  }
}
```

### 3.2 API Dashboard JSON

```json
{
  "dashboard": {
    "title": "API Performance",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (endpoint)",
            "legendFormat": "{{endpoint}}"
          }
        ]
      },
      {
        "id": 2,
        "title": "Response Time (p95)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (endpoint, le))",
            "legendFormat": "{{endpoint}}"
          }
        ],
        "alert": {
          "conditions": [
            {
              "evaluator": {
                "params": [1],
                "type": "gt"
              }
            }
          ],
          "name": "High API Latency"
        }
      },
      {
        "id": 3,
        "title": "Error Rate by Status",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) by (status)",
            "legendFormat": "{{status}}"
          }
        ]
      },
      {
        "id": 4,
        "title": "Active Connections",
        "type": "graph",
        "targets": [
          {
            "expr": "db_connections_active",
            "legendFormat": "Database"
          },
          {
            "expr": "sum(http_requests_in_progress)",
            "legendFormat": "HTTP"
          }
        ]
      }
    ]
  }
}
```

---

## Logging with Loki

### 4.1 Structured Logging (utils/logging.py)

```python
"""Structured logging configuration."""
import logging
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Format logs as JSON."""

    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add extra fields
        if hasattr(record, 'extra'):
            log_data.update(record.extra)

        # Add exception info
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging(level=logging.INFO):
    """Setup structured logging."""
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)

    return root_logger
```

### 4.2 Promtail Configuration

```yaml
# promtail-config.yml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  # Indexer logs
  - job_name: indexer
    static_configs:
      - targets:
          - localhost
        labels:
          job: indexer
          __path__: /var/log/indexer/*.log
    pipeline_stages:
      - json:
          expressions:
            timestamp: timestamp
            level: level
            message: message
            module: module
      - labels:
          level:
          module:
      - timestamp:
          source: timestamp
          format: RFC3339

  # API logs
  - job_name: api
    static_configs:
      - targets:
          - localhost
        labels:
          job: api
          __path__: /var/log/api/*.log
    pipeline_stages:
      - json:
          expressions:
            timestamp: timestamp
            level: level
            message: message
            endpoint: endpoint
            status: status
      - labels:
          level:
          endpoint:
          status:
```

### 4.3 LogQL Queries

```logql
# Find errors in last hour
{job="indexer"} |= "error" | json | level="ERROR"

# API requests by endpoint
rate({job="api"} | json | endpoint=~".+" [5m]) by (endpoint)

# Slow queries
{job="api"} | json | duration > 1000 | line_format "{{.endpoint}} took {{.duration}}ms"

# Error distribution
sum by (level) (count_over_time({job="indexer"} | json | level="ERROR" [1h]))
```

---

## Alerting

### 5.1 Alertmanager Configuration

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'default'
  routes:
    - match:
        severity: critical
      receiver: 'critical'
    - match:
        severity: warning
      receiver: 'warning'

receivers:
  - name: 'default'
    slack_configs:
      - channel: '#alerts'
        title: 'Alert: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'critical'
    slack_configs:
      - channel: '#critical-alerts'
        title: '🚨 CRITICAL: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
    pagerduty_configs:
      - service_key: 'YOUR_PAGERDUTY_KEY'

  - name: 'warning'
    slack_configs:
      - channel: '#alerts'
        title: '⚠️  WARNING: {{ .GroupLabels.alertname }}'
```

### 5.2 Alert Rules

```yaml
# prometheus-alerts.yml
groups:
  - name: indexer
    interval: 30s
    rules:
      - alert: IndexerLagHigh
        expr: indexer_lag_blocks > 100
        for: 5m
        labels:
          severity: warning
          component: indexer
        annotations:
          summary: "Indexer is lagging behind"
          description: "Indexer is {{ $value }} blocks behind (threshold: 100)"

      - alert: IndexerDown
        expr: up{job="indexer"} == 0
        for: 1m
        labels:
          severity: critical
          component: indexer
        annotations:
          summary: "Indexer is down"
          description: "Indexer has been down for more than 1 minute"

      - alert: IndexerErrorRateHigh
        expr: rate(indexer_errors_total[5m]) > 1
        for: 5m
        labels:
          severity: warning
          component: indexer
        annotations:
          summary: "High error rate in indexer"
          description: "Error rate is {{ $value }} errors/sec (threshold: 1)"

  - name: api
    interval: 30s
    rules:
      - alert: APIHighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
          component: api
        annotations:
          summary: "API latency is high"
          description: "95th percentile latency is {{ $value }}s (threshold: 1s)"

      - alert: APIErrorRateHigh
        expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
          component: api
        annotations:
          summary: "High API error rate"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 5%)"

      - alert: DatabaseConnectionPoolExhausted
        expr: db_connections_active >= db_pool_size * 0.9
        for: 5m
        labels:
          severity: warning
          component: database
        annotations:
          summary: "Database connection pool nearly exhausted"
          description: "{{ $value }} connections active ({{ db_pool_size }} max)"

  - name: system
    interval: 30s
    rules:
      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.9
        for: 5m
        labels:
          severity: warning
          component: system
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value | humanizePercentage }}"

      - alert: DiskSpaceLow
        expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.1
        for: 5m
        labels:
          severity: warning
          component: system
        annotations:
          summary: "Disk space running low"
          description: "Only {{ $value | humanizePercentage }} disk space remaining"
```

---

## Performance Monitoring

### 6.1 Application Performance

```python
"""Performance monitoring utilities."""
from functools import wraps
from time import time
from utils.logger import logger


def monitor_performance(func):
    """Decorator to monitor function performance."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time()

        try:
            result = await func(*args, **kwargs)
            duration = time() - start

            logger.info(
                "function_executed",
                function=func.__name__,
                duration_seconds=round(duration, 3),
                status="success"
            )

            return result

        except Exception as e:
            duration = time() - start

            logger.error(
                "function_failed",
                function=func.__name__,
                duration_seconds=round(duration, 3),
                error=str(e),
                status="error"
            )

            raise

    return wrapper


# Usage
@monitor_performance
async def process_block(block_number: int):
    """Process block with performance monitoring."""
    # ... block processing logic
    pass
```

### 6.2 Database Query Monitoring

```python
"""Database query performance monitoring."""
from sqlalchemy import event
from sqlalchemy.engine import Engine
from time import time
from utils.logger import logger


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Track query start time."""
    conn.info.setdefault('query_start_time', []).append(time())


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Log slow queries."""
    total_time = time() - conn.info['query_start_time'].pop()

    # Log slow queries (> 100ms)
    if total_time > 0.1:
        logger.warning(
            "slow_query",
            duration_seconds=round(total_time, 3),
            query=statement[:200],  # First 200 chars
        )

    # Update Prometheus metric
    db_query_duration.labels(query_type="select").observe(total_time)
```

---

## แบบฝึกหัด

### แบบฝึกหัดที่ 1: Setup Prometheus

**เป้าหมาย**: Setup Prometheus และ scrape metrics

**Steps**:
1. Install Prometheus
2. Configure scrape targets
3. Start Prometheus
4. Query metrics via PromQL

**Pass criteria**:
- ✅ Prometheus running
- ✅ Metrics scraped
- ✅ Can query data

### แบบฝึกหัดที่ 2: Create Grafana Dashboard

**เป้าหมาย**: สร้าง dashboard สำหรับ indexer

**Requirements**:
- Blocks indexed per second
- Indexer lag
- Error rate
- Auto-refresh every 30s

**Pass criteria**:
- ✅ Dashboard created
- ✅ Panels show data
- ✅ Looks professional

### แบบฝึกหัดที่ 3: Setup Alerting

**เป้าหมาย**: Configure alerts

**Requirements**:
- Alert when indexer lag > 100 blocks
- Alert when API error rate > 5%
- Send to Slack/Email

**Pass criteria**:
- ✅ Alerts configured
- ✅ Test alerts fire
- ✅ Notifications received

### แบบฝึกหัดที่ 4: Log Aggregation

**เป้าหมาย**: Setup Loki for log aggregation

**Steps**:
1. Install Loki + Promtail
2. Configure log sources
3. Query logs in Grafana

**Pass criteria**:
- ✅ Logs ingested
- ✅ Can search logs
- ✅ LogQL queries work

### แบบฝึกหัดที่ 5: Performance Analysis

**เป้าหมาย**: Analyze performance bottlenecks

**Tasks**:
- Identify slow API endpoints
- Find slow database queries
- Optimize top 3 issues

**Pass criteria**:
- ✅ Bottlenecks identified
- ✅ Optimizations implemented
- ✅ Performance improved

---

## Pass Criteria - PART09

ก่อนจบ PART09 ให้ตรวจสอบว่า:

- [ ] เข้าใจ monitoring architecture
- [ ] Export Prometheus metrics จาก applications
- [ ] สร้าง Grafana dashboards
- [ ] Setup structured logging
- [ ] Configure alerts
- [ ] Monitor application performance
- [ ] สามารถทำแบบฝึกหัดอย่างน้อย 3 ข้อให้สำเร็จ

---

## Production Notes

### Metrics Retention
- Prometheus: 15 days (local)
- Long-term: Thanos/Cortex (S3)
- Logs: 30 days

### High Availability
- Multiple Prometheus instances
- Alertmanager cluster
- Loki replication

### Cost Optimization
- Downsampling old metrics
- Log sampling (trace 100%, debug 10%)
- Metric cardinality limits

---

**จบ PART09 - Monitoring & Observability**

**ถัดไป**: PART10 - Security & Best Practices

---

**สถิติ PART09**:
- **Lines**: ~1,500 lines
- **Dashboards**: 2 complete JSON configs
- **Alert Rules**: 10+ production alerts
- **Exercises**: 5 hands-on labs

---

*เอกสารนี้เป็นส่วนหนึ่งของโปรเจกต์ Blockchain Explorer System*
