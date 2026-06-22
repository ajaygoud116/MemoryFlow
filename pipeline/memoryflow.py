

from extraction.extractor import (
    extract_memory
)


from memory_store.database import (
    save_memory
)

from utils.embedding_cache import get_embedding
from lifecycle.memory_lifecycle import MemoryLifecycleEngine
from scoring.amis import apply_decay
from scoring.amis import (
    compute_amis_score,
    update_recency_score
)

from scoring.redundancy import (
    compute_redundancy
)


from compression.compressor import (
    compress_memory
)

from retrieval.retriever import (
    retrieve_memories
)

from reconstruction.builder import (
    reconstruct_context
)


def run_memoryflow(conversation,query,store):



    existing_texts = {
        m.text
        for m in store.memories
    }

    for sentence in conversation:
        if sentence in existing_texts:
            continue

        memory = extract_memory(sentence)
        store.add_memory(memory)

    memories = store.get_memories(active_only=False)

    print("TOTAL MEMORIES:",len(store.memories))


    total = len(memories)

    for memory in memories:

        update_recency_score(memory,total)

    for memory in memories:

        compute_amis_score(memory,query)

    for memory in memories:
        apply_decay(memory, len(memories))    


    lifecycle = MemoryLifecycleEngine()

    memories = lifecycle.run(memories)

    for memory in memories:

        compress_memory(memory)
        memory.embedding = (get_embedding(memory))
        save_memory(memory)


    for i in range(len(memories)):

        memories[i].redundancy_score = (

            compute_redundancy(memories[i],memories[:i]))


    store.vector_store.rebuild(store.memories)



    retrieved = retrieve_memories(store,query,top_k=5)
    print("Retrieved:",len(retrieved)) 


    context = reconstruct_context(retrieved)

    return context