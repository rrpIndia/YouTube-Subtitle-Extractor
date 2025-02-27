#!/data/data/com.termux/files/usr/bin/python3

import yt_dlp
import requests
import os
from youtube_transcript_api import YouTubeTranscriptApi
import subprocess
import json
from typing import List, Optional
from sys import exit
from dotenv import load_dotenv, dotenv_values

load_dotenv()

debug = True # Enable debug prints

def deb(message):
    if debug:
        print(f"[DEBUG] {message}")

class FileManagment:
    def __init__(self, file):
        self.file = file
        deb(f"FileManager initialized with file: {self.file}")

    def channel_list(self):
        try:
            with open(self.file, 'r') as f:
                content = f.read()
                deb(f"File content read: {content}")
                if not content.strip():
                    print(f'file is empty: {self.file}')
                    return []
                channels = [line.strip() for line in content.splitlines()]
                deb(f"Channels extracted: {channels}")
                return channels
        except FileNotFoundError:
            print(f'file not found {self.file}')
            return []

def get_links_to_file(channel_url: str) -> Optional[List[str]]:
    deb(f"Getting links for channel: {channel_url}")
    command = [
        "yt-dlp",
        '--simulate',
        '--no-quiet',
        '--lazy-playlist',
        "--dateafter", "now-3day",
        "--break-on-reject",
        '--force-write-archive', "--download-archive", "/data/data/com.termux/files/home/storage/shared/study/languages/python/codes/yt_rrp/archive.txt",
        "--print-to-file", '%(.{channel,title,upload_date,webpage_url})#j', 'urls_to_extract.json',
        channel_url
    ]

    deb(f"yt-dlp command: {command}")
    result = subprocess.run(command, capture_output=True, text=True)
    deb(f"yt-dlp result: {result}")
    if result.stdout:
        result = result.stdout.strip().split('\n')
        deb(f"yt-dlp stdout split: {result}")
        return result
    else:
        deb("yt-dlp stdout is empty.")
        return None

def get_title(channel_id: str):
    deb(f"Getting title for channel ID: {channel_id}")
    command = [
        'yt-dlp',
        '--get-title',
        channel_id
    ]
    deb(f"yt-dlp get-title command: {command}")
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout.strip()
    deb(f"Title: {result}")
    return result

def get_yt_subtitles(video_id):
    deb(f"Getting subtitles for video ID: {video_id}")
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=('hi', 'en'), preserve_formatting=True)
        transcript_text = " ".join([entry['text'] for entry in transcript])
        deb(f"Subtitles extracted: {transcript_text[:100]}...") # Print first 100 chars for brevity
        return transcript_text
    except Exception as e:
        print("Error:", e)
        deb(f"Error getting subtitles: {e}")

def get_id(vid_url):
    deb(f"Getting video ID from URL: {vid_url}")
    video_id = vid_url.split('v=')[1].split('&')[0]
    deb(f"Video ID: {video_id}")
    return video_id

def get_id_from_json(file: str) -> List[str]:
    deb(f"Getting IDs from JSON file: {file}")
    with open(file, 'r') as f:
        ids = json.load(f)
        deb(f"IDs loaded from JSON: {ids}")
        return ids

def write_id_to_json(id: list) -> None:
    deb(f"Writing IDs to JSON file: {id}")
    with open('video_id.json', 'w', encoding='utf-8') as f:
        json.dump(id, f, ensure_ascii=False, indent=4)
    deb("IDs written to JSON file.")

def send_to_tg(message):
    deb(f"Sending message to Telegram: {message}")
    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    deb(f"Telegram API request: {params}")
    response = requests.get(url, params=params)
    deb(f"Telegram API response: {response.json()}")
    return response.json()

# for a single session
to_download = FileManagment('channels.txt')
for i in to_download.channel_list():
    deb(f"Processing channel: {i}")
    get_links_to_file(i)
