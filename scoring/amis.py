# scoring\amis.py


from models.embedding_model import (
    EMBEDDING_MODEL
)
from sentence_transformers import util

model = EMBEDDING_MODEL




def compute_importance(memory):

    score = 0
    reasons = []

    # -------------------------
    # Base type importance
    # -------------------------
    if memory.memory_type == "constraint":
        score += 40
        reasons.append("constraint")

    elif memory.memory_type == "fact":
        score += 40
        reasons.append("fact")

    elif memory.memory_type == "preference":
        score += 25
        reasons.append("preference")

    else:
        reasons.append("general")

    # -------------------------
    # Safety / constraints boost
    # -------------------------
    if memory.memory_type == "constraint":
        score += 15
        reasons.append("constraint_memory")

    # -------------------------
    # Numeric importance
    # -------------------------
    if memory.numbers:
        score += 20
        reasons.append("contains_numbers")

    # -------------------------
    # Entity richness
    # -------------------------
    entity_score = min(len(memory.entities) * 5, 20)
    score += entity_score

    if memory.entities:
        reasons.append("entity_rich")

    # -------------------------
    # Critical topic detection
    # -------------------------
    # -------------------------
    # Store explainability
    # -------------------------
    memory.metadata["why_important"] = reasons

    return min(score, 100)


def compute_relevance(memory, query):

    source_text = (
        memory.compressed_text
        if memory.compressed_text
        else memory.text
    )

    emb1 = model.encode(source_text, convert_to_tensor=True)
    emb2 = model.encode(query, convert_to_tensor=True)

    similarity = util.cos_sim(emb1, emb2).item()

    return max(similarity, 0) * 100


def apply_decay(memory, current_turn):

    # Do not decay critical constraints
    if memory.memory_type == "constraint":
        return

    age = current_turn - memory.created_position

    if age <= 0:
        return

    decay_factor = getattr(
        memory,
        "importance_decay_rate",
        0.98
    )

    memory.amis_score *= (decay_factor ** age)

    memory.amis_score = max(0, memory.amis_score)


def compute_amis_score(memory, query):

    importance = compute_importance(memory)

    relevance = compute_relevance(memory, query)
    redundancy = memory.redundancy_score

    retrieval_success = memory.retrieval_success_rate


    score = (
        0.35 * importance +
        0.25 * relevance +
        0.15 * memory.recency_score +
        0.10 * memory.frequency_score +
        0.15 * retrieval_success
    )

    score -= (0.10 * redundancy)
    score -= 0.15 * memory.conflict_risk

    if memory.memory_type == "constraint":
        score += 25
        memory.metadata["protected_memory"] = True

    memory.amis_score = round(min(score, 100), 2)

    return memory.amis_score

def update_recency_score(memory, total_memories):

    if total_memories <= 1:
        memory.recency_score = 100
        return

    memory.recency_score = (
        memory.created_position /
        (total_memories - 1)
    ) * 100