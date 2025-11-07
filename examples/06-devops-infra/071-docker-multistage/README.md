# 071. Docker Multi-Stage Deployment

> Production-Ready Docker Deployment for Complete Blockchain Explorer System ✅

## 📋 Overview

Complete Docker deployment solution for the entire Blockchain Explorer ecosystem using **multi-stage builds** for optimized images. This project provides:
- **Multi-stage Dockerfiles** for each component (minimal image sizes)
- **Docker Compose** orchestration for the complete system
- **Nginx reverse proxy** with load balancing
- **Deployment scripts** for easy management
- **Monitoring and cleanup tools**
- **Production-ready configuration**

## 🎯 Technologies

- **Docker**: 24.0+ (Multi-stage builds)
- **Docker Compose**: v2.0+
- **Nginx**: 1.25 (Reverse proxy)
- **Python**: 3.11 (Backend & Analytics)
- **Node.js**: 20 (Frontend)
- **ClickHouse**: 23.12 (Analytics database)

## 📊 Level

🔴 **Advanced**

## 💡 Features

### Multi-Stage Dockerfiles
- ✅ **Backend API** (FastAPI) - Optimized Python image
- ✅ **Frontend** (Next.js) - Standalone production build
- ✅ **Analytics** (ETL + API) - Minimal Python runtime
- ✅ Non-root users for security
- ✅ Health checks for all services
- ✅ Reduced image sizes (50-70% smaller)

### Docker Compose Orchestration
- ✅ Complete system with one command
- ✅ Service dependencies handled automatically
- ✅ Named volumes for data persistence
- ✅ Custom network configuration
- ✅ Environment variable management
- ✅ Profiles for optional services

### Nginx Reverse Proxy
- ✅ Single entry point for all services
- ✅ Rate limiting
- ✅ Gzip compression
- ✅ SSL/TLS ready
- ✅ Load balancing
- ✅ Health checks

### Deployment Scripts
- ✅ `deploy.sh` - Deploy full or partial system
- ✅ `run-etl.sh` - Execute ETL jobs
- ✅ `monitor.sh` - System monitoring
- ✅ `cleanup.sh` - Clean up resources

### Production Features
- ✅ Security best practices
- ✅ Resource limits
- ✅ Automatic restarts
- ✅ Log rotation
- ✅ Health monitoring
- ✅ Graceful shutdown

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Nginx (Port 80/443)                  │
│                   Reverse Proxy + SSL                   │
└────────────┬────────────────┬─────────────┬─────────────┘
             │                │             │
       ┌─────▼─────┐   ┌─────▼─────┐  ┌───▼────────┐
       │ Frontend  │   │  Backend  │  │ Analytics  │
       │  (Next.js)│   │ (FastAPI) │  │   API      │
       │  Port 3000│   │ Port 8000 │  │ Port 8001  │
       └───────────┘   └─────┬─────┘  └─────┬──────┘
                             │                │
                        ┌────▼────────────────▼─────┐
                        │     ClickHouse DB          │
                        │   Port 8123, 9000          │
                        └────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

```bash
# Docker & Docker Compose
docker --version        # Should be 24.0+
docker-compose --version  # Should be v2.0+

# Git (to clone the repo)
git --version
```

### 1. Navigate to Project

