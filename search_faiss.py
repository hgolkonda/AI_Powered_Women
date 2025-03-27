# 📁 File: search_faiss.py

import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# ✅ Load model & index
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("vector_store/faiss_index.idx")

# ✅ Load metadata
with open("vector_store/metadata.json", "r") as f:
    metadata = json.load(f)

# 🔍 User query
query = input("Ask your AI learning assistant: ")
query_vec = model.encode([query])

# 🧠 Search top 3
k = 3
distances, indices = index.search(np.array(query_vec), k)

# 📦 Show Results
print("\n🔍 Top 3 Results:\n")
for i, idx in enumerate(indices[0]):
    item = metadata[idx]
    print(f"[{i+1}] {item['title']}")
    print(f"    Type: {item['type']}")
    print(f"    Tags: {', '.join(item['tags'])}")
    print(f"    Summary: {item['summary'][:200]}...")
    print(f"    Link: {item['source_url']}\n")
