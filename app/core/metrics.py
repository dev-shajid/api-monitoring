"""
E-commerce specific metrics for Prometheus monitoring
"""
from prometheus_client import Counter, Histogram, Gauge, Summary
from app.core.config import settings

# Namespace for Prometheus metrics
NAMESPACE = settings.MONITORING_NAMESPACE

# Product search metrics
PRODUCT_SEARCHES = Counter(
    f"{NAMESPACE}_product_searches_total", 
    "Total count of product searches",
    ["category", "has_filters"]
)

PRODUCT_SEARCH_RESULTS = Histogram(
    f"{NAMESPACE}_product_search_results", 
    "Number of results returned by product searches",
    buckets=[0, 1, 2, 5, 10, 20, 50, 100]
)

PRODUCT_VIEWS = Counter(
    f"{NAMESPACE}_product_views_total",
    "Total count of individual product views",
    ["product_id", "category"]
)

# Filter usage metrics
FILTER_USAGE = Counter(
    f"{NAMESPACE}_filter_usage_total",
    "Total usage count of different filter types",
    ["filter_type"]
)

# Category metrics
CATEGORY_VIEWS = Counter(
    f"{NAMESPACE}_category_views_total",
    "Total count of category views",
    ["category"]
)

# Search performance
SEARCH_LATENCY = Histogram(
    f"{NAMESPACE}_search_latency_seconds",
    "Search operation latency in seconds",
    ["complexity"]  # 'simple' or 'complex' based on number of filters
)

# Zero results tracking
ZERO_RESULTS_SEARCHES = Counter(
    f"{NAMESPACE}_zero_results_searches_total",
    "Searches that returned zero results",
    ["query_type"]  # 'text', 'category', 'filter'
)