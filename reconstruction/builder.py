# reconstruction\builder.py


def reconstruct_context(
    retrieved_memories
):

    critical = []
    preferences = []
    facts = []
    recent = []

    for memory, score in retrieved_memories:

        text = (

            memory.compressed_text

            if memory.compressed_text

            else memory.text

        )

        if memory.tier == "Tier 1":

            critical.append(text)

        elif memory.tier == "Tier 2":

            preferences.append(text)

        elif memory.tier == "Tier 3":

            facts.append(text)

        else:

            recent.append(text)

    sections = []

    if critical:

        sections.append(
            "Critical Constraints:"
        )

        for item in critical:

            sections.append(f"- {item}")

    if preferences:

        sections.append("\nPreferences:")

        for item in preferences:

            sections.append(f"- {item}")

    if facts:

        sections.append("\nFacts:")

        for item in facts:

            sections.append(f"- {item}")

    if recent:

        sections.append(
            "\nOther Context:"
        )

        for item in recent:

            sections.append(f"- {item}")

    return "\n".join(sections)