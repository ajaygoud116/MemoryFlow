from pipeline.memoryflow import (
    run_memoryflow
)


conversation = []

conversation.append(
    "Hi"
)

conversation.append(
    "I am allergic to shellfish"
)

for i in range(3, 80):

    conversation.append(

        f"Random discussion turn {i}"

    )

conversation.append(
    "My budget is $2500"
)

conversation.append(
    "I want to travel to Bali"
)

for i in range(82, 99):

    conversation.append(

        f"Another discussion turn {i}"

    )

conversation.append(
    "I changed my mind. I want to travel to Switzerland"
)

query = (
    "Recommend a restaurant for my trip"
)

context = run_memoryflow(

    conversation,

    query

)

print(
    "\n=== MEMORY CONTEXT ===\n"
)

print(
    context
)