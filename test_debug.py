#!/data/data/com.termux/files/usr/bin/python3

import yt_dlp
import requests
import os
from youtube_transcript_api import YouTubeTranscriptApi
import subprocess
import json
from typing import List, Optional
from sys import exit
from glob import glob
from dotenv import load_dotenv, dotenv_values

load_dotenv()

debug = True# Enable debug prints

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

    def read_json(self):
        try:
            with open(self.file, 'r') as f:
                deb(f"opening file: {self.file}")
                data_dict = json.load(f)
                deb(f'loaded data from file: {data_dict}')
                return data_dict
        except FileNotFoundError:
            print(f'file is not available')
            deb(f'file is not available')
            return None

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
        "--print-to-file", '%(.{channel,title,upload_date,webpage_url})#j', 'url_extract_%(autonumber)d.json',
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

def get_files(match='url_extract_*.json'):
    '''will return empty list if no files are available or matching'''
    files = glob(match)
    return files

def get_id(vid_url):
    deb(f'video_url is: {vid_url}')
    deb(f'getting ready to extract video id')
    video_id = vid_url.split('v=')[1].split('&')[0]
    deb(f'video id is: {video_id}')
    return video_id 

def get_subtitle(video_url):
    deb(f"Getting subtitles for video URL: {video_url}")
    video_id = get_id(video_url)
    deb(f'got video id: {video_id}')
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=('hi', 'en'), preserve_formatting=True)
        transcript_text = " ".join([entry['text'] for entry in transcript])
        deb(f"Subtitles extracted: {transcript_text[:100]}...") # Print first 100 chars for brevity
        return transcript_text
    except Exception as e:
        print("Error:", e)
        deb(f"Error getting subtitles: {e}")


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
def make_json_files_of_urls():
    deb(f'making json files from urls to extract later')
    to_download = FileManagment('channels.txt')
    for channel in to_download.channel_list():
        deb(f"Processing channel: {channel}")
        get_links_to_file(channel)

#make_json_files_of_urls()

for dic in get_files():
    json_file = FileManagment(dic)
    json_dict = json_file.read_json()

    title = json_dict['title']
    channel_name = json_dict['channel']
    link = json_dict['webpage_url']
    subtitle = get_subtitle(link)

    message = f'''
    <b>{title}\n\n\n</b>
    {link}
    <u>Channel: {channel_name}\n\n\n </u>
    {subtitle}'''

    messages = [ message[i:i+4095] for i in range(0, len(message), 4095) ]
    for message in messages:
        send_to_tg(message)
    os.remove(dic)
    deb(f'removed file: {dic}')
