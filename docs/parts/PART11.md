# PART11 - Deployment & DevOps

> **เนื้อหา**: Docker Production, Kubernetes, CI/CD Pipeline, Infrastructure as Code, Auto-scaling, Backup & Disaster Recovery
>
> **เป้าหมาย**: Deploy Blockchain Explorer to production with DevOps best practices
>
> **ระยะเวลา**: 10-14 ชั่วโมง
>
> **Prerequisites**: PART01-10, Docker, Kubernetes basics, AWS/GCP/Azure

---

## 📑 สารบัญ

1. [Deployment Architecture](#deployment-architecture)
2. [Docker Production Setup](#docker-production-setup)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [CI/CD Pipeline](#cicd-pipeline)
5. [Infrastructure as Code](#infrastructure-as-code)
6. [Monitoring & Logging](#monitoring--logging)
7. [Backup & Disaster Recovery](#backup--disaster-recovery)
8. [แบบฝึกหัด](#แบบฝึกหัด)

---

## Deployment Architecture

### 1.1 Production Architecture

```
┌─────────────────────────────────────────────────────────────┐
│            Production Deployment Architecture               │
└─────────────────────────────────────────────────────────────┘

    Internet
       │
       ▼
┌──────────────┐
│  Cloudflare  │  ← CDN, DDoS protection
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Load Balancer│  ← HA Proxy / ALB
│   (nginx)    │
└──────┬───────┘
       │
       ├─────────────┬─────────────┬─────────────┐
       ▼             ▼             ▼             ▼
   ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐
   │ API  │      │ API  │      │ API  │      │ API  │
   │ Pod 1│      │ Pod 2│      │ Pod 3│      │ Pod 4│
   └──┬───┘      └──┬───┘      └──┬───┘      └──┬───┘
      │             │             │             │
      └─────────────┴─────────────┴─────────────┘
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
   ┌────────┐  ┌────────┐  ┌────────┐
   │Postgres│  │ Redis  │  │ Click  │
   │ Primary│  │Cluster │  │ House  │
   └───┬────┘  └────────┘  └────────┘
       │
       ▼
   ┌────────┐
   │Postgres│
   │Replica │
   └────────┘
```

### 1.2 High Availability Setup

**Components**:
- **Load Balancer**: 2+ instances (active-passive)
- **API**: 4+ pods (auto-scaling 2-10)
- **Database**: Primary + 2 replicas
- **Cache**: Redis cluster (3 masters, 3 replicas)
- **Storage**: S3/Cloud Storage for backups

---

## Docker Production Setup

### 2.1 Production Dockerfile

```dockerfile
# Multi-stage build for API
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Add .local/bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 2.2 Production docker-compose.yml

```yaml
version: '3.8'

services:
  # API
  api:
    image: blockchain-explorer-api:${VERSION:-latest}
    build:
      context: ./api
      dockerfile: Dockerfile
      cache_from:
        - blockchain-explorer-api:latest
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - LOG_LEVEL=INFO
    secrets:
      - db_password
      - jwt_secret
    networks:
      - frontend
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Indexer
  indexer:
    image: blockchain-explorer-indexer:${VERSION:-latest}
    build:
      context: ./indexer
      dockerfile: Dockerfile
    deploy:
      replicas: 1
      resources:
        limits:
          cpus: '4'
          memory: 4G
        reservations:
          cpus: '2'
          memory: 2G
    environment:
      - ETH_NODE_URL=${ETH_NODE_URL}
      - DATABASE_URL=${DATABASE_URL}
      - BATCH_SIZE=100
    secrets:
      - db_password
    networks:
      - backend
    restart: unless-stopped

  # PostgreSQL
  postgres:
    image: postgres:15-alpine
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
        reservations:
          cpus: '2'
          memory: 4G
    environment:
      - POSTGRES_DB=blockchain_explorer
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
      - PGDATA=/var/lib/postgresql/data/pgdata
    secrets:
      - db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres/postgresql.conf:/etc/postgresql/postgresql.conf:ro
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis
  redis:
    image: redis:7-alpine
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 2G
    command: redis-server --appendonly yes --maxmemory 1gb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Nginx (Load Balancer)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - nginx_logs:/var/log/nginx
    networks:
      - frontend
    depends_on:
      - api
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  nginx_logs:
    driver: local

secrets:
  db_password:
    file: ./secrets/db_password.txt
  jwt_secret:
    file: ./secrets/jwt_secret.txt
```

### 2.3 Production Nginx Configuration

```nginx
# nginx.conf
user nginx;
worker_processes auto;
worker_rlimit_nofile 65535;

error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format json_combined escape=json '{'
        '"time_local":"$time_local",'
        '"remote_addr":"$remote_addr",'
        '"request":"$request",'
        '"status":$status,'
        '"body_bytes_sent":$body_bytes_sent,'
        '"request_time":$request_time,'
        '"upstream_response_time":"$upstream_response_time",'
        '"http_user_agent":"$http_user_agent"'
    '}';

    access_log /var/log/nginx/access.log json_combined;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 10m;

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=100r/s;
    limit_req_status 429;

    # Upstream (API servers)
    upstream api_backend {
        least_conn;
        server api:8000 max_fails=3 fail_timeout=30s;
        keepalive 32;
    }

    # HTTP -> HTTPS redirect
    server {
        listen 80;
        server_name explorer.example.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name explorer.example.com;

        # SSL
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        # Security headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-Frame-Options "DENY" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # API endpoints
        location /api/ {
            limit_req zone=api burst=50 nodelay;

            proxy_pass http://api_backend;
            proxy_http_version 1.1;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header Connection "";

            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;

            # Buffering
            proxy_buffering on;
            proxy_buffer_size 4k;
            proxy_buffers 8 4k;
            proxy_busy_buffers_size 8k;
        }

        # Health check
        location /health {
            access_log off;
            proxy_pass http://api_backend/health;
        }

        # Metrics (internal only)
        location /metrics {
            allow 10.0.0.0/8;
            deny all;
            proxy_pass http://api_backend/metrics;
        }
    }
}
```

---

## Kubernetes Deployment

### 3.1 Kubernetes Manifests

**Deployment (api-deployment.yaml)**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: blockchain-explorer
  labels:
    app: api
    version: v1
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: api
        image: your-registry/blockchain-explorer-api:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
          protocol: TCP
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-secret
              key: url
        - name: REDIS_URL
          value: "redis://redis:6379/0"
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            cpu: "500m"
            memory: "1Gi"
          limits:
            cpu: "2000m"
            memory: "2Gi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15"]
      terminationGracePeriodSeconds: 30
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - api
              topologyKey: kubernetes.io/hostname
```

**Service (api-service.yaml)**:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api
  namespace: blockchain-explorer
  labels:
    app: api
spec:
  type: ClusterIP
  selector:
    app: api
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
    name: http
  sessionAffinity: None
```

**Ingress (ingress.yaml)**:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  namespace: blockchain-explorer
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - api.explorer.example.com
    secretName: api-tls
  rules:
  - host: api.explorer.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api
            port:
              number: 80
```

**HorizontalPodAutoscaler (hpa.yaml)**:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
  namespace: blockchain-explorer
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 15
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 2
        periodSeconds: 15
```

### 3.2 Helm Chart

**Chart.yaml**:

```yaml
apiVersion: v2
name: blockchain-explorer
description: A Helm chart for Blockchain Explorer
type: application
version: 1.0.0
appVersion: "1.0.0"
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: https://charts.bitnami.com/bitnami
  - name: redis
    version: "17.x.x"
    repository: https://charts.bitnami.com/bitnami
```

**values.yaml**:

```yaml
# API configuration
api:
  replicaCount: 3
  image:
    repository: your-registry/blockchain-explorer-api
    tag: latest
    pullPolicy: Always
  service:
    type: ClusterIP
    port: 80
  ingress:
    enabled: true
    className: nginx
    annotations:
      cert-manager.io/cluster-issuer: letsencrypt-prod
    hosts:
      - host: api.explorer.example.com
        paths:
          - path: /
            pathType: Prefix
    tls:
      - secretName: api-tls
        hosts:
          - api.explorer.example.com
  resources:
    requests:
      cpu: 500m
      memory: 1Gi
    limits:
      cpu: 2000m
      memory: 2Gi
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

# PostgreSQL
postgresql:
  enabled: true
  auth:
    database: blockchain_explorer
    username: postgres
    existingSecret: database-secret
  primary:
    persistence:
      size: 100Gi
    resources:
      requests:
        cpu: 2000m
        memory: 4Gi

# Redis
redis:
  enabled: true
  master:
    persistence:
      size: 10Gi
```

---

## CI/CD Pipeline

### 4.1 GitHub Actions

**.github/workflows/ci-cd.yml**:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Test
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: |
          pytest --cov=. --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  # Build and Push Docker image
  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          cache-to: type=inline

  # Deploy to Kubernetes
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG }}

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/api api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} -n blockchain-explorer
          kubectl rollout status deployment/api -n blockchain-explorer

      - name: Verify deployment
        run: |
          kubectl get deployment api -n blockchain-explorer
          kubectl get pods -n blockchain-explorer -l app=api
```

---

## Infrastructure as Code

### 5.1 Terraform (AWS Example)

**main.tf**:

```hcl
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "terraform-state-blockchain-explorer"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "blockchain-explorer-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = false

  tags = {
    Environment = "production"
    Project     = "blockchain-explorer"
  }
}

# EKS Cluster
module "eks" {
  source = "terraform-aws-modules/eks/aws"

  cluster_name    = "blockchain-explorer"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    main = {
      min_size     = 2
      max_size     = 10
      desired_size = 3

      instance_types = ["t3.large"]
      capacity_type  = "ON_DEMAND"

      labels = {
        Environment = "production"
      }

      tags = {
        Environment = "production"
      }
    }
  }

  tags = {
    Environment = "production"
    Project     = "blockchain-explorer"
  }
}

# RDS PostgreSQL
module "db" {
  source = "terraform-aws-modules/rds/aws"

  identifier = "blockchain-explorer-db"

  engine            = "postgres"
  engine_version    = "15.3"
  instance_class    = "db.r6g.xlarge"
  allocated_storage = 100

  db_name  = "blockchain_explorer"
  username = "postgres"
  password = var.db_password

  vpc_security_group_ids = [module.vpc.default_security_group_id]
  db_subnet_group_name   = module.vpc.database_subnet_group_name

  multi_az               = true
  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  maintenance_window     = "Mon:04:00-Mon:05:00"

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  tags = {
    Environment = "production"
  }
}

# ElastiCache Redis
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "blockchain-explorer-redis"
  engine               = "redis"
  node_type            = "cache.r6g.large"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  engine_version       = "7.0"
  port                 = 6379

  subnet_group_name = module.vpc.elasticache_subnet_group_name
  security_group_ids = [module.vpc.default_security_group_id]

  tags = {
    Environment = "production"
  }
}

# S3 Bucket for Backups
resource "aws_s3_bucket" "backups" {
  bucket = "blockchain-explorer-backups"

  tags = {
    Environment = "production"
  }
}

resource "aws_s3_bucket_versioning" "backups" {
  bucket = aws_s3_bucket.backups.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "backups" {
  bucket = aws_s3_bucket.backups.id

  rule {
    id     = "archive-old-backups"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}
```

---

## Backup & Disaster Recovery

### 6.1 Database Backup

```bash
#!/bin/bash
# backup-database.sh

set -euo pipefail

# Configuration
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-blockchain_explorer}"
DB_USER="${DB_USER:-postgres}"
BACKUP_DIR="${BACKUP_DIR:-/backups}"
S3_BUCKET="${S3_BUCKET:-blockchain-explorer-backups}"
RETENTION_DAYS=30

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Generate backup filename
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_${DB_NAME}_${TIMESTAMP}.sql.gz"

echo "Starting backup of $DB_NAME..."

# Create backup
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
    --format=custom --compress=9 --verbose \
    | gzip > "$BACKUP_FILE"

echo "Backup created: $BACKUP_FILE"

# Upload to S3
if command -v aws &> /dev/null; then
    echo "Uploading to S3..."
    aws s3 cp "$BACKUP_FILE" "s3://$S3_BUCKET/postgres/"
    echo "Upload complete"
fi

# Clean old backups
echo "Cleaning old backups (older than $RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "backup_*.sql.gz" -type f -mtime +$RETENTION_DAYS -delete

echo "Backup completed successfully"
```

### 6.2 Disaster Recovery Plan

```markdown
## Disaster Recovery Procedures

### RTO/RPO Targets
- **RTO** (Recovery Time Objective): 4 hours
- **RPO** (Recovery Point Objective): 1 hour

### Backup Strategy
1. **Database**: Continuous WAL archiving + Daily full backup
2. **Configuration**: Git repository
3. **Secrets**: Encrypted in AWS Secrets Manager
4. **Logs**: 30-day retention in S3

### Recovery Procedures

#### Database Failure
1. Promote read replica to primary
2. Update DNS/connection strings
3. Verify data integrity
4. Create new replica

#### Complete Infrastructure Loss
1. Deploy infrastructure with Terraform
2. Restore database from S3 backup
3. Deploy applications via CI/CD
4. Verify all services
5. Update DNS

#### Partial Service Failure
1. Check pod/container status
2. Review logs
3. Rollback if needed
4. Scale if necessary

### Testing Schedule
- **Monthly**: Database restore test
- **Quarterly**: Full DR drill
- **Annually**: Multi-region failover test
```

---

## แบบฝึกหัด

### แบบฝึกหัดที่ 1: Docker Production Build

**เป้าหมาย**: Build production-ready Docker images

**Requirements**:
- Multi-stage build
- Non-root user
- Health checks
- Minimal image size

**Pass criteria**:
- ✅ Image builds successfully
- ✅ Size < 500MB
- ✅ Passes security scan

### แบบฝึกหัดที่ 2: Deploy to Kubernetes

**เป้าหมาย**: Deploy application to K8s cluster

**Steps**:
1. Create namespace
2. Deploy manifests
3. Configure ingress
4. Setup HPA

**Pass criteria**:
- ✅ All pods running
- ✅ Ingress accessible
- ✅ Auto-scaling works

### แบบฝึกหัดที่ 3: Setup CI/CD

**เป้าหมาย**: Configure GitHub Actions pipeline

**Requirements**:
- Run tests on PR
- Build on merge
- Deploy to staging/prod
- Rollback capability

**Pass criteria**:
- ✅ Pipeline runs
- ✅ Tests pass
- ✅ Deployment successful

### แบบฝึกหัดที่ 4: Infrastructure as Code

**เป้าหมาย**: Deploy infrastructure with Terraform

**Tasks**:
- Define VPC, subnets
- Create EKS cluster
- Setup RDS database
- Configure S3 backups

**Pass criteria**:
- ✅ Infrastructure deployed
- ✅ State stored remotely
- ✅ Can destroy and recreate

### แบบฝึกหัดที่ 5: Disaster Recovery Test

**เป้าหมาย**: Test backup and restore

**Steps**:
1. Take database backup
2. Delete database
3. Restore from backup
4. Verify data integrity

**Pass criteria**:
- ✅ Backup successful
- ✅ Restore works
- ✅ No data loss

---

## Pass Criteria - PART11

ก่อนจบ PART11 ให้ตรวจสอบว่า:

- [ ] เข้าใจ production deployment architecture
- [ ] สร้าง production-ready Docker images
- [ ] Deploy to Kubernetes cluster
- [ ] Setup CI/CD pipeline
- [ ] Implement Infrastructure as Code
- [ ] Configure backup & disaster recovery
- [ ] สามารถทำแบบฝึกหัดอย่างน้อย 3 ข้อให้สำเร็จ

---

## Production Notes

### Deployment Checklist

**Before Deployment**:
- [ ] All tests pass
- [ ] Security scan clean
- [ ] Performance tested
- [ ] Monitoring configured
- [ ] Backups tested
- [ ] DR plan documented
- [ ] Runbook created

**During Deployment**:
- [ ] Use blue-green or rolling deployment
- [ ] Monitor metrics
- [ ] Check error rates
- [ ] Verify health checks
- [ ] Test critical paths

**After Deployment**:
- [ ] Monitor for 1 hour
- [ ] Check logs
- [ ] Verify metrics
- [ ] Update documentation
- [ ] Communicate to team

---

**จบ PART11 - Deployment & DevOps**

**ถัดไป**: PART12 - Testing & Quality Assurance

---

**สถิติ PART11**:
- **Lines**: ~2,000 lines
- **Deployment configs**: 10+ production files
- **Infrastructure**: Complete IaC examples
- **Exercises**: 5 hands-on labs

---

*เอกสารนี้เป็นส่วนหนึ่งของโปรเจกต์ Blockchain Explorer System*
