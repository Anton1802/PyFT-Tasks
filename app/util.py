import requests
from decouple import config

def send_message(message: str, chat_id):
    TOKEN_TELEGRAM_BOT = config("TOKEN_TELEGRAM_BOT")
    URL = f'https://api.telegram.org/bot{TOKEN_TELEGRAM_BOT}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
    }
    
    response = requests.post(URL, data=payload, timeout=5)

    return response.json()