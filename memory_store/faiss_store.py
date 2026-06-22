# memory_store\faiss_store.py


# A real FAISS vector store that:

# stores embeddings
# supports similarity search
# maps FAISS IDs to memory IDs

import faiss
import numpy as np

from models.embedding_model import EMBEDDING_MODEL


class FaissMemoryStore:

    def __init__(self):

        self.model = EMBEDDING_MODEL

        sample = self.model.encode("test")

        self.dimension = len(sample)

        self.index = faiss.IndexFlatIP(
            self.dimension
        )

        self.memory_ids = []

    def rebuild(self, memories):

        self.index.reset()
        self.memory_ids = []

        for memory in memories:
            self.add_memory(memory)

    
    def add_memory(
        self,
        memory
    ):
        if memory.memory_id == -1:
            return
        text = memory.compressed_text if memory.compressed_text else memory.text

        if memory.embedding is None:
            embedding = self.model.encode(text)
        else:
            embedding = memory.embedding.cpu().numpy() if hasattr(memory.embedding, 'cpu') else memory.embedding

        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        embedding = np.array([embedding], dtype="float32")
        self.index.add(embedding)
        self.memory_ids.append(memory.memory_id)        

    def get_memory_id(self, index_id):
        if index_id < 0 or index_id >= len(self.memory_ids):
            return None
        return self.memory_ids[index_id]
    
    
    def search(
        self,
        query,
        k=5
    ):

        if len(
            self.memory_ids
        ) == 0:

            return []

        query_embedding = (
            self.model.encode(query)
        )

        norm = np.linalg.norm(query_embedding)
        if norm > 0:
            query_embedding = query_embedding / norm

        query_embedding = np.array(
            [query_embedding],
            dtype="float32"
        )

        cos_similarities, indices = self.index.search(query_embedding, k)

        results = []

        for idx, similarity in zip(
            indices[0],
            cos_similarities[0]
        ):

            if idx == -1:
                continue

            memory_id = self.get_memory_id(idx)
            if memory_id is None:
                continue

            results.append(
                (memory_id, float(similarity))
            )

        return results
    
