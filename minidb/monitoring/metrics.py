from prometheus_client import Counter, Histogram, CollectorRegistry

# Create a singleton registry
registry = CollectorRegistry()

# Define metrics inside this registry
api_requests_total = Counter(
    "api_requests_total", "Total number of API requests", registry=registry
)

buffer_evictions_total = Counter(
    "buffer_evictions_total", "Total buffer evictions", registry=registry
)

page_load_time = Histogram(
    "page_load_time_seconds", "Time taken to load a page from disk", registry=registry
)
