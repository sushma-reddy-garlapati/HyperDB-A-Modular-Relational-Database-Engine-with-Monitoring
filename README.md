```markdown
HyperDB – A Modular Relational Database Engine with Monitoring
```
HyperDB is a modular, high-performance relational database system built from scratch. It features custom file-based storage, buffer management with LRU eviction, tombstone-based slot reuse, page compaction, and real-time monitoring via Prometheus. Designed for backend engineers and systems enthusiasts, HyperDB emphasizes clarity, observability, and production-grade polish.

![CI](https://github.com/sushma-reddy-garlapati/HyperDB-A-Modular-Relational-Database-Engine-with-Monitoring/actions/workflows/test.yml/badge.svg)
![Coverage](https://img.shields.io/badge/Coverage-89%25-brightgreen)
![License](https://img.shields.io/github/license/sushma-reddy-garlapati/HyperDB-A-Modular-Relational-Database-Engine-with-Monitoring)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Last Commit](https://img.shields.io/github/last-commit/sushma-reddy-garlapati/HyperDB-A-Modular-Relational-Database-Engine-with-Monitoring)


## ❓ Why HyperDB?

HyperDB is built for engineers who want to understand database internals — not just use them. It’s a hands-on, modular system that teaches buffer management, page-level storage, tombstone reuse, and real-time observability. Whether you're prepping for systems interviews or building scalable data platforms, HyperDB gives you the tools and transparency to learn and deploy with confidence.


---

## 🚀 Features

- 🧠 **Buffer Manager** with LRU eviction and page reuse
- 📦 **Page-Level Storage** with tombstone-based slot reuse
- 🔍 **Query Engine** with insert, lookup, and range scan support
- 📊 **Prometheus Monitoring** for page loads and buffer hits
- 🧪 **Benchmark Suite** for insert, lookup, eviction, and reuse
- 📈 **Streamlit Dashboard** for real-time buffer visualization
- 🔁 **Compaction Logic** to reclaim deleted slots
- ⚙️ **CI/CD Integration** with pytest and coverage enforcement
- 🧹 **Modular Design** with clean separation of buffer, storage, and monitoring layers

---

## 🧪 Benchmark Results

| Operation     | Records | Time (sec) | Avg Latency (μs) |
|---------------|---------|------------|------------------|
| Insert        | 1000    | 0.0008     | 0.8              |
| Lookup        | 1000    | 0.0002     | 0.2              |
| Eviction      | 1000    | 0.0021     | —                |
| Slot Reuse    | 1000    | 0.0036     | 3.6              |

> HyperDB handles thousands of operations in milliseconds, validating buffer logic, offset tracking, and tombstone reuse.

---

## 📊 Dashboard Preview

> Coming soon: Streamlit dashboard with buffer state, page compaction, and query latency metrics.

---

## 🛠️ Architecture Overview

```
+------------------+       +------------------+       +------------------+
|   BufferManager  | <---> |     PageManager  | <---> |   FileManager    |
+------------------+       +------------------+       +------------------+
        ↑                          ↑                          ↑
        |                          |                          |
  Prometheus Metrics       Tombstone Reuse           Disk-backed Storage
```

---

## 📦 Installation

```bash
git clone https://github.com/sushma-reddy-garlapati/HyperDB-A-Modular-Relational-Database-Engine-with-Monitoring.git
cd HyperDB
pip install -r requirements.txt
```

---

## 🧪 Run Benchmark

```bash
python benchmark_hyperdb.py
```

---

## 🧪 Run Tests

```bash
pytest --cov=minidb minidb/tests/
```

---

## 🧹 Project Structure

```
HyperDB/
├── minidb/
│   ├── buffer/           # BufferManager, LRU logic
│   ├── storage/          # PageManager, FileManager
│   ├── monitoring/       # Prometheus metrics
│   ├── query_engine.py   # Insert, lookup, range scan
│   └── tests/            # Unit tests for all modules
├── benchmark_hyperdb.py  # Benchmark suite
├── dashboard.py          # Streamlit dashboard
├── requirements.txt
├── README.md
└── .github/workflows/    # CI pipeline
```

---

## 📜 License

This project is licensed under the MIT License.

---

## 👩‍💻 Built By

**Sushma reddy Garlapati**  
