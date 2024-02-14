import os
import json
import random
import asyncio
import aiohttp  # Use aiohttp for async HTTP requests
from datetime import datetime, timedelta
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

bootstrap_servers = os.getenv('BROKER')
topic_name = os.getenv('TOPIC_NAME')
bot_token = os.getenv('BOT_TOKEN')
api_url = os.getenv('API_URL')
chat_id = os.getenv('CHAT_ID')


bot = Bot(token=bot_token)

async def send_message():
    async with aiohttp.ClientSession() as session:
        print("Attempting to send message...")
        payload = {
            "seed_text": "baja ",
            "num_generate": random.randint(4, 35)
        }
        headers = {'Content-Type': 'application/json'}

        async with session.post(api_url, json=payload, headers=headers) as response:
            print(f"API Response Status: {response.status}")
            if response.status == 200:
                message_content = await response.json()

                message_text = message_content.get('generated_text', 'Default message') + "\n\n<i>-The Whisperer Bot ❤️</i>"

                print(f"Message to send: {message_text}")
                telegram_response = await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='HTML')
                print(f"Telegram Response: {telegram_response}")
            else:
                print(f"Failed to get message from API. Status code: {response.status}")

async def schedule_daily_message():
    now = datetime.now()
    start_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=20, minute=0, second=0, microsecond=0)

    # Calculate a random future time between start_time and end_time
    delta_seconds = (end_time - start_time).total_seconds()
    random_future_time = start_time + timedelta(seconds=random.randint(0, int(delta_seconds)))
    print(f"Next message scheduled for {random_future_time.strftime('%Y-%m-%d %H:%M:%S')}")

    while True:
        now = datetime.now()
        if now >= random_future_time:
            await send_message()

            next_day = now + timedelta(days=1)
            start_time = next_day.replace(hour=8, minute=0, second=0, microsecond=0)
            end_time = next_day.replace(hour=20, minute=0, second=0, microsecond=0)

            delta_seconds = (end_time - start_time).total_seconds()
            random_future_time = start_time + timedelta(seconds=random.randint(0, int(delta_seconds)))

            print(f"Next message scheduled for {random_future_time.strftime('%Y-%m-%d %H:%M:%S')}")
        await asyncio.sleep(60)

async def main():
    await schedule_daily_message()

if __name__ == '__main__':
    asyncio.run(main())
