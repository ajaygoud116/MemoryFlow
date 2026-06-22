# scoring\redundancy.py


from sentence_transformers import util

from utils.embedding_cache import (
    get_embedding
)

def compute_redundancy(
    memory,
    existing_memories
):

    if len(existing_memories) == 0:

        return 0

    memory_emb = get_embedding(memory)

    max_similarity = 0

    for existing in existing_memories:

        emb = get_embedding(existing)
        
        similarity = util.cos_sim(memory_emb,emb).item()

        max_similarity = max(max_similarity,similarity)

    return max_similarity * 100