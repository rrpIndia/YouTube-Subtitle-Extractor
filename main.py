#!/data/data/com.termux/files/usr/bin/python3
import re
import yt_dlp
import requests
import os
from youtube_transcript_api import YouTubeTranscriptApi
import subprocess
import json
from typing import List, Optional
from sys import exit
from glob import glob
from datetime import datetime
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
                    exit(f'file is empty: {self.file}')

                channels = [line.strip() for line in content.splitlines()]
                return channels
        except FileNotFoundError:
            print(f'file not found {self.file}')
            return []

    def read_json(self, json_file):
        self.json_file = json_file
        try:
            with open(self.json_file, 'r') as f:
                data_dict = json.load(f)
                return data_dict
        except FileNotFoundError:
            print(f'file is not available')
            return None

    def make_json_files_of_urls():
        for channel in self.channel_list():
            get_links_to_file(channel)


    def get_links_to_file(self, channel_url: str) -> Optional[List[str]]:
        self.channel_url = channel_url
        command = [
            "yt-dlp",
            '--simulate',
            '--no-quiet',
            '--lazy-playlist',
            "--dateafter", "now-3day",
            "--break-on-reject",
            '--force-write-archive', "--download-archive", "/data/data/com.termux/files/home/storage/shared/study/languages/python/codes/yt_rrp/archive.txt",
            "--print-to-file", '%(.{channel,title,upload_date,webpage_url})#j', 'url_extract_%(autonumber)d.json',
            self.channel_url
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        if result.stdout:
            result = result.stdout.strip().split('\n')
            return result
        else:
            return None

    def get_files(self, match='url_extract_*.json'):
        self.match = match
        '''will return empty list if no files are available or matching'''
        files = glob(self.match)
        return files

class Sender:
    def __init__(self, message):
        self.message = message
        
    def send_to_tg(self):
        bot_token = os.getenv("BOT_TOKEN")
        chat_id = os.getenv("CHAT_ID")
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        params = {
            'chat_id': chat_id,
            'text': self.message,
            'parse_mode': 'HTML'
        }
        response = requests.get(url, params=params)
        return response.json()   

class Video:
    def __init__(self, vid_url):
        self.vid_url = vid_url
        self.vid_id = self.get_id()
        self.subtitle = self.get_subtitle()

    def get_id(self)-> Optional[str]:
        data = re.findall(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", self.vid_url)
        if data:
            return data[0]
        return None

    def get_subtitle(self):
        vid_id = self.get_id()
        try:
            transcript = YouTubeTranscriptApi.get_transcript(vid_id, languages=('hi', 'en'), preserve_formatting=True)
            transcript_text = " ".join([entry['text'] for entry in transcript])
            return transcript_text
        except Exception as e:
            print("Error:", e)



# for a single session

def main():
    files = FileManagment('channels.txt')
    files.make_json_files_of_urls
    for dic in files.get_files():
        json_dict = files.read_json(dic)
        yt = Video(link)

        title = json_dict['title']
        upload_date = datetime.strptime(json_dict['upload_date'], "%Y%m%d").date()
        channel_name = json_dict['channel']
        link = json_dict['webpage_url']
        subtitle = yt.subtitle

        message = f'''
        <b>{title}\n\n\n</b>
        {link}
        {upload_date}
        <u>Channel: {channel_name}\n\n\n </u>
        {subtitle}'''

        messages = [ message[i:i+4095] for i in range(0, len(message), 4095) ]
        for message in messages:
            print(message)
        os.remove(dic)


if __name__ == '__main__':
    main()
