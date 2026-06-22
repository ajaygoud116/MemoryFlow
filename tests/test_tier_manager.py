from extraction.extractor import extract_memory

from tiering.tier_manager import (
    assign_tiers
)

texts = [

    "Budget is 2500 dollars",

    "Avoid seafood",

    "Need wheelchair accessibility",

    "Traveling with wife",

    "Meeting date is June 20"
]

memories = []

score = 100

for text in texts:

    memory = extract_memory(text)

    memory.amis_score = score

    memories.append(memory)

    score -= 20

assign_tiers(memories)

for memory in memories:

    print(
        memory.text,
        "->",
        memory.tier
    )