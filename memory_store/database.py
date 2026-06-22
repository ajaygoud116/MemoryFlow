# memory_store\database.py



import sqlite3
import json
from core.memory import Memory


DB_PATH = "memoryflow.db"


def init_db():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            memory_id INTEGER PRIMARY KEY,
            text TEXT,
            compressed_text TEXT,
            entities TEXT,
            numbers TEXT,
            constraints TEXT,
            noun_chunks TEXT,
            memory_type TEXT,
            topic TEXT,
            value TEXT,
            tier TEXT,
            active INTEGER,
            relevance_score REAL,
            recency_score REAL,
            frequency_score REAL,
            redundancy_score REAL,
            amis_score REAL,
            retrieval_count INTEGER,
            created_position INTEGER,
            created_at REAL,
            metadata TEXT
        )
    """)

    conn.commit()
    conn.close()


def serialize(memory: Memory):

    return (
        memory.memory_id,
        memory.text,
        memory.compressed_text,
        json.dumps(memory.entities),
        json.dumps(memory.numbers),
        json.dumps(memory.constraints),
        json.dumps(memory.noun_chunks),
        memory.memory_type,
        memory.topic,
        memory.value,
        memory.tier,
        int(memory.active),
        memory.relevance_score,
        memory.recency_score,
        memory.frequency_score,
        memory.redundancy_score,
        memory.amis_score,
        memory.retrieval_count,
        memory.created_position,
        memory.created_at,
        json.dumps(memory.metadata),
    )


def deserialize(row):

    return Memory(
        text=row[1],
        entities=json.loads(row[3]),
        numbers=json.loads(row[4]),
        constraints=json.loads(row[5]),
        noun_chunks=json.loads(row[6]),
        memory_type=row[7],
        topic=row[8],
        value=row[9],
        compressed_text=row[2],
        active=bool(row[11]),
        relevance_score=row[12],
        recency_score=row[13],
        frequency_score=row[14],
        redundancy_score=row[15],
        amis_score=row[16],
        retrieval_count=row[17],
        created_position=row[18],
        created_at=row[19],
        metadata=json.loads(row[20]),
    )


def save_memory(memory: Memory):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO memories VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, serialize(memory))

    conn.commit()
    conn.close()


def load_all_memories():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM memories")
    rows = cursor.fetchall()

    conn.close()

    return [deserialize(row) for row in rows]