```bash
cd examples/06-devops-infra/071-docker-multistage
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

**Important `.env` settings:**
```bash
RPC_URL=http://host.docker.internal:8545  # For local blockchain
# OR
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY
```

### 3. Deploy

```bash
# Make scripts executable (if not already)
chmod +x scripts/*.sh

# Deploy full system
./scripts/deploy.sh

# Or deploy specific components
./scripts/deploy.sh backend
./scripts/deploy.sh frontend
./scripts/deploy.sh analytics
```

### 4. Verify Deployment

```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Monitor system
./scripts/monitor.sh
```

### 5. Access Services

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Analytics API**: http://localhost:8001
- **ClickHouse**: http://localhost:8123

## 📚 Detailed Usage

### Deployment Modes

**Full Deployment** (all core services):
```bash
./scripts/deploy.sh full
```

**Backend Only**:
```bash
./scripts/deploy.sh backend
```

**Frontend with Dependencies**:
```bash
./scripts/deploy.sh frontend
```

**Analytics Services**:
```bash
./scripts/deploy.sh analytics
```

**With Nginx Proxy**:
```bash
./scripts/deploy.sh with-proxy
# Access via http://localhost
```

**With Tabix UI** (ClickHouse web interface):
```bash
./scripts/deploy.sh with-ui
# Access via http://localhost:8080
```

### Running ETL Jobs

```bash
# ETL for today
./scripts/run-etl.sh today

# ETL for yesterday
./scripts/run-etl.sh yesterday

# ETL for specific date
./scripts/run-etl.sh 2024-01-15

# ETL for date range
./scripts/run-etl.sh 2024-01-01 2024-01-31
```

### Monitoring

```bash
# One-time status check
./scripts/monitor.sh

# Continuous monitoring (refresh every 5 seconds)
watch -n 5 ./scripts/monitor.sh

# View service logs
docker-compose logs -f [service_name]

# Examples:
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f analytics
```

### Cleanup

```bash
# Soft cleanup (stop containers)
./scripts/cleanup.sh soft

# Hard cleanup (stop + remove volumes)
./scripts/cleanup.sh hard

# Full cleanup (remove everything)
./scripts/cleanup.sh full

# Clear logs only
./scripts/cleanup.sh logs
```

## 🗂️ Project Structure

```
071-docker-multistage/
├── backend/
│   └── Dockerfile                 # FastAPI multi-stage build
├── frontend/
│   └── Dockerfile                 # Next.js multi-stage build
├── analytics/
│   └── Dockerfile                 # Analytics multi-stage build
├── nginx/
│   ├── nginx.conf                 # Nginx configuration
│   └── ssl/                       # SSL certificates (optional)
├── scripts/
│   ├── deploy.sh                  # Deployment script
│   ├── run-etl.sh                 # ETL runner
│   ├── monitor.sh                 # Monitoring script
│   └── cleanup.sh                 # Cleanup script
├── docker-compose.yml             # Orchestration config
├── .env.example                   # Environment template
└── README.md                      # This file
```

## 🐳 Docker Images

### Image Sizes (Approximate)

**Before Multi-Stage:**
- Backend: ~1.2 GB
- Frontend: ~1.5 GB
- Analytics: ~1.2 GB
- **Total: ~3.9 GB**

**After Multi-Stage:**
- Backend: ~400 MB (67% reduction)
- Frontend: ~500 MB (67% reduction)
- Analytics: ~400 MB (67% reduction)
- **Total: ~1.3 GB (67% savings)**

### Building Images Manually

```bash
# Backend
docker build -f backend/Dockerfile \
  -t blockchain-backend:latest \
  ../../03-backend-api/031-block-api

# Frontend
docker build -f frontend/Dockerfile \
  -t blockchain-frontend:latest \
  ../../04-frontend-ui/046-block-list

# Analytics
docker build -f analytics/Dockerfile \
  -t blockchain-analytics:latest \
  ../../05-data-analytics/061-daily-stats
```

## 🔧 Configuration

### Environment Variables

**`.env` file:**
```bash
# Blockchain
RPC_URL=http://localhost:8545

# ClickHouse
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=

# Debug
DEBUG=false

# Domain (for production)
DOMAIN=your-domain.com
```

### Docker Compose Profiles

**Default** (core services):
- clickhouse
- backend
- frontend
- analytics

**ETL Profile**:
```bash
docker-compose --profile etl run etl
```

**Proxy Profile**:
```bash
docker-compose --profile proxy up -d
```

**UI Profile**:
```bash
docker-compose --profile ui up -d
```

### Nginx Configuration

Edit `nginx/nginx.conf` to customize:
- Rate limiting
- SSL/TLS settings
- Caching rules
- Proxy timeouts
- CORS headers

## 🔒 Security Features

### Multi-Stage Builds
- Separate build and runtime stages
- No build tools in production images
- Minimal attack surface

### Non-Root Users
All services run as non-root:
```dockerfile
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
```

### Resource Limits
Configure in `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1G
    reservations:
      cpus: '0.5'
      memory: 512M
```

### Network Isolation
Custom network with subnet:
```yaml
networks:
  blockchain_net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### Health Checks
All services have health checks:
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"
```

## 📊 Performance Optimization

### Build Optimization
- Layer caching for dependencies
- `.dockerignore` for unnecessary files
- Multi-stage builds for size reduction

### Runtime Optimization
- Gunicorn with multiple workers
- Connection pooling
- Gzip compression in Nginx
- Static file caching

### Database Optimization
- ClickHouse partitioning
- Materialized views
- Proper indexes

## 🎯 Production Deployment

### 1. Prepare Server

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Enable Docker service
sudo systemctl enable docker
sudo systemctl start docker
```

### 2. Clone Repository

```bash
git clone <repository-url>
cd blockchain_ecosystem/examples/06-devops-infra/071-docker-multistage
```

### 3. Configure Production

```bash
# Edit .env with production settings
nano .env

# Set production RPC URL
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY

# Disable debug
DEBUG=false

# Set domain
DOMAIN=your-domain.com
```

### 4. SSL/TLS Setup

```bash
# Generate SSL certificate (Let's Encrypt)
sudo apt-get install certbot
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates
mkdir -p nginx/ssl
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/key.pem

# Enable HTTPS in nginx.conf
nano nginx/nginx.conf
# Uncomment HTTPS server block
```

### 5. Deploy with Proxy

```bash
./scripts/deploy.sh with-proxy
```

### 6. Set Up Monitoring

```bash
# Add to crontab for periodic monitoring
crontab -e

# Add line:
*/5 * * * * /path/to/scripts/monitor.sh >> /var/log/blockchain-monitor.log
```

### 7. Set Up ETL Cron Job

```bash
# Add to crontab
crontab -e

