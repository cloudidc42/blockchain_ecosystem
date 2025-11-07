# Multi-stage Dockerfile for Analytics ETL & API
# Stage 1: Builder
FROM python:3.11-slim as builder

LABEL maintainer="Blockchain Explorer Team"
LABEL description="Analytics ETL & API - Builder Stage"

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Stage 2: Runtime
FROM python:3.11-slim

LABEL maintainer="Blockchain Explorer Team"
LABEL description="Analytics ETL & API - Production"

# Create non-root user
RUN groupadd -r analytics && useradd -r -g analytics analytics

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY etl/ ./etl/
COPY api/ ./api/
COPY .env.example .env

# Create directories for logs and data
RUN mkdir -p /app/logs /app/data && \
    chown -R analytics:analytics /app

# Switch to non-root user
USER analytics

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/usr/local/bin:$PATH"

# Health check (for API)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8001/health')" || exit 1

# Expose port for API
EXPOSE 8001

# Default command runs the API
# For ETL, override with: docker run <image> python etl/blockchain_etl.py today
CMD ["gunicorn", "api.analytics_api:app", \
     "--workers", "2", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8001", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]
