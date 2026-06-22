# lifecycle\memory_lifecycle.py



from datetime import datetime
from tiering.tier_manager import assign_tiers

class MemoryLifecycleEngine:

    """
    Handles:
    - forgetting
    - consolidation
    - promotion/demotion
    - archival cleanup
    """

    def __init__(self):

        self.decay_rate = 0.02  # general forgetting speed

        self.min_score_to_live = 5

    # ----------------------------
    # FORGETTING MECHANISM
    # ----------------------------
    def apply_forgetting(self, memory):

        if memory.memory_type == "constraint":
            return  # never forget constraints

        age = max(
            1,
            datetime.now().timestamp() - memory.created_at
        )

        age_hours = age / 3600
        decay = self.decay_rate * age_hours

        memory.amis_score -= decay

        memory.amis_score = max(
            0,
            memory.amis_score
        )

        if memory.amis_score < self.min_score_to_live:

            memory.active = False

            memory.metadata["archived_reason"] = "low_relevance"

    # ----------------------------
    # CONSOLIDATION
    # ----------------------------
    def consolidate(self, memory):

        """
        Strengthen important memories
        if they are frequently retrieved
        """

        if memory.retrieval_count > 5:

            memory.amis_score = min(
                100,
                memory.amis_score + 10
            )

            memory.metadata["consolidated"] = True


    # ----------------------------
    # FULL LIFECYCLE RUN
    # ----------------------------
    def run(self, memories):

        for memory in memories:

            self.apply_forgetting(memory)

            self.consolidate(memory)

        assign_tiers(memories)    

        return memories