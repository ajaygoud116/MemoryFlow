from extraction.extractor import extract_memory

from memory_store.store import MemoryStore

from scoring.amis import (
    update_recency_score
)


store = MemoryStore()

sentences = [

    "Budget is 2500 dollars",

    "I prefer luxury hotels",

    "Meeting date is June 20",

    "Book flight tomorrow"

]

for sentence in sentences:

    memory = extract_memory(
        sentence
    )

    store.add_memory(
        memory
    )

total = len(
    store.get_memories()
)

for memory in store.get_memories():

    update_recency_score(
        memory,
        total
    )

    print(
        memory.text,
        "->",
        round(
            memory.recency_score,
            2
        )
    )