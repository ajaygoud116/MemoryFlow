import os

if os.path.exists("memoryflow.db"):
    os.remove("memoryflow.db")

from pipeline.memoryflow import run_memoryflow
from benchmarking.benchmark_v2 import retention_score


conversation = [

    "My budget is $2500",

    "I am allergic to shellfish",

    "I prefer luxury hotels",

    "Let's discuss flights",

    "Let's discuss restaurants",

    "Let's discuss weather",

    "Let's discuss attractions",

    "Let's discuss trains",

    "Let's discuss museums",

    "Let's discuss schedules"
]

query = "Recommend a restaurant"

context = run_memoryflow(
    conversation,
    query
)

expected = [

    "2500",

    "shellfish",

    "luxury"
]

score = retention_score(
    expected,
    context
)

print("\nRETENTION TEST")
print("=" * 50)
print(context)
print()
print("Retention Score:", score)