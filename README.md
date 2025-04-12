# API Monitoring Project

A FastAPI-based e-commerce API with comprehensive monitoring using Prometheus, Grafana, Jaeger, and Loki.

## Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [Monitoring Setup](#monitoring-setup)
- [API Usage](#api-usage)
- [Troubleshooting](#troubleshooting)

## Features

- FastAPI e-commerce endpoints with product search and filtering
- Comprehensive monitoring stack:
  - Prometheus for metrics collection
  - Grafana for metrics visualization
  - Jaeger for distributed tracing
  - Loki for log aggregation
- Docker-based deployment
- Custom business metrics and traces

## Quick Start

1. Clone and setup:
```bash
git clone https://github.com/dev-shajid/api-monitoring.git
cd api-monitoring
cp .env.example .env
```

2. Start services:
```bash
docker-compose up -d
```

3. Access services:
- API & Docs: http://localhost:8000/docs
- Grafana: http://localhost:3000 (admin/admin)
- Jaeger UI: http://localhost:16686
- Prometheus: http://localhost:9090

## Local Development Setup

1. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the FastAPI application:
```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Or using Python directly
python -m app.main
```

4. For local development, ensure:
- Docker services are running (Prometheus, Grafana, Jaeger)
- Environment variables are properly set in `.env`
- Python 3.9+ is installed
- Virtual environment is activated

### Development Requirements

```txt
fastapi>=0.68.0
uvicorn>=0.15.0
prometheus-client>=0.11.0
opentelemetry-api>=1.11.1
opentelemetry-sdk>=1.11.1
opentelemetry-instrumentation-fastapi>=0.30b1
opentelemetry-exporter-jaeger>=1.11.1
python-dotenv>=0.19.0
```

## Monitoring Setup

### 1. Grafana Dashboards

- Access the pre-configured E-commerce dashboard:
  http://localhost:3000/goto/TYiDMs0Hg?orgId=1

Dashboard includes:
- Request rates and latencies
- Error rates by type
- Product search metrics
- Resource utilization
- Log correlation

### 2. Jaeger Distributed Tracing

Access Jaeger UI: http://localhost:16686

Key features:
- Search traces by:
  - Service: "ecommerce-api"
  - Operation: Specific endpoints
  - Tags: Error types, status codes
  - Time range

Generate sample traces:
```bash
# Normal operations
curl http://localhost:8000/products
curl http://localhost:8000/products/1
curl http://localhost:8000/health

# Error traces
curl http://localhost:8000/error?type=value
curl http://localhost:8000/error?type=runtime
```

Understanding traces:
- Each trace shows complete request flow
- Spans show operation timing
- Error details and stack traces
- Request/response parameters
- Custom attributes

### 3. Metrics (Prometheus)

Available metrics:

Technical:
- `api_requests_total`: Request count by endpoint
- `api_exceptions_total`: Exception count by type
- `api_request_duration_seconds`: Request latency
- `api_active_requests`: Current request count

Business:
- `api_product_searches_total`: Search count by category
- `api_product_views_total`: Product view count
- `api_filter_usage_total`: Filter usage patterns
- `api_search_latency_seconds`: Search performance

### 4. Logging (Loki)

Access through Grafana:
1. Click "Explore"
2. Select "Loki" data source
3. Query logs using LogQL

Example queries:
```logql
{container="api"} |= "error"
{container="api"} | json | status_code >= 400
```

## API Usage

Key endpoints:
```bash
# Product operations
GET /products                   # List products
GET /products/{id}             # Get product details
GET /products/categories       # List categories

# Monitoring
GET /metrics                   # Prometheus metrics
GET /health                    # Health check
GET /error?type=value         # Generate test error
```

Search with filters:
```bash
curl "http://localhost:8000/products?category=Electronics&min_price=300"
```

## Troubleshooting

### Common Issues

1. **No Traces in Jaeger**
   - Check Jaeger is running: `docker ps | grep jaeger`
   - Check app logs for connection errors

2. **Missing Metrics in Grafana**
   - Ensure Prometheus is running and scraping
   - Check data source configuration in Grafana
   - Verify metrics endpoint: http://localhost:8000/metrics

3. **Docker Networking**
   - Verify host.docker.internal resolution
   - Check container connectivity
   - Inspect container logs

### Monitoring Health Check

1. Generate test data:
```bash
# Generate requests
for i in {1..10}; do curl http://localhost:8000/products; done

# Generate errors
curl http://localhost:8000/error
```

2. Verify monitoring:
- Check Jaeger for traces
- View Grafana dashboard
- Query Prometheus metrics
- Search logs in Loki

### Environment Variables

Key configurations in `.env`:
```env
ENVIRONMENT=development
LOG_LEVEL=INFO
METRICS_ENABLED=true
MONITORING_NAMESPACE=api
```

---

Built with FastAPI, Prometheus, Grafana, Jaeger, and Loki 📊

For more details, check the [API Documentation](http://localhost:8000/docs)