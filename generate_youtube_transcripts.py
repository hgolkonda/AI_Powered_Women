from youtube_transcript_api import YouTubeTranscriptApi


def generate_youtube_transcript(video_id: str) -> str:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([entry["text"] for entry in transcript])


def save_youtube_transcript(youtube_link: str, output_dir: str):
    video_id = youtube_link.split("watch?v=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([entry["text"] for entry in transcript])
    with open(f"{output_dir}/{video_id}.txt", "w") as f:
        f.write(text)


if __name__ == "__main__":
    output_dir = "data/video/transcripts"
    youtube_links = []
    with open("data/video/youtube_links.txt", "r") as f:
        for line in f:
            youtube_links.append(line.strip())

    for link in youtube_links:
        save_youtube_transcript(link, output_dir)
