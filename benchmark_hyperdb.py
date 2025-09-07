from time import perf_counter as timer
import random
from prometheus_client import REGISTRY
from minidb.buffer.buffer_manager import BufferManager

def get_metric(name):
    for metric in REGISTRY.collect():
        if metric.name == name:
            for sample in metric.samples:
                return sample.value
    return None

def print_metrics(label=""):
    hits = get_metric("buffer_hits_total") or 0
    misses = get_metric("buffer_misses_total") or 0
    total = hits + misses
    print(f"{label}Buffer Hits: {hits}")
    print(f"{label}Buffer Misses: {misses}")
    if total > 0:
        print(f"{label}Hit Ratio: {hits / total:.2%}")
    else:
        print(f"{label}Hit Ratio: N/A (no page accesses)")


def benchmark_insert(n=1000):
    bm = BufferManager(capacity=10)
    start = timer()
    for i in range(n):
        bm.insert_record(f"user_{i}", f"email_{i}@example.com")
    end = timer()
    print(f"[Insert] {n} records in {end - start:.4f} sec")
    print(f"         Avg latency: {(end - start)/n:.6f} sec/record")
    print_metrics("         ")

def benchmark_lookup(n=1000):
    bm = BufferManager(capacity=10)
    for i in range(n):
        bm.insert_record(f"user_{i}", f"email_{i}@example.com")

    start = timer()
    for i in range(n):
        bm.get_record(f"user_{i}")
    end = timer()
    print(f"[Lookup] {n} records in {end - start:.4f} sec")
    print(f"         Avg latency: {(end - start)/n:.6f} sec/record")
    print_metrics("         ")

def benchmark_eviction(n=1000, capacity=5):
    bm = BufferManager(capacity=capacity)
    start = timer()
    for i in range(n):
        bm.insert_record(f"user_{i}", f"email_{i}@example.com")
    end = timer()
    print(f"[Eviction] {n} inserts with buffer capacity {capacity}")
    print(f"           Time taken: {end - start:.4f} sec")
    print_metrics("           ")

def benchmark_slot_reuse(n=1000):
    bm = BufferManager()
    for i in range(n):
        bm.insert_record(f"user_{i}", f"email_{i}@example.com")
        bm.delete_record(f"user_{i}")

    start = timer()
    for i in range(n):
        bm.insert_record(f"user_reuse_{i}", f"email_reuse_{i}@example.com")
    end = timer()
    print(f"[Slot Reuse] {n} inserts into deleted slots")
    print(f"             Time taken: {end - start:.4f} sec")
    print(f"             Avg latency: {(end - start)/n:.6f} sec/record")
    print_metrics("             ")

def benchmark_random_lookup(n=1000, insert_total=10000):
    bm = BufferManager(capacity=10)
    for i in range(insert_total):
        bm.insert_record(f"user_{i}", f"email_{i}@example.com")

    keys = [f"user_{random.randint(0, insert_total - 1)}" for _ in range(n)]
    start = timer()
    found = 0
    for key in keys:
        if bm.get_record(key):
            found += 1
    end = timer()
    print(f"[Random Lookup] {n} lookups from {insert_total} records")
    print(f"                Found: {found}")
    print(f"                Time taken: {end - start:.4f} sec")
    print(f"                Avg latency: {(end - start)/n:.6f} sec/record")
    print_metrics("                ")

if __name__ == "__main__":
    print("=== HyperDB Benchmark Suite ===")
    benchmark_insert()
    benchmark_lookup()
    benchmark_eviction()
    benchmark_slot_reuse()
    benchmark_random_lookup()
# from time import perf_counter as timer
# from minidb.buffer.buffer_manager import BufferManager
# from prometheus_client import REGISTRY

# def get_metric(name):
#     for metric in REGISTRY.collect():
#         if metric.name == name:
#             for sample in metric.samples:
#                 return sample.value
#     return None


# def benchmark_insert(n=1000):
#     bm = BufferManager(capacity=10)
#     start = timer()
#     for i in range(n):
#         bm.insert_record(f"user_{i}", f"email_{i}@example.com")
#     end = timer()
#     print(f"[Insert] {n} records in {end - start:.4f} sec")
#     print(f"         Avg latency: {(end - start)/n:.6f} sec/record")

# def benchmark_lookup(n=1000):
#     bm = BufferManager(capacity=10)
#     for i in range(n):
#         bm.insert_record(f"user_{i}", f"email_{i}@example.com")

#     start = timer()
#     for i in range(n):
#         bm.get_record(f"user_{i}")
#     end = timer()
#     print(f"[Lookup] {n} records in {end - start:.4f} sec")
#     print(f"         Avg latency: {(end - start)/n:.6f} sec/record")

# def benchmark_eviction(n=1000, capacity=5):
#     bm = BufferManager(capacity=capacity)
#     start = timer()
#     for i in range(n):
#         bm.insert_record(f"user_{i}", f"email_{i}@example.com")
#     end = timer()
#     print(f"[Eviction] {n} inserts with buffer capacity {capacity}")
#     print(f"           Time taken: {end - start:.4f} sec")

# def benchmark_slot_reuse(n=1000):
#     bm = BufferManager()
#     for i in range(n):
#         bm.insert_record(f"user_{i}", f"email_{i}@example.com")
#         bm.delete_record(f"user_{i}")

#     start = timer()
#     for i in range(n):
#         bm.insert_record(f"user_reuse_{i}", f"email_reuse_{i}@example.com")
#     end = timer()
#     print(f"[Slot Reuse] {n} inserts into deleted slots")
#     print(f"             Time taken: {end - start:.4f} sec")
#     print(f"             Avg latency: {(end - start)/n:.6f} sec/record")

# if __name__ == "__main__":
#     print("=== HyperDB Benchmark Suite ===")
#     benchmark_insert()
#     benchmark_lookup()
#     benchmark_eviction()
#     benchmark_slot_reuse()
