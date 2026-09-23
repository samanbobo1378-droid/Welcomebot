import os
from flask import Flask
from threading import Thread
import telebot
import time
import requests

TOKEN = '8628828031:AAFK0mSv7Sp2caHb9dmM02N3ITTqIfqVu5g'
bot = telebot.TeleBot(TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Bot is active and running!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

def self_ping():
    time.sleep(10)
    app_url = os.environ.get('RENDER_EXTERNAL_URL')
    if app_url:
        while True:
            try:
                requests.get(app_url)
            except:
                pass
            time.sleep(300)

# پاکسازی متن
def clean_text(text):
    if not text:
        return ""
    return text.strip().strip('،!؟.,؛»«()[]{}')

# بررسی اینکه آیا فرستنده ادمین است یا خیر
def is_admin(message):
    try:
        if message.chat.type in ['group', 'supergroup']:
            member = bot.get_chat_member(message.chat.id, message.from_user.id)
            if member.status in ['administrator', 'creator']:
                return True
        return False
    except:
        return False

# ۱. پاسخ به سلام (فقط کاربران عادی و فقط وقتی پیام خودشون هست، نه وقتی ادمین‌ها دارن جواب می‌دن یا ریپلی می‌کنن)
@bot.message_handler(func=lambda message: message.text and not is_admin(message) and message.reply_to_message is None and clean_text(message.text) == 'سلام')
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام، خوبین ؟\nبه مشهد استار خوش اومدی 💫\nامیدوارم حال دلت خوب باشه 💞", reply_to_message_id=message.message_id)

# ۲. پاسخ به خداحافظ (فقط کاربران عادی و پیام مستقل)
@bot.message_handler(func=lambda message: message.text and not is_admin(message) and message.reply_to_message is None and clean_text(message.text) in ['خداحافظ', 'خدافظ', 'بای'])
def send_goodbye(message):
    bot.send_message(message.chat.id, "چه زود داری میری 🥺", reply_to_message_id=message.message_id)

# ۳. پاسخ به لفت (فقط کاربران عادی و پیام مستقل)
@bot.message_handler(func=lambda message: message.text and not is_admin(message) and message.reply_to_message is None and clean_text(message.text) in ['لف', 'لفت'])
def send_left(message):
    bot.send_message(message.chat.id, "خیلی بدی کجا میری منو تنها میزاری؟ 💔", reply_to_message_id=message.message_id)

if name == 'main':
    keep_alive()
    t_ping = Thread(target=self_ping)
    t_ping.start()
    
    bot.infinity_polling()
