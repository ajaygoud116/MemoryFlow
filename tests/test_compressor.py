# tests/test_compressor.py

from extraction.extractor import extract_memory

from compression.compressor import compress_memory


m1 = extract_memory(
    "Budget is 2500 dollars"
)

m1.tier = "Tier 1"

m2 = extract_memory(
    "Need luxury hotel near beach"
)

m2.tier = "Tier 2"

m3 = extract_memory(
    "Weather forecast indicates sunny conditions throughout the week"
)

m3.tier = "Tier 3"

m4 = extract_memory(
    "Hello"
)

m4.tier = "Tier 4"

print(
    compress_memory(m1)
)

print(
    compress_memory(m2)
)

print(
    compress_memory(m3)
)

print(
    compress_memory(m4)
)