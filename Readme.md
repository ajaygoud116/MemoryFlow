# MemoryFlow

## Importance-Aware Hierarchical Memory Orchestration for Long-Horizon AI Agents

MemoryFlow is a memory orchestration framework designed to address one of the fundamental limitations of modern AI agents: the inability to efficiently manage long-term conversational context.

As conversations grow, traditional retrieval systems accumulate large amounts of historical information. This increases token costs, introduces retrieval noise, and often causes critical user constraints to become buried beneath low-value conversational data.

MemoryFlow introduces an importance-aware memory layer that continuously evaluates, prioritizes, compresses, retrieves, and evolves memories based on their utility to future reasoning tasks.

Rather than treating all memories equally, the system attempts to answer a simple question:

> Which memories are worth keeping, which should be compressed, and which can safely fade over time?

---

# Problem Statement

Most memory systems for LLM-powered agents rely on one of three approaches:

## Full Conversation Storage

Every interaction is retained and supplied during retrieval.

### Problems

- Context window growth
- Increased token consumption
- Higher inference latency
- Retrieval interference

---

## Summarization-Based Memory

Historical conversations are periodically summarized.

### Problems

- Loss of critical details
- Information drift
- Poor handling of user preferences and constraints

---

## Pure Vector Retrieval

Memories are retrieved solely through semantic similarity.

### Problems

- No memory prioritization
- No lifecycle management
- No conflict resolution
- No compression awareness

---

MemoryFlow was designed to explore whether memory itself could become an actively managed resource rather than a passive storage layer.

---

# Core Architectural Decisions

## 1. Adaptive Memory Importance Scoring (AMIS)

### Decision

Every memory receives an Adaptive Memory Importance Score (AMIS).

### Reasoning

Not all memories contribute equally to future reasoning.

Example:

```text
I am allergic to shellfish
```

is significantly more important than:

```text
Check weather
```

Traditional retrieval systems often treat both as equally retrievable semantic chunks.

MemoryFlow attempts to quantify memory value and use it to guide retention and retrieval decisions.

### Trade-off

The current scoring system relies on manually tuned weights and thresholds.

While effective for the prototype, future versions should learn these values automatically from retrieval performance and user feedback.

---

## 2. Hierarchical Memory Management

### Decision

Memories are organized into four semantic tiers.

| Tier | Purpose | Action |
|--------|----------|---------|
| Tier 1 | Critical Constraints | Preserve |
| Tier 2 | Preferences | Structured Storage |
| Tier 3 | Facts | Summarize |
| Tier 4 | Disposable Context | Compress |

### Reasoning

A user's allergy should not be treated the same way as a temporary search request.

The tiering system allows MemoryFlow to allocate storage and compression effort according to memory value.

### Trade-off

Current tier boundaries are manually tuned and may not generalize across domains.

---

## 3. Controlled Use of LLMs

### Decision

LLMs are used only for:

- Structured memory extraction
- Memory summarization

### Reasoning

During development, a conscious effort was made to avoid relying on LLMs for every memory management decision.

Critical operations such as:

- AMIS scoring
- Tier assignment
- Conflict resolution
- Retrieval ranking
- Lifecycle transitions

remain deterministic.

### Trade-off

Deterministic systems are easier to debug and evaluate, but may sacrifice some adaptability.

---

## 4. Semantic Conflict Resolution

### Decision

MemoryFlow actively detects contradictory user states.

### Example

Old Memory:

```text
I prefer budget hotels
```

Updated Memory:

```text
I prefer luxury hotels
```

### Reasoning

Without conflict resolution, both memories remain active and pollute future retrieval results.

MemoryFlow compares:

- Topic similarity
- Value similarity
- Context similarity
- Polarity

to determine whether a memory should be merged, replaced, or ignored.

### Trade-off

Conflict detection currently relies on heuristic matching and remains an active area for future improvement.

---

## 5. Lifecycle-Aware Memory

### Decision

Memories evolve over time.

Supported lifecycle operations include:

- Promotion
- Demotion
- Consolidation
- Forgetting
- Archival

### Reasoning

Human memory is dynamic.

An AI memory system should also be capable of adapting to changing relevance.

### Trade-off

Lifecycle policies remain manually engineered in the current prototype.

---

## 6. Retrieval Re-Ranking

### Decision

Retrieval combines semantic similarity and memory importance.

### Formula

```text
Final Score =
0.70 × Semantic Similarity
+
0.30 × AMIS
```

### Reasoning

Pure semantic retrieval often surfaces memories that are similar but not necessarily important.

The additional importance signal helps prioritize memories that are likely to matter more during reasoning.

### Trade-off

Weighting parameters remain heuristic and require larger-scale evaluation.

---

# System Architecture

```text
User Conversation
        ↓
Memory Extraction
        ↓
Conflict Resolution
        ↓
AMIS Scoring
        ↓
Tier Assignment
        ↓
Compression + Lifecycle
        ↓
SQLite + FAISS Storage
        ↓
Retrieval & Re-ranking
        ↓
Context Reconstruction
        ↓
AI Agent
```

---

# Technical Stack

### Language

- Python

### NLP

- spaCy

### LLM Layer

- Ollama
- Llama 3

### Embeddings

- all-MiniLM-L6-v2

### Vector Retrieval

- FAISS

### Storage

- SQLite

### Dashboard

- Streamlit

---

# Evaluation

## Compression Benchmark

| Metric | Result |
|----------|----------|
| Baseline Tokens | 24 |
| MemoryFlow Tokens | 15 |
| Token Reduction | 37.5% |

## Retrieval Evaluation

| Metric | Score |
|---------|--------|
| Recall@5 | 1.0 |
| Precision@5 | 1.0 |
| MRR | 1.0 |
| NDCG@5 | 1.0 |

---

# Engineering Challenges

A significant portion of development effort was spent on experimentation, debugging, and iterative refinement.

Key challenges included:

- Circular import failures during FAISS integration
- Memory identifier mismatches between vector and storage layers
- Duplicate memory ingestion
- Retrieval ranking instability
- Compression regressions
- Persistence recovery issues

Resolving these issues significantly improved the robustness of the final system.

---

# Future Directions

The current implementation demonstrates the viability of importance-aware memory orchestration but remains a prototype.

Planned improvements include:

- Adaptive AMIS learning
- Dynamic tier assignment
- Long-horizon evaluation (50–100+ turn conversations)
- Retrieval-aware compression
- Episodic memory formation
- Temporal memory graphs
- Multi-agent memory sharing

---

# Repository Structure

```text
memoryflow/

├── extraction/
├── scoring/
├── compression/
├── conflict/
├── lifecycle/
├── retrieval/
├── reconstruction/
├── memory_store/
├── benchmarking/
├── dashboard/
├── tests/
└── pipeline/
```

---


MemoryFlow Research Prototype
