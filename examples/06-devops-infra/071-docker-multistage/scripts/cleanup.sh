#!/bin/bash
# Cleanup Script for Blockchain Explorer

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}╔════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║  Blockchain Explorer Cleanup Script       ║${NC}"
echo -e "${YELLOW}╚════════════════════════════════════════════╝${NC}\n"

# Parse arguments
MODE="${1:-soft}"

case $MODE in
    "soft")
        echo -e "${YELLOW}🧹 Soft cleanup: Stopping containers...${NC}"
        docker-compose down
        echo -e "${GREEN}✅ Containers stopped${NC}"
        ;;

    "hard")
        echo -e "${RED}⚠️  Hard cleanup: Stopping containers and removing volumes...${NC}"
        read -p "This will delete all data. Are you sure? (yes/no): " confirm

        if [ "$confirm" = "yes" ]; then
            docker-compose down -v
            echo -e "${GREEN}✅ Containers and volumes removed${NC}"
        else
            echo -e "${YELLOW}Cancelled${NC}"
            exit 0
        fi
        ;;

    "full")
        echo -e "${RED}⚠️  Full cleanup: Removing everything including images...${NC}"
        read -p "This will delete all containers, volumes, and images. Are you sure? (yes/no): " confirm

        if [ "$confirm" = "yes" ]; then
            docker-compose down -v --rmi all
            echo -e "${GREEN}✅ Everything removed${NC}"

            # Clean up dangling images and volumes
            echo -e "${YELLOW}🧹 Cleaning up Docker system...${NC}"
            docker system prune -f
            echo -e "${GREEN}✅ Docker system cleaned${NC}"
        else
            echo -e "${YELLOW}Cancelled${NC}"
            exit 0
        fi
        ;;

    "logs")
        echo -e "${YELLOW}🧹 Cleaning up logs...${NC}"
        docker-compose logs --tail=0 > /dev/null 2>&1
        echo -e "${GREEN}✅ Logs cleared${NC}"
        ;;

    *)
        echo -e "${RED}❌ Unknown mode: $MODE${NC}"
        echo -e "\nAvailable modes:"
        echo -e "  soft  - Stop containers (default)"
        echo -e "  hard  - Stop containers and remove volumes (data loss!)"
        echo -e "  full  - Remove everything including images (complete cleanup!)"
        echo -e "  logs  - Clear logs only"
        exit 1
        ;;
esac

echo -e "\n${GREEN}💡 To restart: ./scripts/deploy.sh${NC}\n"
