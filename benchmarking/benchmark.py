

from collections import Counter

import tiktoken

from sentence_transformers import util

from benchmarking.baseline import BaselineAgent

from models.embedding_model import EMBEDDING_MODEL

from retrieval.retriever import retrieve_memories
from benchmarking.retrieval_metrics import (
    compute_recall_at_k,
    compute_precision_at_k,
    compute_mrr,
    compute_ndcg_at_k
)


ENCODER = tiktoken.get_encoding(
    "cl100k_base"
)

model = EMBEDDING_MODEL



def count_tokens(text: str):

    if not text:
        return 0

    return len(ENCODER.encode(text))




def build_memoryflow_context(store,query, top_k=5):

    retrieved = retrieve_memories(
        store,
        query,
        top_k=top_k
    )


    lines = []

    for memory, _ in retrieved:
        print("MEMFLOW TOKENS:",count_tokens(memory.compressed_text))
        text = (
            memory.compressed_text
            if memory.compressed_text
            else memory.text
        )

        lines.append(text)

    return "\n".join(lines)



def calculate_metrics(store):

    memories = store.get_memories(active_only=False)

    active_memories = [m for m in memories if m.active]

    archived_memories = [m for m in memories if not m.active]

    original_tokens = 0
    compressed_tokens = 0

    for memory in memories:

        original_tokens += count_tokens(
            memory.text
        )

        compressed_tokens += count_tokens(
            (
                memory.compressed_text
                if memory.compressed_text
                else memory.text
            )
        )

    compression_ratio = 0

    if original_tokens > 0:

        compression_ratio = (1-(compressed_tokens/original_tokens)) * 100

    tier_counts = Counter(
        memory.tier
        for memory in memories
    )

    return {

        "total_memories":
            len(memories),

        "active_memories":
            len(active_memories),

        "archived_memories":
            len(archived_memories),

        "original_tokens":
            original_tokens,

        "compressed_tokens":
            compressed_tokens,

        "compression_ratio":
            round(compression_ratio,2),

        "tier_distribution":
            dict(tier_counts)

    }




def compare_systems(
    conversation,
    store,
    query=None, top_k=5
):

    baseline = BaselineAgent()



    baseline_context = baseline.build_context(conversation,query, top_k=top_k)

    baseline_tokens = count_tokens(baseline_context)


    memoryflow_context = build_memoryflow_context(store,query, top_k=top_k)

    memoryflow_tokens = count_tokens(memoryflow_context)


    reduction = 0

    if baseline_tokens > 0:

        reduction = (1-(memoryflow_tokens/baseline_tokens)) * 100

    return {

        "baseline_tokens":
            baseline_tokens,

        "memoryflow_tokens":
            memoryflow_tokens,

        "token_reduction_percent":
            round(reduction,2),

        "baseline_context_sample":
            baseline_context[:300],

        "memoryflow_context_sample":
            memoryflow_context[:300]

    }




def retention_score(
    expected_items,
    retrieved_context,
    threshold=0.70
):

    if len(expected_items) == 0:
        return 0

    context_embedding = model.encode(
        retrieved_context,
        convert_to_tensor=True
    )

    found = 0

    for item in expected_items:

        item_embedding = model.encode(
            item,
            convert_to_tensor=True
        )

        similarity = util.cos_sim(
            item_embedding,
            context_embedding
        ).item()

        if similarity >= threshold:
            found += 1

    return round((found/len(expected_items)) * 100,2)