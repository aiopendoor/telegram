import os
import asyncio
import json
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

# .env 로드
load_dotenv(os.path.join(os.path.dirname(__file__), "../../00_Core/.env"))

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_STRING = os.getenv("TELEGRAM_SESSION_STRING")

async def get_first_message_dates():
    if not SESSION_STRING:
        print("Error: TELEGRAM_SESSION_STRING is missing")
        return

    channels_config = {}
    if os.path.exists('channels.json'):
        with open('channels.json', 'r', encoding='utf-8') as f:
            channels_config = json.load(f)
    
    source_channels = channels_config.get("source_channels", [])
    if not source_channels:
        print("No channels found in channels.json")
        return

    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("Error: Client not authorized. Please check your session string.")
        await client.disconnect()
        return

    print(f"\n{'Channel':<40} | {'First Message Date (KST)':<25}")
    print("-" * 70)

    kst = timezone(timedelta(hours=9))

    for channel in source_channels:
        try:
            entity = await client.get_entity(channel)
            chat_title = getattr(entity, 'title', channel)
            
            # reverse=True로 하면 가장 오래된 메시지부터 가져옵니다 (ID가 낮은 순)
            # 하지만 텔레그램 API 특성상 ID 1 또는 첫 번째 메시지를 바로 가져오려면 
            # limit=1과 reverse=True를 조합하거나, 가장 큰 offset_id를 0으로 주고 reverse=True를 합니다.
            # Telethon의 iter_messages(reverse=True)는 ID 순으로 정렬하여 가져오므로 
            # 첫 번째 메시지는 가장 처음에 나오는 메시지입니다.
            async for message in client.iter_messages(entity, limit=1, reverse=True):
                first_date = message.date.astimezone(kst).strftime('%Y-%m-%d %H:%M:%S')
                print(f"{chat_title:<40} | {first_date:<25}")
                break
        except Exception as e:
            print(f"{str(channel):<40} | Error: {e}")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(get_first_message_dates())
