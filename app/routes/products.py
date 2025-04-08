from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Query, HTTPException, Depends, Path
import logging
import time
from app.core.models import Product, ProductResponse, ProductSearchParams
from app.core.metrics import (
    PRODUCT_SEARCHES, 
    PRODUCT_SEARCH_RESULTS,
    PRODUCT_VIEWS,
    FILTER_USAGE,
    CATEGORY_VIEWS,
    SEARCH_LATENCY,
    ZERO_RESULTS_SEARCHES
)
from app.data.products import products

router = APIRouter()
logger = logging.getLogger("api")

# Get unique categories, subcategories, and brands for filtering options
CATEGORIES = sorted(list(set(p["category"] for p in products)))
SUBCATEGORIES = sorted(list(set(p["subcategory"] for p in products)))
BRANDS = sorted(list(set(p["brand"] for p in products)))
COLORS = sorted(list(set(color for p in products for color in p["color"])))

@router.get("/", response_model=ProductResponse, summary="Search products")
async def search_products(
    query: Optional[str] = None,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    color: Optional[str] = None,
    availability: Optional[bool] = None,
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Search for products with various filters
    
    - **query**: Text to search in product name and description
    - **category**: Filter by product category
    - **subcategory**: Filter by product subcategory
    - **brand**: Filter by product brand
    - **min_price**: Minimum price filter
    - **max_price**: Maximum price filter
    - **color**: Filter by color
    - **availability**: Filter by product availability
    - **min_rating**: Minimum product rating (0-5)
    - **limit**: Maximum number of results to return
    - **offset**: Number of results to skip (for pagination)
    """
    start_time = time.time()
    
    # Track which category is being searched
    search_category = category if category else "all"
    
    # Track if filters are being used
    has_filters = any([
        query, category, subcategory, brand, 
        min_price, max_price, color, 
        availability, min_rating
    ])
    
    # Record metric for product search
    PRODUCT_SEARCHES.labels(
        category=search_category,
        has_filters=str(has_filters)
    ).inc()
    
    # Record metrics for each filter type used
    if query:
        FILTER_USAGE.labels(filter_type="text_query").inc()
    if category:
        FILTER_USAGE.labels(filter_type="category").inc()
        CATEGORY_VIEWS.labels(category=category).inc()
    if subcategory:
        FILTER_USAGE.labels(filter_type="subcategory").inc()
    if brand:
        FILTER_USAGE.labels(filter_type="brand").inc()
    if min_price or max_price:
        FILTER_USAGE.labels(filter_type="price").inc()
    if color:
        FILTER_USAGE.labels(filter_type="color").inc()
    if availability is not None:
        FILTER_USAGE.labels(filter_type="availability").inc()
    if min_rating is not None:
        FILTER_USAGE.labels(filter_type="rating").inc()
    
    logger.info(f"🔍 Product search: query='{query}', category='{category}', brand='{brand}'")
    
    # Convert parameters to model
    params = ProductSearchParams(
        query=query,
        category=category,
        subcategory=subcategory,
        brand=brand,
        min_price=min_price,
        max_price=max_price,
        color=color,
        availability=availability,
        min_rating=min_rating
    )
    
    # Search products
    results = _search_products(params)
    
    # Track search performance (complexity based on number of filters used)
    search_complexity = "complex" if has_filters else "simple"
    SEARCH_LATENCY.labels(complexity=search_complexity).observe(time.time() - start_time)
    
    # Record the number of results
    PRODUCT_SEARCH_RESULTS.observe(len(results))
    
    # Track searches with zero results
    if len(results) == 0:
        if query:
            query_type = "text"
        elif category or subcategory:
            query_type = "category"
        else:
            query_type = "filter"
        ZERO_RESULTS_SEARCHES.labels(query_type=query_type).inc()
    
    # Apply pagination
    paginated_results = results[offset:offset + limit]
    
    # Convert to Pydantic models
    product_models = [Product(**product) for product in paginated_results]
    
    return ProductResponse(
        total=len(results),
        results=product_models
    )


def _search_products(params: ProductSearchParams):
    """
    Search products based on provided parameters
    """
    results = products.copy()
    
    # Text search in name and description
    if params.query:
        query = params.query.lower()
        results = [
            p for p in results 
            if query in p["name"].lower() or query in p["description"].lower()
        ]
    
    # Filter by category
    if params.category:
        results = [p for p in results if p["category"].lower() == params.category.lower()]
    
    # Filter by subcategory
    if params.subcategory:
        results = [p for p in results if p["subcategory"].lower() == params.subcategory.lower()]
    
    # Filter by brand
    if params.brand:
        results = [p for p in results if p["brand"].lower() == params.brand.lower()]
    
    # Filter by price range
    if params.min_price is not None:
        results = [p for p in results if p["price"] >= params.min_price]
    
    if params.max_price is not None:
        results = [p for p in results if p["price"] <= params.max_price]
    
    # Filter by color
    if params.color:
        results = [
            p for p in results 
            if any(params.color.lower() in c.lower() for c in p["color"])
        ]
    
    # Filter by availability
    if params.availability is not None:
        results = [p for p in results if p["availability"] == params.availability]
    
    # Filter by minimum rating
    if params.min_rating is not None:
        results = [p for p in results if p["rating"] >= params.min_rating]
    
    return results
    
    
@router.get("/categories", summary="Get available product categories")
async def get_categories():
    """Get all available product categories for filtering"""
    # Record category browsing metrics
    FILTER_USAGE.labels(filter_type="list_categories").inc()
    return {"categories": CATEGORIES}


@router.get("/subcategories", summary="Get available product subcategories")
async def get_subcategories(category: Optional[str] = None):
    """Get all available product subcategories for filtering"""
    # Record subcategory browsing metrics
    FILTER_USAGE.labels(filter_type="list_subcategories").inc()
    if category:
        # Filter subcategories by category
        CATEGORY_VIEWS.labels(category=category).inc()
        filtered = [p["subcategory"] for p in products if p["category"].lower() == category.lower()]
        return {"subcategories": sorted(list(set(filtered)))}
    return {"subcategories": SUBCATEGORIES}


@router.get("/brands", summary="Get available product brands")
async def get_brands():
    """Get all available product brands for filtering"""
    # Record brand browsing metrics
    FILTER_USAGE.labels(filter_type="list_brands").inc()
    return {"brands": BRANDS}


@router.get("/colors", summary="Get available product colors")
async def get_colors():
    """Get all available product colors for filtering"""
    # Record color browsing metrics
    FILTER_USAGE.labels(filter_type="list_colors").inc()
    return {"colors": COLORS}


@router.get("/{product_id}", response_model=Product, summary="Get product details")
async def get_product(product_id: int = Path(..., description="The ID of the product to retrieve")):
    """Get detailed information about a specific product by ID"""
    logger.info(f"🔍 Product details request: id={product_id}")
    
    for product in products:
        if product["id"] == product_id:
            # Record metric for product view
            PRODUCT_VIEWS.labels(
                product_id=str(product_id),
                category=product["category"]
            ).inc()
            return Product(**product)
    
    logger.warning(f"❌ Product not found: id={product_id}")
    raise HTTPException(status_code=404, detail="Product not found")