import time

from benchmarking.baseline import BaselineAgent

from benchmarking.benchmark_v2 import (
    build_memoryflow_context
)

from memory_store.store import MemoryStore

from extraction.extractor import extract_memory


conversation = [

    f"Memory {i}"

    for i in range(1000)
]


baseline = BaselineAgent()

start = time.time()

baseline_context = (
    baseline.build_context(
        conversation
    )
)

baseline_time = (
    time.time() - start
)


store = MemoryStore()

for text in conversation:

    store.add_memory(
        extract_memory(text)
    )

start = time.time()

memoryflow_context = (
    build_memoryflow_context(
        store
    )
)

memoryflow_time = (
    time.time() - start
)

print("\nLATENCY TEST")
print("=" * 50)

print(
    "Baseline:",
    baseline_time
)

print(
    "MemoryFlow:",
    memoryflow_time
)