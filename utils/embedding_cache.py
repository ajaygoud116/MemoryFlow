# utils\embedding_cache.py


from models.embedding_model import (
    EMBEDDING_MODEL
)

model = EMBEDDING_MODEL


def get_embedding(memory):

    if memory.embedding is None:

        memory.embedding = model.encode(
            memory.text,
            convert_to_tensor=True
        )

    return memory.embedding