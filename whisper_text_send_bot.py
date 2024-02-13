import os
import json
import schedule
import time
import random
import requests
from datetime import datetime, timedelta
from telegram import Bot
from dotenv import load_dotenv
import asyncio


load_dotenv()

bootstrap_servers = [os.getenv('BROKER')]
topic_name = os.getenv('TOPIC_NAME')
bot_token = os.getenv('BOT_TOKEN')
api_url = os.getenv('API_URL')
chat_id = os.getenv('CHAT_ID')

bot = Bot(token=bot_token)

async def send_message():
    print("Attempting to send message...")
    payload = {
        "seed_text": "baja master boi",
        "num_generate": random.randint(4, 35)
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(api_url, json=payload, headers=headers)
    print(f"API Response Status: {response.status_code}")
    if response.status_code == 200:
        message_content = response.json()

        message_text = message_content.get('generated_text', 'Default message') + "\n\n<i>-The Whisperer Bot ❤️</i>"

        print(f"Message to send: {message_text}")
        telegram_response = await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='HTML')
        print(f"Telegram Response: {telegram_response}")
    else:
        print(f"Failed to get message from API. Status code: {response.status_code}")


def schedule_daily_message():
    # Schedule the message to be sent at a random time between 8 AM and 8 PM
    now = datetime.now()
    start_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=20, minute=0, second=0, microsecond=0)

    random_time = start_time + timedelta(seconds=random.randint(0, int((end_time - start_time).total_seconds())))
    schedule_time = random_time.strftime("%H:%M")

    schedule.every().day.at(schedule_time).do(send_message)
    print(f"Message scheduled for {schedule_time}")

if __name__ == '__main__':
    # Schedule the message sending function
    schedule_daily_message()
    
    # Run the scheduler in an async loop
    loop = asyncio.get_event_loop()

    # loop.run_until_complete(send_message())

    while True:
        schedule.run_pending()
        time.sleep(1)
