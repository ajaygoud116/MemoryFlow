# retrieval/retriever.py
import numpy as np
from memory_store.database import save_memory


def retrieve_memories(
    store, 
    query: str, 
    top_k: int = 5, 
    candidate_pool_factor: int = 5,
    similarity_threshold: float = 0.23,  
    semantic_weight: float = 0.70        
):
    """
    Retrieves and re-ranks active agent memories using calibrated semantic profiles.
    
    Parameters:
        store: Unified memory store orchestrator instance.
        query (str): Active incoming user lookup string.
        top_k (int): Total context elements returned to the model framework.
        candidate_pool_factor (int): Primary search scaling multiplier.
        similarity_threshold (float): Rejection floor boundary for pure semantic relevance [0.0 - 1.0].
        semantic_weight (float): Re-ranking balance factor. AMIS weight becomes (1.0 - semantic_weight).
    """
    # Fetch all currently active memory nodes
    active_pool = store.get_memories(active_only=True)
    pool_size = len(active_pool)
    
    if pool_size == 0:
        return []
        

    base_fetch = top_k * candidate_pool_factor
    adaptive_floor = int(np.sqrt(pool_size))
    fetch_k = min(max(base_fetch, adaptive_floor), pool_size)
    
    # Execute vector store Inner Product (Cosine) search
    search_results = store.vector_store.search(query, k=fetch_k)
    
    scored = []
    for memory_id, similarity in search_results:
        
        memory = store.get_memory_by_id(memory_id)
        print(f"MEMORY={memory.text} "f"SIM={similarity:.4f}")
        if memory is None or not memory.active:
            continue
            
        # This explicitly stops low-relevance items from cheating retrieval via high AMIS scores.
        if similarity < similarity_threshold:
            continue
            
        # Prevents negative noise skew and aligns with calibrated AMIS metrics
        normalized_similarity = max(0.0, similarity)
        similarity_score = normalized_similarity * 100.0
        
    
        amis_weight = 1.0 - semantic_weight
        retrieval_score = (semantic_weight * similarity_score) + (amis_weight * memory.amis_score)
        
        scored.append((memory, retrieval_score))
        
    # Sort and return clean top-k matches
    scored.sort(key=lambda x: x[1], reverse=True)
    retrieved = scored[:top_k]
    
    # Update active telemetry tracking counters
    for memory, _ in retrieved:
        store.update_frequency(memory.memory_id)
        
        memory.retrieval_success_rate = min(
            memory.retrieval_success_rate + 5,
            100
        )
        save_memory(memory)
    return retrieved