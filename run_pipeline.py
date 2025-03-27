# 📁 File: run_full_pipeline.py

from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urlparse

# 🎯 Init
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.IndexFlatL2(384)
metadata = []
CHUNK_SECONDS = 30

# 🎥 VIDEO PIPELINE
video_links = [
    ("https://www.youtube.com/watch?v=ad79nYk2keg", "AI Crash Course - Intro", ["AI course", "playlist", "video", "course lecture"]),
    ("https://www.youtube.com/watch?v=8Pyy2d3SZuM", "AI Crash Course - Part 2", ["AI course", "playlist", "video", "course lecture"]),
    ("https://www.youtube.com/watch?v=sp_OMFCfGMw", "AI Crash Course - Part 3", ["AI course", "playlist", "video", "explainer"]),
    ("https://www.youtube.com/watch?v=anTjbDH6y-Y", "AI Crash Course - Part 4", ["AI course", "playlist", "video", "course lecture"]),
    ("https://www.youtube.com/watch?v=ua-CiDNNj30", "Learn Data Science Tutorial - Full Course for Beginners", ["Data Science course", "video", "course lecture", "beginner"]),
    ("https://www.youtube.com/watch?v=LHBE6Q9XlzI", "Python for Data Science - Course for Beginners", ["Data Science course", "video", "python", "numpy", "pandas", "matplotlib"]),
    ("https://www.youtube.com/watch?v=GPVsHOlRBBI", "Data Analysis with Python Course", ["Data Science course", "video", "data analysis", "pandas", "visualization"]),
    ("https://www.youtube.com/watch?v=anTjbDH6y-Y", "Build 12 Data Science Apps with Python and Streamlit", ["Data Science course", "video", "streamlit", "app building", "python"])
]

def get_chunks(video_url):
    video_id = video_url.split("v=")[-1].split("&")[0]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    chunks = []
    chunk = []
    current_start = 0
    for entry in transcript:
        if entry['start'] < current_start + CHUNK_SECONDS:
            chunk.append(entry['text'])
        else:
            chunks.append({"start": current_start, "end": current_start + CHUNK_SECONDS, "text": " ".join(chunk)})
            current_start += CHUNK_SECONDS
            chunk = [entry['text']]
    if chunk:
        chunks.append({"start": current_start, "end": current_start + CHUNK_SECONDS, "text": " ".join(chunk)})
    return chunks, video_id

def add_video_chunks(chunks, title, tags, content_type, video_url, video_id):
    for i, chunk in enumerate(chunks):
        embedding = model.encode([chunk['text']])[0]
        index.add(np.array([embedding]))
        embed_url = f"https://www.youtube.com/embed/{video_id}?start={chunk['start']}&end={chunk['end']}&autoplay=0"
        metadata.append({
            "title": title,
            "summary": chunk['text'],
            "tags": tags,
            "content_type": content_type,
            "type": "video",
            "source_url": embed_url,
            "embed_url": embed_url,
        })

# 📝 BLOG PIPELINE
blog_urls = [
    "https://www.datasciencecentral.com/",
    "https://www.smartdatacollective.com/",
    "https://whatsthebigdata.com/",
    "http://blog.kaggle.com/",
    "https://insidebigdata.com/"
]

def scrape_blogs():
    for url in blog_urls:
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            title_tag = soup.find('h1') or soup.find('h2')
            title = title_tag.get_text(strip=True) if title_tag else urlparse(url).netloc
            paragraphs = soup.find_all('p')
            summary = " ".join(p.get_text(strip=True) for p in paragraphs[:4])[:500]
            metadata.append({
                "title": title,
                "summary": summary,
                "tags": ["blog", "data science", "article"],
                "content_type": "blog",
                "type": "blog",
                "source_url": url,
               
            })
        except Exception as e:
            print(f"⚠️ Failed to scrape {url}: {e}")

# 🚀 RUN PIPELINE
for url, title, tags in video_links:
    try:
        yt = YouTube(url)
        chunks, video_id = get_chunks(url)
        add_video_chunks(chunks, title, tags, tags[-1], url, video_id)
    except Exception as e:
        print(f"⚠️ Skipped {url}: {e}")

scrape_blogs()

# 💾 Save all in unified format
os.makedirs("output", exist_ok=True)
with open("output/unified_content.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("✅ Final unified content saved to output/unified_content.json")