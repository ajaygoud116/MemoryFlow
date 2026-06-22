# compression/compressor.py

import tiktoken

ENCODER = tiktoken.get_encoding(
    "cl100k_base"
)

def count_tokens(text):

    if not text:
        return 0

    return len(
        ENCODER.encode(text)
    )


import ollama

def llm_summarize(text):

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role":"user",
                "content":
                f"Compress in <10 words:\n{text}"
            }
        ]
    )

    return response["message"]["content"].strip()

def compute_compression_strength(memory):

    retrieval_success = getattr(memory,"retrieval_success_rate",0)

    frequency = getattr(memory,"frequency_score",0)

    amis = getattr(memory,"amis_score",0)

    score = (
        0.50 * (100 - amis)
        +
        0.30 * (100 - retrieval_success)
        +
        0.20 * (100 - frequency)
    )

    # Constraints should resist compression

    if memory.memory_type == "constraint":
        score -= 40

    return max(0,min(score, 100))


def build_structured_memory(memory):

    if memory.topic and memory.value:
        return memory.value

    if memory.topic:
        return memory.topic

    if memory.value:
        return str(memory.value)

    if memory.memory_type == "constraint":
        return f"!{memory.value}"

    if memory.memory_type == "preference":
        return f"P:{memory.value}"

    if memory.memory_type == "fact":
        return f"F:{memory.value}"

    return ""


def build_capsule(memory):

    if memory.topic and memory.value:
        return memory.value
    
    if memory.topic:
        return memory.topic

    if memory.value:
        return str(memory.value)


    return memory.text


def compress_memory(memory):

    strength = compute_compression_strength(memory)

    memory.metadata["compression_strength"] = round(strength,2)


    if strength < 25:
        memory.compressed_text = (memory.text)


    elif strength < 50:

        structured = (
            build_structured_memory(
                memory
            )
        )

        if structured:
            memory.compressed_text = (structured)

        else:
            memory.compressed_text = (memory.text)


    elif strength < 75:
        summary = llm_summarize(memory.text)

        if (summary and len(summary) < len(memory.text)):
            memory.compressed_text = (summary)

        else:
            memory.compressed_text = (build_structured_memory(memory) or memory.text)

    else:
        capsule = build_capsule(memory)

        if capsule:
            memory.compressed_text = (capsule)

        else:
            memory.compressed_text = (memory.text)


    original_tokens = count_tokens(memory.text)

    compressed_tokens = count_tokens(memory.compressed_text)


    if original_tokens == 0:

        memory.compression_cost = 100

    else:

        memory.compression_cost = round((compressed_tokens/original_tokens) * 100,2)

    return memory