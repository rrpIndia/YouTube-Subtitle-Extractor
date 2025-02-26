#!/data/data/com.termux/files/usr/bin/python3

import yt_dlp
import requests
import os
from youtube_transcript_api import YouTubeTranscriptApi
import subprocess
import json
from typing import List
from dotenv import load_dotenv, dotenv_values

load_dotenv()

with open('channels.txt', 'r') as f:
    channels = f.read().split()

def get_links(channel_url: str):
    command = [
        "yt-dlp",
        '--simulate',
        '--lazy-playlist',
        "--dateafter", "now-1day",
        "--break-on-reject",
        '--force-write-archive', "--download-archive", "/data/data/com.termux/files/home/storage/shared/study/languages/python/codes/yt_rrp/archive.txt",
        "--print", "webpage_url",

        channel_url
    ]

    # Run yt-dlp and capture output
    result = subprocess.run(command, capture_output=True, text=True)
    result = result.stdout.strip().split('\n') #turning to list, stripped because there is a newline at last line
    print(result)
    return result

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

for channel in channels:
    for video in get_links(channel):
        vid_id = get_id(video)
        id_list = get_id_from_json('video_id.json')
        if vid_id in id_list:
            print(f'already exists: {vid_id}')
            pass
        else:
            id_list.append(vid_id)
            write_id_to_json(id_list)
            sub = get_yt_subtitles(vid_id)
            title = get_title(vid_id)

            message = f'<b>{title}</b>\n\n' + sub
            # sometimes message is too long, > 4096characters
            messages = [ message[i:i+4095] for i in range(0, len(message), 4095) ]
            for message in messages:
                print(send_to_tg(message=message))
                print(type(message))


