
```markdown
# HyperDB – A Modular Relational Database Engine with Monitoring
```
![CI](https://github.com/sushma-reddy-garlapati/HyperDB-A-Modular-Relational-Database-Engine-with-Monitoring/actions/workflows/test.yml/badge.svg)
![Coverage](https://img.shields.io/badge/Coverage-89%25-brightgreen)
![License](https://img.shields.io/github/license/sushma-reddy-garlapati/HyperDB-A-Modular-Relational-Database-Engine-with-Monitoring)
![Python](https://img.shields.io/badge/Python-3.12-blue)

HyperDB is a custom-built, modular relational database engine designed to demonstrate core backend engineering principles with a focus on buffer management, storage, and observability. It features a page-based storage system with an LRU buffer manager, precise offset tracking, and real-time metrics collection using Prometheus.

The project includes a comprehensive benchmark suite validating insertions, lookups, evictions, and buffer management performance, alongside a Streamlit dashboard for interactive visualization of buffer state and query latency. A robust CI/CD pipeline with GitHub Actions ensures code quality through automated testing and coverage reporting.

---

## 🚀 Features

- 🧠 LRU-based buffer eviction with page pinning logic
- 📦 Page-level storage with offset tracking and slot management
- 📊 Prometheus metrics for buffer hits, page loads, and query latency
- 📈 Streamlit dashboard for real-time buffer visualization
- 🧪 Benchmark suite for insert, lookup, and eviction performance
- ✅ CI/CD pipeline with automated testing and coverage enforcement

---

## 🧪 Benchmark Results

| Operation     | Records | Time (sec) | Avg Latency (μs) |
|---------------|---------|------------|------------------|
| Insert        | 1000    | 0.0008     | 0.8              |
| Lookup        | 1000    | 0.0002     | 0.2              |
| Eviction      | 1000    | 0.0021     | —                |

> HyperDB executes thousands of operations in milliseconds, validating buffer logic and offset reuse.

---

## 📊 Dashboard Preview

> Coming soon: Streamlit dashboard with buffer state, query latency, and page-level metrics.

---

## 🛠️ Architecture Overview

```
+------------------+       +------------------+       +------------------+
|   BufferManager  | <---> |     PageManager  | <---> |   FileManager    |
+------------------+       +------------------+       +------------------+
        ↑                          ↑                          ↑
        |                          |                          |
  Prometheus Metrics       Offset Tracking           Disk-backed Storage
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

## 📁 Project Structure

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

## 🛠️ Skills & Tools Used

| Category         | Tools & Technologies                                      |
|------------------|-----------------------------------------------------------|
| **Languages**    | Python                                                    |
| **Testing**      | `pytest`, `pytest-cov`                                    |
| **Monitoring**   | `prometheus_client`, Prometheus                          |
| **Dashboarding** | `streamlit`                                               |
| **DevOps**       | GitHub Actions, cron jobs, CI/CD setup                    |
| **Design**       | Modular architecture, clean UI, recruiter-facing README   |
| **Debugging**    | Root cause analysis, edge case simulation, test coverage  |
| **Documentation**| Architecture diagrams, benchmark tables, feature breakdown|

---

## 📜 License

This project is licensed under the MIT License.

## 👩‍💻 Built By

**Sushma reddy Garlapati**  
