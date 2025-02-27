import os
import requests
from dotenv import load_dotenv, dotenv_values

load_dotenv()
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
print(send_to_tg('<h1>test</h1>'))
