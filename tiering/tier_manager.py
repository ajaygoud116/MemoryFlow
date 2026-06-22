# tiering/tier_manager.py

def assign_tiers(memories):

    if len(memories) == 0:
        return memories

    active_memories = [
        m for m in memories
        if m.active
    ]

    if len(active_memories) == 0:
        return memories


    # -------------------------
    # Assign tiers
    # -------------------------

    for memory in memories:

        if not memory.active:
            memory.tier = "Archived"
            continue
        
        if memory.memory_type == "constraint":
            memory.tier = "Tier 1"
            continue

        score = memory.amis_score
        if score >= 70:
            memory.tier = "Tier 1"

        elif score >= 50:
            memory.tier = "Tier 2"

        elif score >= 30:
            memory.tier = "Tier 3"

        else:
            memory.tier = "Tier 4"

    return memories