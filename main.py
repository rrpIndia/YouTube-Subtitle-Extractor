#!/data/data/com.termux/files/usr/bin/python3
import re
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
CHANNEL_FILE = '/data/data/com.termux/files/home/storage/shared/study/languages/python/codes/yt_rrp/channels.txt'

class FileManagment:
    def __init__(self, file):
        '''takes file of channel list as input'''
        self.file = file
        self.channel_list = self.channel_list()

def channel_list(channel_file) -> list:
    "" "takes a file of channel per line and generate a python list"""
    try:
        with open(channel_file, 'r') as f:
            content = f.read()
            if not content.strip():
                exit(f'file is empty: {self.file}')

            channels = [line.strip() for line in content.splitlines()]
            return channels
    except FileNotFoundError:
        print(f'file not found {self.file}')
        return []

def read_json(json_file):
    try:
        with open(json_file, 'r') as f:
            data_dict = json.load(f)
            return data_dict
    except FileNotFoundError:
        print(f'file is not available')
        return None

def make_json_files_of_urls(channel_list: list) -> None:
    for channel in channel_list:
        get_links_to_file(channel)


def get_link_to_file(channel_url: str) -> Optional[List[str]]:
    '''takes a url of channel as input and make json files of newly released video'''
    print(f'started making json file for {channel_url}')


    #in second loop, program will put json data into already created files because %autoincrement does not know in  which iteration it is
    # that is why channel name is must 
    command = [
        "yt-dlp",
        '--simulate',
        '--no-quiet',
        '--lazy-playlist',
        "--dateafter", "now-3day",
        "--break-on-reject",
        '--force-write-archive', "--download-archive", "/data/data/com.termux/files/home/storage/shared/study/languages/python/codes/yt_rrp/archive.txt",
        "--print-to-file", '%(.{channel,title,upload_date,webpage_url})#j', f'url_extract_{self.channel_url.split('/')[-1]}_%(autonumber)d.json',
        channel_url
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.stdout:
        result = result.stdout.strip().split('\n')
        print(result)
        return result
    return None

def get_files(match='url_extract_*.json')-> list:
    '''will return empty list if no files are available or matching'''
    files = glob(self.match)
    return files

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
   
def get_id(vid_url: str)-> Optional[str]:
    data = re.findall(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", vid_url)
    if data:
        return data[0]
    return None

def get_subtitle(vid_id) -> str:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(vid_id, languages=('hi', 'en'), preserve_formatting=True)
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text
    except Exception as e:
        print("Error:", e)



# for a single session

def main():
    files = FileManagment(CHANNEL_FILE)
    print(f'initialising FileManagment Class')
    files.make_json_files_of_urls()
    print(f'making json files')
    for dic in files.get_files():
        json_dict = files.read_json(dic)

        title = json_dict['title']
        upload_date = datetime.strptime(json_dict['upload_date'], "%Y%m%d").date()
        channel_name = json_dict['channel']
        link = json_dict['webpage_url']
        yt = Video(link)
        subtitle = yt.subtitle
        message = f'''
        <b>{title}\n\n\n</b>
        {link}
        {upload_date}
        <u>Channel: {channel_name}\n\n\n </u>
        {subtitle}'''

        messages = [ message[i:i+4095] for i in range(0, len(message), 4095) ]
        for message in messages:
            tg = Sender(message)
            tg.send_to_tg()
            print(message)
        os.remove(dic)

if __name__ == '__main__':
    main()
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
ain()
").date()
        channel_name = json_dict['channel']
        link = json_dict['webpage_url']
        yt = Video(link)
        subtitle = yt.subtitle
        message = f'''
        <b>{title}\n\n\n</b>
        {link}
        {upload_date}
        <u>Channel: {channel_name}\n\n\n </u>
        {subtitle}'''

        messages = split_story(message)
        for message in messages:
            tg = Sender(message)
            tg.send_to_tg()
            print(message)
        os.remove(dic)

if __name__ == '__main__':
    main()
name__ == '__main__':
>>>>>>> 7a4526e (nothimg)
    main()
