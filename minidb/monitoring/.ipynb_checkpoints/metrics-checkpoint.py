from prometheus_client import Counter, Histogram

if "metrics_registered" not in globals():
    api_requests_total = Counter("api_requests_total", "Total number of API requests")
    buffer_evictions_total = Counter("buffer_evictions_total", "Total buffer evictions")
    page_load_time = Histogram("page_load_time_seconds", "Time taken to load a page from disk")
    metrics_registered = True
