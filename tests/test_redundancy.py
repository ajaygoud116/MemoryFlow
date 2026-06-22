from extraction.extractor import extract_memory

from scoring.redundancy import (
    compute_redundancy
)

m1 = extract_memory(
    "Budget is 2500 dollars"
)

m2 = extract_memory(
    "My spending limit is 2500 dollars"
)

score = compute_redundancy(
    m2,
    [m1]
)

print(score)