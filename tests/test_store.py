from extraction.extractor import extract_memory

from memory_store.store import MemoryStore


store = MemoryStore()

m1 = extract_memory(
    "Budget is 2500 dollars"
)

store.add_memory(m1)

store.update_frequency(
    m1.memory_id
)

store.update_frequency(
    m1.memory_id
)

print(
    store.get_memories()[0]
)