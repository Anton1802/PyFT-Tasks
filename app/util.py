from decouple import config
from telebot import TeleBot

def send_message(message: str, chat_id):
    TOKEN_TELEGRAM_BOT = config("TOKEN_TELEGRAM_BOT")
    bot = TeleBot(token=TOKEN_TELEGRAM_BOT)
    bot.send_message(chat_id, message, parse_mode='Markdown')