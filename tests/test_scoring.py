# tests/test_scoring.py

from extraction.extractor import extract_memory
from scoring.amis import compute_amis_score

memory = extract_memory(
    "My spending limit is around 2500 dollars"
)

score = compute_amis_score(
    memory,
    "Find me a hotel"
)

print(memory)
print(score)