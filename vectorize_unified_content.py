# 📁 File: vectorize_unified_content.py

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# ✅ Load data
with open("output/unified_content.json", "r") as f:
    data = json.load(f)

# ✅ Initialize model & FAISS index
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.IndexFlatL2(384)
metadata = []

# ✅ Generate embeddings and store metadata
for item in data:
    summary = item.get("summary")
    if summary:
        embedding = model.encode([summary])[0]
        index.add(np.array([embedding]))
        metadata.append(item)

# ✅ Save FAISS index and metadata
os.makedirs("vector_store", exist_ok=True)
faiss.write_index(index, "vector_store/faiss_index.idx")
with open("vector_store/metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("✅ Vector embeddings saved to vector_store/")
