from typing import Dict, Optional, Tuple
from sentence_transformers import util
import numpy as np


class ConflictManager:
    """
    Robust semantic + structural conflict resolution engine for memory systems.
    Designed for high-noise LLM memory ingestion pipelines.
    """

    def __init__(
        self,
        conflict_threshold: float = 0.70,
        identity_threshold: float = 0.92
    ):
        self.conflict_threshold = conflict_threshold
        self.identity_threshold = identity_threshold

    # -----------------------------
    # SAFE VECTOR NORMALIZATION
    # -----------------------------
    def cosine(self, a, b) -> float:
        """
        Safe cosine similarity in [0,1] space.
        Handles tensors, lists, numpy arrays, and None.
        """
        if a is None or b is None:
            return 0.0

        try:
            sim = util.cos_sim(a, b).item()
            # clamp for numerical safety
            sim = max(-1.0, min(1.0, sim))
            return (sim + 1.0) / 2.0
        except Exception:
            return 0.0

    # -----------------------------
    # FEATURE ENGINE
    # -----------------------------
    def extract_features(self, new, old) -> np.ndarray:
        """
        Multi-axis semantic comparison:
        [topic, value, context, polarity_conflict]
        """

        topic_similarity = self.cosine(
            getattr(new, "topic_embedding", None),
            getattr(old, "topic_embedding", None)
        )

        value_similarity = self.cosine(
            getattr(new, "value_embedding", None),
            getattr(old, "value_embedding", None)
        )

        context_similarity = self.cosine(
            getattr(new, "embedding", None),
            getattr(old, "embedding", None)
        )

        # -----------------------------
        # POLARITY CONFLICT DETECTION
        # -----------------------------
        polarity_conflict = 0

        new_pol = getattr(new, "polarity", None)
        old_pol = getattr(old, "polarity", None)

        if new_pol is not None and old_pol is not None:

            # Strong rule:
            # same topic + opposite polarity = conflict
            if new_pol != old_pol and topic_similarity > 0.70:
                polarity_conflict = 1

        return np.array([
            topic_similarity,
            value_similarity,
            context_similarity,
            float(polarity_conflict)
        ], dtype=np.float32)

    # -----------------------------
    # SCORING MODEL
    # -----------------------------
    def score(self, f: np.ndarray) -> float:
        """
        Weighted conflict scoring function.
        """

        topic, value, context, polarity = f

        # weak signal filter
        if topic < 0.45 and context < 0.45:
            return 0.0

        # core conflict equation
        score = (
            0.35 * topic +
            0.25 * context +
            0.25 * (1.0 - value) +
            0.15 * polarity
        )

        return float(score)

    # -----------------------------
    # MAIN DECISION ENGINE
    # -----------------------------
    def detect_conflict(self, new, old) -> Tuple[bool, Optional[Dict]]:

        if not getattr(old, "active", False):
            return False, None

        features = self.extract_features(new, old)
        topic, value, context, polarity = features

        # -----------------------------
        # MERGE CASE (IDENTITY)
        # -----------------------------
        if (
            topic >= 0.85 and
            value >= self.identity_threshold
        ):
            new.conflict_risk = 0
            return False, {
                "action": "MERGE",
                "confidence": round(float(value), 3),
                "reason": "IDENTICAL_SEMANTIC_STATE"
            }

        # -----------------------------
        # CONFLICT SCORE
        # -----------------------------
        conflict_score = self.score(features)

        if conflict_score < self.conflict_threshold:
            return False, None

        # -----------------------------
        # CONFLICT CASE
        # -----------------------------
        new.conflict_risk = 100
        return True, {
            "conflict": True,
            "action": "REPLACE",
            "confidence": round(conflict_score, 3),
            "reason": "SEMANTIC_STATE_MUTATION",
            "features": {
                "topic": round(float(topic), 3),
                "value": round(float(value), 3),
                "context": round(float(context), 3),
                "polarity": int(polarity)
            }
        }

    # -----------------------------
    # RESOLUTION ENGINE
    # -----------------------------
    def resolve_conflict(self, new_memory, old_memory, report: Dict):

        if not report:
            return old_memory

        action = report.get("action")

        # -------------------------
        # REPLACE OLD MEMORY
        # -------------------------
        if action == "REPLACE":

            # timestamp-aware override safety
            new_time = getattr(new_memory, "created_at", 0)
            old_time = getattr(old_memory, "created_at", 0)

            # prevent stale overwrite
            if new_time < old_time:
                return old_memory

            old_memory.active = False
            old_memory.metadata["archived_reason"] = "semantic_conflict_override"
            old_memory.metadata["conflict_report"] = report

        # -------------------------
        # MERGE INCREMENT
        # -------------------------
        elif action == "MERGE":
            old_memory.retrieval_count = getattr(old_memory, "retrieval_count", 0) + 1
            old_memory.metadata["conflict_report"] = report

        return old_memory