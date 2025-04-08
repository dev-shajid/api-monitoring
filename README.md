# API Monitoring Project

This project demonstrates a FastAPI-based e-commerce API with comprehensive monitoring using Prometheus and Grafana, along with Loki for log aggregation.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Monitoring](#monitoring)
- [Architecture](#architecture)
- [Metrics](#metrics)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

The API Monitoring project provides a foundation for implementing observability in modern web applications. It combines:

- A FastAPI application serving an e-commerce API
- Prometheus metrics collection with custom business metrics
- Grafana dashboards for visualization
- Loki for centralized logging
- Docker-based deployment for easy setup

This setup allows you to monitor not only technical metrics like request counts and latencies but also business-specific metrics like product searches, filter usage patterns, and zero-result searches.

## Features

### API Features
- Product search with multiple filters (category, price, brand, etc.)
- Product details by ID
- Category, subcategory, brand, and color listings
- Health and status endpoints

### Monitoring Features
- Request count and latency metrics
- Error tracking and categorization
- Business metrics for e-commerce operations
- Structured logging with Loki integration
- Ready-to-use Grafana dashboards

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.9+](https://www.python.org/downloads/) (for local development)
- [Git](https://git-scm.com/downloads) (optional)

### Installation

1. Clone or download the repository:
   ```bash
   git clone https://github.com/dev-shajid/api-monitoring.git
   cd api-monitoring
   ```

2. Create environment file:
   ```bash
   cp .env.example .env
   ```

3. Start the services using Docker Compose:
   ```bash
   docker-compose up -d
   ```

   This will start:
   - FastAPI application on port 8000
   - Prometheus on port 9090
   - Grafana on port 3000
   - Loki on port 3100

### Configuration

The application is configured using environment variables defined in the `.env` file:

- `ENVIRONMENT`: Development or production mode
- `LOG_LEVEL`: Logging verbosity (INFO, DEBUG, etc.)
- `LOKI_ENABLED`: Enable/disable Loki logging
- `METRICS_ENABLED`: Enable/disable Prometheus metrics
- `MONITORING_NAMESPACE`: Prefix for all metrics

## Usage

### API Endpoints

After starting the services, the following endpoints are available:

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Metrics**: http://localhost:8000/metrics
- **Product Search**: http://localhost:8000/products
- **Product Details**: http://localhost:8000/products/{id}
- **Categories**: http://localhost:8000/products/categories

Example API calls:

```bash
# Get all products
curl http://localhost:8000/products

# Search with filters
curl http://localhost:8000/products?category=Electronics&min_price=300

# Get product details
curl http://localhost:8000/products/1
```

### Monitoring

- **Prometheus**: http://localhost:9090
  - Query metrics using PromQL
  - Check targets and scrape status

- **Grafana**: http://localhost:3000 (username: admin, password: admin)
  - Import dashboards for API monitoring
  - Create custom visualizations
  - Set up alerts

- **Loki**: Accessed through Grafana
  - Query logs using LogQL
  - Filter by status code, endpoint, or error type

## Architecture

The project consists of the following components:

1. **FastAPI Application**:
   - Core API functionality
   - Middleware for metrics collection
   - Structured logging

2. **Prometheus**:
   - Metrics scraping and storage
   - Time-series database

3. **Grafana**:
   - Visualization platform
   - Dashboard creation
   - Alerts configuration

4. **Loki**:
   - Log aggregation
   - Querying capabilities

5. **Node Exporter & cAdvisor**:
   - System-level metrics
   - Container metrics

## Metrics

The application exposes various metrics through the `/metrics` endpoint:

### Technical Metrics
- `api_requests_total`: Total number of HTTP requests
- `api_exceptions_total`: Total count of exceptions
- `api_request_duration_seconds`: Request latency histogram
- `api_active_requests`: Gauge of currently active requests

### Business Metrics
- `api_product_searches_total`: Product search count by category
- `api_product_search_results`: Histogram of search result counts
- `api_product_views_total`: Individual product view count
- `api_filter_usage_total`: Usage count of different filter types
- `api_category_views_total`: Category view count
- `api_search_latency_seconds`: Search operation latency
- `api_zero_results_searches_total`: Searches with no results

## Troubleshooting

### Common Issues

1. **Metrics not appearing in Prometheus**
   - Check if the API is accessible at http://localhost:8000/metrics
   - Verify Prometheus targets at http://localhost:9090/targets
   - Check the Prometheus configuration in `prometheus.yml`

2. **Logs not appearing in Loki**
   - Ensure Loki is running (`docker-compose ps`)
   - Check Loki status at http://localhost:8000/loki-status
   - Verify the Loki URL in the `.env` file

3. **Docker networking issues**
   - On macOS, ensure `host.docker.internal` resolves correctly
   - Check if the containers can communicate with each other

### Testing the Monitoring Setup

The application provides a special endpoint to generate errors for testing:

```bash
# Generate a random error
curl http://localhost:8000/error

# Generate a specific error type (value, key, type, runtime)
curl http://localhost:8000/error?type=value
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Submit a pull request

Please ensure your code follows the project's style and includes appropriate tests.

---

Built with ❤️ using FastAPI, Prometheus, Grafana, and Loki