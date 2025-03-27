from youtube_transcript_api import YouTubeTranscriptApi

def get_30_sec_transcript(video_url):
    video_id = video_url.split("v=")[-1].split("&")[0]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    lines = []
    for entry in transcript:
        if entry['start'] <= 30:
            lines.append(entry['text'])
        else:
            break

    return " ".join(lines), video_id