# Run ETL daily at 2 AM
0 2 * * * /path/to/scripts/run-etl.sh yesterday
```

## 🐛 Troubleshooting

### Problem: Containers Won't Start

```bash
# Check logs
docker-compose logs

# Check specific service
docker-compose logs backend

# Restart service
docker-compose restart backend
```

### Problem: Port Already in Use

```bash
# Find process using port
sudo lsof -i :3000
sudo lsof -i :8000

# Kill process or change port in docker-compose.yml
```

### Problem: Build Fails

```bash
# Clear Docker cache
docker builder prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check Dockerfile syntax
docker build -f backend/Dockerfile --check .
```

### Problem: Can't Connect to Blockchain

```bash
# For local blockchain, use host.docker.internal
RPC_URL=http://host.docker.internal:8545

# Test connection from container
docker-compose exec backend curl $RPC_URL -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

### Problem: Out of Memory

```bash
# Check container memory usage
docker stats

# Increase Docker memory limit
# Docker Desktop -> Settings -> Resources -> Memory

# Or set limits in docker-compose.yml
```

### Problem: ClickHouse Connection Failed

```bash
# Check ClickHouse logs
docker-compose logs clickhouse

# Verify ClickHouse is running
curl http://localhost:8123/ping

# Restart ClickHouse
docker-compose restart clickhouse
```

## 📈 Scaling

### Horizontal Scaling

```yaml
# In docker-compose.yml
backend:
  deploy:
    replicas: 3

# Use docker swarm or Kubernetes for production scaling
```

### Load Balancing

Nginx automatically load balances across replicas:
```nginx
upstream backend_api {
    server backend:8000 max_fails=3 fail_timeout=30s;
    # Add more servers here
}
```

### Database Replication

Set up ClickHouse replication:
```sql
-- Create replicated table
CREATE TABLE daily_blocks_replicated
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/daily_blocks', '{replica}')
PARTITION BY toYYYYMM(date)
ORDER BY date;
```

## ✅ Pass Criteria

1. ✅ All Dockerfiles build successfully
2. ✅ Multi-stage builds reduce image sizes
3. ✅ Docker Compose starts all services
4. ✅ Services can communicate with each other
5. ✅ Health checks pass for all services
6. ✅ Frontend accessible at port 3000
7. ✅ Backend API accessible at port 8000
8. ✅ Analytics API accessible at port 8001
9. ✅ ETL job runs successfully
10. ✅ Nginx proxy works (if enabled)
11. ✅ All scripts execute without errors

## 🎓 What You'll Learn

- ✅ Docker multi-stage builds
- ✅ Docker Compose orchestration
- ✅ Nginx reverse proxy configuration
- ✅ Container networking
- ✅ Volume management
- ✅ Health checks and monitoring
- ✅ Security best practices
- ✅ Production deployment strategies
- ✅ Resource optimization
- ✅ Bash scripting for DevOps

## 🚀 Next Steps

### 1. Add CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy
on: push
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and Deploy
        run: |
          docker-compose build
          docker-compose up -d
```

### 2. Add Monitoring Stack

```bash
# Add Prometheus + Grafana
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```

### 3. Kubernetes Migration

```bash
# Generate Kubernetes manifests
kompose convert -f docker-compose.yml
```

### 4. Add Logging Stack

```yaml
# ELK Stack (Elasticsearch, Logstash, Kibana)
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
  logstash:
    image: docker.elastic.co/logstash/logstash:8.10.0
  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
```

## 📚 Related Projects

This deployment includes:
- **031-block-api**: Backend API
- **046-block-list**: Frontend UI
- **061-daily-stats**: Analytics System

## 🎉 Summary

This project completes the **10 priority projects** for the Blockchain Explorer ecosystem:

1. ✅ 001-basic-erc20 - ERC-20 Token
2. ✅ 002-erc721-nft - NFT Contract
3. ✅ 004-dex-amm - DEX/AMM
4. ✅ 016-web3py-basic - Web3.py Basics
5. ✅ 017-send-eth - Send ETH
6. ✅ 018-erc20-interact - ERC-20 Interaction
7. ✅ 031-block-api - Backend API
8. ✅ 046-block-list - Frontend UI
9. ✅ 061-daily-stats - Analytics
10. ✅ **071-docker-multistage - Docker Deployment** ✨

**Total Achievement: 10/10 Priority Projects (100%)** 🎉

---

**License**: MIT
**Version**: 1.0.0
**Docker Compose Version**: 3.8
**Status**: Production Ready ✅
