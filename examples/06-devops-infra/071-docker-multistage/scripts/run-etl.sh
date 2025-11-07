#!/bin/bash
# Run ETL Job

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

DATE_ARG="${1:-today}"

echo -e "${GREEN}🔄 Running ETL for: ${DATE_ARG}${NC}\n"

# Check if ClickHouse is running
if ! docker-compose ps clickhouse | grep -q "Up"; then
    echo -e "${YELLOW}⚠️  ClickHouse is not running. Starting it...${NC}"
    docker-compose up -d clickhouse
    echo -e "${YELLOW}⏳ Waiting for ClickHouse to be ready...${NC}"
    sleep 10
fi

# Run ETL with the specified date
docker-compose --profile etl run --rm etl python etl/blockchain_etl.py $DATE_ARG

echo -e "\n${GREEN}✅ ETL job completed!${NC}"

# Show some stats
echo -e "\n${YELLOW}📊 Recent Data:${NC}"
docker exec blockchain_clickhouse clickhouse-client \
    -q "SELECT date, block_count, total_transactions FROM blockchain_analytics.daily_blocks ORDER BY date DESC LIMIT 5 FORMAT Pretty"
