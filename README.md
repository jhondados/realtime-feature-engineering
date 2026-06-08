# ⚡ Real-Time Feature Engineering Platform

[![Latency](https://img.shields.io/badge/Feature%20Serving-< 2ms%20P99-green)](.) [![Features](https://img.shields.io/badge/Features%20Registered-8%2C400-blue)](.) [![Events](https://img.shields.io/badge/Events%2Fsec-1.2M-orange)](.)

> **Sub-millisecond feature serving** at 1.2M events/sec. Point-in-time correct feature joins for training, streaming computation with Flink and shared feature registry used by 40+ models.

## 🏗️ Platform Architecture
```
Events (Kafka) → Flink Streaming → Feature Computation
                                → Redis (online store, < 2ms)
                                → BigQuery (offline store)
Feature Registry → Definition, owner, lineage, quality metrics
Model Training   → Point-in-time correct join from offline store
Model Serving    → Batch fetch from Redis (< 2ms per request)
```

## 📊 Metrics
- **8,400 registered features** across 40+ models
- **< 2ms P99** online feature serving (Redis)
- **1.2M events/sec** streaming throughput
- **Zero training/serving skew** (same computation, different stores)
