#!/data/data/com.termux/files/usr/bin/python3

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import subprocess

def get_links(channel_url: str):
    command = [
        "yt-dlp",
        "--ignore-errors",
        "--dateafter", "now-1week",
        "--break-on-reject",
        "--print", "webpage_url",
        #"--download-archive", "$HOME//data/log/yt_rrp.txt",  # Keep track of downloaded videos
        channel_url
    ]

    # Run yt-dlp and capture output
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

# Function to get subtitles from a YouTube video link
def get_youtube_subtitles():
    try:
        # Extract the video ID from the URL
        video_id = 'DskRAuw8vxk'.strip()
        
        # Get the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=('hi','en'), preserve_formatting=True)
        
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text
    
    except Exception as e:
        print("Error:", e)

print(get_links('https://m.youtube.com/c/fireship'))
