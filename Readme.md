# MemoryFlow

## Importance-Aware Hierarchical Memory Orchestration for Long-Horizon AI Agents

MemoryFlow is a memory orchestration framework that enables AI agents to efficiently manage long-term conversational context through importance-aware memory scoring, hierarchical storage, adaptive compression, semantic conflict resolution, and lifecycle-aware retrieval.

Unlike traditional memory systems that rely solely on vector retrieval or context truncation, MemoryFlow continuously evaluates the utility of each memory and dynamically determines whether it should be retained, compressed, archived, or discarded.

---

## Problem

As AI agents operate over longer conversations, context windows become saturated with redundant or low-value information.

This leads to:

- Increased token costs
- Higher inference latency
- Retrieval noise
- Loss of critical user constraints
- Long-horizon reasoning degradation

Traditional approaches such as context truncation and naive summarization often remove information that remains important for future reasoning.

---

## Solution

MemoryFlow introduces a unified memory layer consisting of:

### Adaptive Memory Importance Scoring (AMIS)

Scores each memory using:

- Importance
- Relevance
- Recency
- Retrieval Frequency
- Retrieval Success
- Redundancy
- Conflict Risk

### Hierarchical Memory Management

| Tier | Description | Action |
|--------|------------|---------|
| Tier 1 | Critical Constraints | Preserve |
| Tier 2 | Preferences | Structured Storage |
| Tier 3 | Facts | Summarize |
| Tier 4 | Disposable Context | Compress |

### Semantic Conflict Resolution

Detects state changes and archives outdated memories to prevent agent inconsistency.

### Lifecycle Management

Supports:

- Forgetting
- Consolidation
- Promotion
- Demotion
- Archival

---

## Architecture

User Conversation
→ Memory Extraction
→ Conflict Resolution
→ AMIS Scoring
→ Tier Assignment
→ Compression & Lifecycle Management
→ FAISS + SQLite Memory Store
→ Retrieval & Re-ranking
→ Context Reconstruction
→ AI Agent

---

## Technology Stack

- Python
- spaCy
- Ollama (Llama 3)
- all-MiniLM-L6-v2
- FAISS
- SQLite
- Streamlit

---

## Evaluation

### Compression Benchmark

| Metric | Result |
|----------|----------|
| Baseline Tokens | 24 |
| MemoryFlow Tokens | 15 |
| Token Reduction | 37.5% |

### Retrieval Evaluation

| Metric | Score |
|---------|--------|
| Recall@5 | 1.0 |
| Precision@5 | 1.0 |
| MRR | 1.0 |
| NDCG@5 | 1.0 |

---

## Applications

- Customer Support Agents
- Healthcare Assistants
- Travel Planning Systems
- Enterprise Knowledge Agents
- Autonomous Research Agents

---

**Author:** Ajay Goud Kamugaru  
**Project:** Bharat Academix CodeQuest 2026  