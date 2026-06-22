# core\memory.py


from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Memory:

    # Original memory
    text: str

    # Extracted information
    entities: list
    numbers: list
    noun_chunks: list
    constraints: list = field(default_factory=list)
    

    # Memory classification
    memory_type: str = "unknown"

    # Topic tracking
    topic: Optional[str] = None
    value: Optional[str] = None

    # Compression
    compressed_text: Optional[str] = None

    # Active memory state
    active: bool = True

    # Scores
    relevance_score: float = 0.0
    recency_score: float = 0.0
    frequency_score: float = 0.0
    
    retrieval_success_rate: float = 0.0
    compression_cost: float = 0.0
    conflict_risk: float = 0.0
    retention_score: float = 0.0

    redundancy_score: float = 0.0
    amis_score: float = 0.0

    # Tiering
    tier: str = ""

    # Usage tracking
    retrieval_count: int = 0

    # Metadata
    memory_id: int = -1
    created_position: int = 0

    metadata: dict = field(default_factory=dict)

    # Embedding placeholder
    embedding: object = None

    # Optional timestamp for when the memory was created
    created_at: float = 0

    
