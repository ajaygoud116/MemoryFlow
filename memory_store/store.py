

from time import time
from typing import List

from core import memory
from core.memory import Memory
from utils.embedding_cache import get_embedding
from conflict.conflict_manager import ConflictManager

from memory_store.faiss_store import FaissMemoryStore

from memory_store.database import (
    init_db,
    save_memory,
    load_all_memories
)


class MemoryStore:

    def __init__(self):

        init_db()

        self.memories: List[Memory] = load_all_memories()

        self.counter = max([m.memory_id for m in self.memories],default=-1) + 1

        self.conflict_manager = ConflictManager()

        self.vector_store = FaissMemoryStore()

        for memory in self.memories:
            if memory.embedding is None:
                memory.embedding = get_embedding(memory)
            self.vector_store.add_memory(memory)

    def add_memory(self, memory):

        memory.created_at = time()

        memory.memory_id = self.counter

        print(
            "CREATED MEMORY ID:",
            memory.memory_id,
            memory.text
        )

        memory.created_position = len(self.memories)

        self.counter += 1


        # create embedding
        if memory.embedding is None:

            memory.embedding = self.vector_store.model.encode(
                memory.text
            )


        # conflict resolution
        self.update_existing_memory(memory)


        self.memories.append(memory)


        # ADD TO FAISS HERE
        self.vector_store.add_memory(memory)


        # persist
        save_memory(memory)
        
    def update_existing_memory(self, new_memory):

        for existing in self.memories:

            if not existing.active:
                continue
            

            conflict, report = (self.conflict_manager.detect_conflict(new_memory,existing))
            
            if report is not None:

                self.conflict_manager.resolve_conflict(new_memory,existing,report)

                save_memory(existing)



    def get_memories(self, active_only=True):

        if not active_only:
            return self.memories

        return [
            m for m in self.memories if m.active
        ]

    def get_memory_by_id(self, memory_id):

        for memory in self.memories:

            if memory.memory_id == memory_id:
                return memory

        return None

    def update_frequency(self, memory_id):

        memory = self.get_memory_by_id(memory_id)

        if memory is None:
            return

        memory.retrieval_count += 1

        memory.frequency_score = min(
            memory.retrieval_count * 10,
            100
        )

        save_memory(memory)