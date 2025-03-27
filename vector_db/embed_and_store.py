from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)
metadata = []

def add_to_vector_store(text, title, tags, video_url):
    embedding = model.encode([text])[0]
    index.add(np.array([embedding]))
    
    # Extract YouTube video ID
    video_id = video_url.split("v=")[-1].split("&")[0]
    embed_url = f"https://www.youtube.com/embed/{video_id}?start=0&end=30&autoplay=0"

    metadata.append({
        "title": title,
        "summary": text,
        "tags": tags,
        "video_url": video_url,
        "embed_url": embed_url
    })

def save_metadata(path="output/youtube_embeddings.json"):
    os.makedirs("output", exist_ok=True)
    with open(path, "w") as f:
        json.dump(metadata, f, indent=2)
