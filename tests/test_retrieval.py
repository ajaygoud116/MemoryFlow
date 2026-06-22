# Critical Constraints

# shellfish allergy

# budget 2500

# Switzerland

import os

if os.path.exists("memoryflow.db"):
    os.remove("memoryflow.db")

from pipeline.memoryflow import run_memoryflow


conversation = [

    "My budget is $2500",

    "I am allergic to shellfish",

    "I prefer luxury hotels",

    "Destination is Switzerland",

    "Search flights",

    "Search trains",

    "Search restaurants"
]


query = (
    "Recommend dinner options"
)

context = run_memoryflow(
    conversation,
    query
)

print("\nRETRIEVAL TEST")
print("=" * 50)

print(context)

print("\nExpected:")

print(
    "- shellfish allergy"
)

print(
    "- budget"
)

print(
    "- Switzerland"
)