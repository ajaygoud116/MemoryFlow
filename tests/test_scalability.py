import os

if os.path.exists("memoryflow.db"):
    os.remove("memoryflow.db")



import time

from extraction.extractor import (
    extract_memory
)

from memory_store.store import (
    MemoryStore
)


sizes = [

    100,

    500,

    1000,

    2000
]


print("\nSCALABILITY TEST")
print("=" * 50)

for size in sizes:

    store = MemoryStore()

    start = time.time()

    for i in range(size):

        memory = extract_memory(
            f"Memory {i}"
        )

        store.add_memory(
            memory
        )

    elapsed = (
        time.time() - start
    )

    print(

        f"{size} memories "

        f"-> {elapsed:.2f}s"

    )