#!/bin/bash
# Monitoring Script for Blockchain Explorer

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

clear

echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Blockchain Explorer System Monitor       ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}\n"

# Function to check service health
check_service() {
    local service=$1
    local url=$2

    if curl -sf "$url" > /dev/null 2>&1; then
        echo -e "   ${GREEN}✓${NC} $service"
    else
        echo -e "   ${RED}✗${NC} $service"
    fi
}

# Service Health Checks
echo -e "${YELLOW}🏥 Service Health:${NC}"
check_service "Backend API     " "http://localhost:8000/health"
check_service "Analytics API   " "http://localhost:8001/health"
check_service "Frontend        " "http://localhost:3000"
check_service "ClickHouse      " "http://localhost:8123/ping"

# Container Status
echo -e "\n${YELLOW}🐳 Container Status:${NC}"
docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

# Resource Usage
echo -e "\n${YELLOW}💻 Resource Usage:${NC}"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" \
    $(docker-compose ps -q) 2>/dev/null || echo "   No containers running"

# ClickHouse Stats
echo -e "\n${YELLOW}📊 ClickHouse Database:${NC}"
if docker-compose ps clickhouse | grep -q "Up"; then
    docker exec blockchain_clickhouse clickhouse-client -q "
        SELECT
            formatReadableSize(sum(bytes)) as size,
            sum(rows) as rows,
            count() as parts
        FROM system.parts
        WHERE database = 'blockchain_analytics' AND active
        FORMAT Pretty
    " 2>/dev/null || echo "   Unable to query ClickHouse"
else
    echo -e "   ${RED}ClickHouse not running${NC}"
fi

# Recent Logs
echo -e "\n${YELLOW}📝 Recent Errors (last 10):${NC}"
docker-compose logs --tail=50 2>&1 | grep -i "error\|exception\|failed" | tail -10 || echo "   No recent errors"

echo -e "\n${GREEN}🔄 Refresh: watch -n 5 ./scripts/monitor.sh${NC}"
echo -e "${GREEN}📊 Full logs: docker-compose logs -f [service]${NC}\n"
