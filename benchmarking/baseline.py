# benchmarking/baseline.py

from sentence_transformers import util

from models.embedding_model import (
    EMBEDDING_MODEL
)

model = EMBEDDING_MODEL

class BaselineAgent:

    def __init__(self):

        self.embedding_cache = {}

    def build_context(self,conversation,query,top_k=5):
        query_emb = model.encode(query,convert_to_tensor=True)

        scored = []

        for text in conversation:

            if text not in self.embedding_cache:

                self.embedding_cache[text] = model.encode(text,convert_to_tensor=True)

            similarity = util.cos_sim(query_emb,self.embedding_cache[text]).item()

            scored.append((similarity,text))

        scored.sort(key=lambda x: x[0],reverse=True)

        selected = [text for _, text in scored[:top_k]]

        return "\n".join(selected)