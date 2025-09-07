from time import perf_counter as timer
from minidb.buffer.buffer_manager import BufferManager

def benchmark_insert(n=1000):
    bm = BufferManager(capacity=10)
    start = timer()
    for i in range(n):
        bm.insert_record(f"user_{i}", f"email_{i}@example.com")
    end = timer()
    print(f"[Insert] {n} records in {end - start:.4f} sec")
    print(f"         Avg latency: {(end - start)/n:.6f} sec/record")

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

def benchmark_eviction(n=1000, capacity=5):
    bm = BufferManager(capacity=capacity)
    start = timer()
    for i in range(n):
        bm.insert_record(f"user_{i}", f"email_{i}@example.com")
    end = timer()
    print(f"[Eviction] {n} inserts with buffer capacity {capacity}")
    print(f"           Time taken: {end - start:.4f} sec")

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

if __name__ == "__main__":
    print("=== HyperDB Benchmark Suite ===")
    benchmark_insert()
    benchmark_lookup()
    benchmark_eviction()
    benchmark_slot_reuse()
