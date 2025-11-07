.PHONY: help setup start-clickhouse stop-clickhouse etl-today etl-yesterday api clean

help:
	@echo "Blockchain Analytics - Available Commands:"
	@echo ""
	@echo "  make setup              - Install Python dependencies"
	@echo "  make start-clickhouse   - Start ClickHouse with Docker Compose"
	@echo "  make stop-clickhouse    - Stop ClickHouse"
	@echo "  make etl-today          - Run ETL for today"
	@echo "  make etl-yesterday      - Run ETL for yesterday"
	@echo "  make api                - Start Analytics API"
	@echo "  make clean              - Clean up containers and data"
	@echo ""

setup:
	pip install -r requirements.txt
	cp .env.example .env
	@echo "✅ Setup complete. Edit .env file with your configuration."

start-clickhouse:
	docker-compose up -d
	@echo "⏳ Waiting for ClickHouse to be ready..."
	@sleep 5
	@echo "✅ ClickHouse is running at http://localhost:8123"
	@echo "   Tabix UI: http://localhost:8080"

stop-clickhouse:
	docker-compose down

etl-today:
	python etl/blockchain_etl.py today

etl-yesterday:
	python etl/blockchain_etl.py yesterday

api:
	uvicorn api.analytics_api:app --host 0.0.0.0 --port 8001 --reload

clean:
	docker-compose down -v
	rm -rf __pycache__ etl/__pycache__ api/__pycache__
