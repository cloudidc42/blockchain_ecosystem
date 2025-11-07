#!/bin/bash
# Blockchain Explorer Deployment Script

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Blockchain Explorer Deployment Script    ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}\n"

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ Created .env file. Please edit it with your configuration.${NC}"
    echo -e "${YELLOW}⏸  Pausing deployment. Edit .env and run this script again.${NC}"
    exit 0
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

echo -e "${GREEN}📋 Deployment Configuration:${NC}"
echo -e "   RPC URL: ${RPC_URL}"
echo -e "   Debug Mode: ${DEBUG:-false}"
echo -e ""

# Parse command line arguments
MODE="${1:-full}"

case $MODE in
    "full")
        echo -e "${GREEN}🚀 Starting full deployment (all services)...${NC}\n"

        echo -e "${YELLOW}1️⃣  Building Docker images...${NC}"
        docker-compose build

        echo -e "\n${YELLOW}2️⃣  Starting services...${NC}"
        docker-compose up -d

        echo -e "\n${YELLOW}3️⃣  Waiting for services to be healthy...${NC}"
        sleep 10

        echo -e "\n${GREEN}✅ Deployment complete!${NC}"
        ;;

    "backend")
        echo -e "${GREEN}🚀 Starting backend services only...${NC}\n"
        docker-compose up -d clickhouse backend
        echo -e "\n${GREEN}✅ Backend services started!${NC}"
        ;;

    "frontend")
        echo -e "${GREEN}🚀 Starting frontend with dependencies...${NC}\n"
        docker-compose up -d clickhouse backend analytics frontend
        echo -e "\n${GREEN}✅ Frontend services started!${NC}"
        ;;

    "analytics")
        echo -e "${GREEN}🚀 Starting analytics services...${NC}\n"
        docker-compose up -d clickhouse analytics
        echo -e "\n${GREEN}✅ Analytics services started!${NC}"
        ;;

    "with-proxy")
        echo -e "${GREEN}🚀 Starting with Nginx reverse proxy...${NC}\n"
        docker-compose --profile proxy up -d
        echo -e "\n${GREEN}✅ All services with proxy started!${NC}"
        ;;

    "with-ui")
        echo -e "${GREEN}🚀 Starting with Tabix UI...${NC}\n"
        docker-compose --profile ui up -d
        echo -e "\n${GREEN}✅ All services with UI started!${NC}"
        ;;

    *)
        echo -e "${RED}❌ Unknown mode: $MODE${NC}"
        echo -e "Available modes:"
        echo -e "  full        - Start all core services (default)"
        echo -e "  backend     - Start backend API only"
        echo -e "  frontend    - Start frontend with dependencies"
        echo -e "  analytics   - Start analytics services"
        echo -e "  with-proxy  - Start with Nginx reverse proxy"
        echo -e "  with-ui     - Start with Tabix UI"
        exit 1
        ;;
esac

echo -e "\n${GREEN}📊 Service Status:${NC}"
docker-compose ps

echo -e "\n${GREEN}🌐 Access Points:${NC}"
echo -e "   Frontend:      ${GREEN}http://localhost:3000${NC}"
echo -e "   Backend API:   ${GREEN}http://localhost:8000${NC}"
echo -e "   API Docs:      ${GREEN}http://localhost:8000/docs${NC}"
echo -e "   Analytics API: ${GREEN}http://localhost:8001${NC}"
echo -e "   ClickHouse:    ${GREEN}http://localhost:8123${NC}"

if docker-compose ps | grep -q "blockchain_nginx"; then
    echo -e "   Nginx Proxy:   ${GREEN}http://localhost${NC}"
fi

if docker-compose ps | grep -q "blockchain_tabix"; then
    echo -e "   Tabix UI:      ${GREEN}http://localhost:8080${NC}"
fi

echo -e "\n${YELLOW}💡 Useful Commands:${NC}"
echo -e "   View logs:    ${GREEN}docker-compose logs -f [service]${NC}"
echo -e "   Stop all:     ${GREEN}docker-compose down${NC}"
echo -e "   Restart:      ${GREEN}docker-compose restart [service]${NC}"
echo -e "   Run ETL:      ${GREEN}./scripts/run-etl.sh${NC}"
echo -e ""
