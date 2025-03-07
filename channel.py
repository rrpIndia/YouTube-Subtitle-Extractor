from sys import exit
import requests
import re

class ChannelFile:
    def __init__(self, channel_file):
        self.channel_file = channel_file

    def input(self):
        inp = str(input('please give channel url: '))
        return inp

    def is_valid_yt_channel(self, url):
        self.url = url
        # Regular expression to match YouTube channel URLs
        pattern = r'^https?:\/\/(?:m\.)?(?:www\.)?youtube\.com\/(?:channel|c)\/([a-zA-Z0-9_-]+)(?:\/|\/videos\/)?$'
        
        # Check if the URL matches the pattern
        if re.match(pattern,self.url):
            try:
                # Send a GET request to the URL
                response = requests.get(self.url)
                
                # If the response status code is 200, it's a valid URL
                if response.status_code == 200:
                    return True
                else:
                    return False
            except requests.exceptions.RequestException as e:
                print(e)
                
        else:
            return False
    
    def make_file(self, channel):
        self.channel = channel
        with open(self.channel_file, 'a') as f:
            f.write(f'{self.channel}\n')


if __name__ == '__main__':
    cf = ChannelFile('test_file.txt')
    ui = cf.input()
    if cf.is_valid_yt_channel(ui):
        cf.make_file(ui)
        print(ui)
    else:
        print('invalid')
