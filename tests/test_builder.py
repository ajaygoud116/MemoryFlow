# tests/test_builder.py

from extraction.extractor import extract_memory

from reconstruction.builder import (
    reconstruct_context
)

retrieved = [

    (
        extract_memory(
            "Budget is 2500 dollars"
        ),
        0.85
    ),

    (
        extract_memory(
            "Avoid seafood"
        ),
        0.72
    )
]

context = reconstruct_context(
    retrieved
)

print(context)