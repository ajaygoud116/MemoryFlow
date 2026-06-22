from pipeline.memoryflow import (
    run_memoryflow
)

conversation = [

    "Budget is 2500 dollars",

    "Avoid seafood",

    "Need wheelchair accessibility",

    "Traveling with wife",

    "Meeting date is June 20"
]

query = "Recommend restaurant"

context = run_memoryflow(
    conversation,
    query
)

print(context)