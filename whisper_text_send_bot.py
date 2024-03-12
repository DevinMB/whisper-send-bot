import os
import asyncio
import aiohttp
from datetime import datetime, timedelta
from telegram import Bot
import random


# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Environment variables
bot_token = os.getenv('BOT_TOKEN')
api_url = os.getenv('API_URL')
chat_id = os.getenv('CHAT_ID')
week_schedule = os.getenv('WEEK_SCHEDULE', '')  # Expected format: "1,3,5" for Mon, Wed, Fri
seed_text = os.getenv('SEED_TEXT')

# Initialize bot
bot = Bot(token=bot_token)

async def send_message():
    async with aiohttp.ClientSession() as session:
        print("Attempting to send message...")
        payload = {
            "seed_text": seed_text,
            "num_generate": random.randint(4, 35)
        }
        headers = {'Content-Type': 'application/json'}

        async with session.post(api_url, json=payload, headers=headers) as response:
            print(f"API Response Status: {response.status}")
            if response.status == 200:
                message_content = await response.json()

                message_text = message_content.get('generated_text', 'Default message') + "\n\n<i>-The Whisperer Bot ❤️ v1</i>"

                print(f"Message to send: {message_text}")
                telegram_response = await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='HTML')
                print(f"Telegram Response: {telegram_response}")
            else:
                print(f"Failed to get message from API. Status code: {response.status}")

async def schedule_message(active_days):
    while True:
        now = datetime.now()

        if now.weekday() in active_days:
            print(f"Day {now.weekday()} is in list of week days {active_days}")

            # Calculate a random hour between 8 AM (inclusive) and 8 PM (exclusive)
            random_hour = random.randint(8, 19)  # 19 is inclusive in randint, so this goes up to 7:59 PM
            print(f"Random Hour Is {random_hour}")
            # Calculate today's date with the random hour
            scheduled_time = now.replace(hour=random_hour, minute=0, second=0, microsecond=0)

            if now <= scheduled_time < now.replace(hour=20, minute=0, second=0, microsecond=0):
                # Wait until the scheduled time if it hasn't passed yet
                sleep_seconds = (scheduled_time - now).total_seconds()
                await asyncio.sleep(sleep_seconds)
                await send_message()

            # After sending a message or if the random time for today has passed, wait until the next day
            next_day = now + timedelta(days=1)
            next_day_start = next_day.replace(hour=0, minute=0, second=0, microsecond=0)  # Midnight, start of the next day
            await asyncio.sleep((next_day_start - now).total_seconds())

        else:
            # If today is not an active day, wait until the next day to check again
            next_day = now + timedelta(days=1)
            next_day_start = next_day.replace(hour=0, minute=0, second=0, microsecond=0)  # Midnight, start of the next day
            print("Will check again next day: {next_day}")
            await asyncio.sleep((next_day_start - now).total_seconds())


async def main():
    active_days = [int(day) for day in week_schedule.split(',') if day.isdigit()]
    await schedule_message(active_days)

if __name__ == '__main__':
    asyncio.run(main())
