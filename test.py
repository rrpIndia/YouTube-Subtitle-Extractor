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

class FileManagment:
    def __init__(self, file):
        self.file = file
    def channel_list(self):
        try:
            with open(self.file, 'r') as f:
                content = f.read()
                if not content.strip():
                    print(f'file is empty: {self.file}')
                    return []
                channels = [ line.strip() for line in content.splitlines() ]
                return channels
        except FileNotFoundError:
            print(f'file not found {self.file}')
            return []




def get_links_to_file(channel_url: str) -> Optional[List[str]]:
    command = [
        "yt-dlp",
        '--simulate',
        '--lazy-playlist',
        "--dateafter", "now-1day",
        "--break-on-reject",
        '--force-write-archive', "--download-archive", "/data/data/com.termux/files/home/storage/shared/study/languages/python/codes/yt_rrp/archive.txt",
        "--print-to-file", "webpage_url", 'urls_to_extract.txt',

        channel_url
    ]

    # Run yt-dlp and capture output
    result = subprocess.run(command, capture_output=True, text=True)
    if result.stdout:
        result = result.stdout.strip().split('\n') #turning to list, stripped because there is a newline at last line
        return result
    else:
        #sometimes output will have no string we cant turn that into a list
        #it was a major bug, took my 3 hours
        return None

def get_title(channel_id: str):
    command = [
            'yt-dlp',
            '--get-title',
            channel_id
            ]
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout.strip()
    return result

def get_yt_subtitles(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=('hi','en'), preserve_formatting=True)
        
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text
    
    except Exception as e:
        print("Error:", e)

def get_id(vid_url):
    video_id = vid_url.split('v=')[1].split('&')[0]
    return video_id 

def get_id_from_json(file: str) -> List[str]:
    with open(file, 'r') as f:
        ids = json.load(f)
        return ids

def write_id_to_json(id: list) -> None:
    with open('video_id.json', 'w', encoding='utf-8') as f:
        
        json.dump(id, f, ensure_ascii=False, indent=4)

def send_to_tg(message):
    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
    'chat_id': chat_id,
    'text': message,
    'parse_mode': 'HTML'
}
    response = requests.get(url, params=params)
    return response.json()


# for a single session

to_download = FileManagment('urls_to_extract.txt')
print(to_download.channel_list())
