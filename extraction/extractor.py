# extraction\extractor.py



import json
import spacy

import ollama
from tomlkit import value



from core.memory import Memory
from utils.embedding_cache import get_embedding


nlp = spacy.load("en_core_web_sm")






def llm_extract_memory(text):

    prompt = f"""
You are a memory extraction engine.

Extract structured memory information.

Return ONLY valid JSON.

Schema:

{{
    "topic": "",
    "value": "",
    "memory_type": "",
    "compressed_text": "",
    "reason": ""
}}

Rules:

memory_type must be one of:

- constraint
- preference
- fact
- chatter

Examples:

Input:
"I am allergic to shellfish."

Output:
{{
    "topic":"allergy",
    "value":"shellfish",
    "memory_type":"constraint",
    "compressed_text":"Shellfish allergy.",
    "reason":"Health constraint."
}}

Input:
"I prefer aisle seats."

Output:
{{
    "topic":"seat_preference",
    "value":"aisle",
    "memory_type":"preference",
    "compressed_text":"Prefers aisle seats.",
    "reason":"User preference."
}}

Memory Text:

{text}
"""

    try:

        response = ollama.chat(
            model="llama3",
            format="json",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response["message"]["content"]
        print("\nRAW OLLAMA OUTPUT")
        print(content)
        
        return json.loads(content)          
    


    except Exception:

        return {
            "topic": None,
            "value": None,
            "memory_type": "chatter",
            "compressed_text": text,
            "reason": "fallback"
        }


def extract_memory(text):

    doc = nlp(text)

    entities = []
    numbers = []

    noun_chunks = [
        chunk.text
        for chunk in doc.noun_chunks
    ]

    for ent in doc.ents:

        entities.append(
            (
                ent.text,
                ent.label_
            )
        )

    for token in doc:

        if token.like_num:

            numbers.append(
                token.text
            )


    structured = llm_extract_memory(text)

    print("\nEXTRACTED")
    print(structured)

    topic = structured.get(
        "topic"
    )

    value = structured.get(
        "value"
    )

    memory_type = structured.get(
        "memory_type",
        "chatter"
    )

    compressed_text = structured.get(
        "compressed_text",
        text
    )


    memory = Memory(

        text=text,

        entities=entities,

        numbers=numbers,

        constraints=[],

        noun_chunks=noun_chunks,

        memory_type=memory_type,

        topic=topic,

        value=value,

        compressed_text=compressed_text

    )

    memory.embedding =get_embedding(memory)

    memory.metadata[
        "extraction_reason"
    ] = structured.get(
        "reason",
        ""
    )
    if topic:
        memory.topic_embedding = (get_embedding(Memory(text=topic,entities=[],numbers=[],noun_chunks=[])))

    if value:
        memory.value_embedding = (get_embedding(Memory(text=str(value),entities=[],numbers=[],noun_chunks=[])))
    return memory