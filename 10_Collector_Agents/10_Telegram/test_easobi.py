import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()

async def test():
    api_id = int(os.getenv("TELEGRAM_API_ID"))
    api_hash = os.getenv("TELEGRAM_API_HASH")
    session = os.getenv("TELEGRAM_SESSION_STRING")
    
    client = TelegramClient(StringSession(session), api_id, api_hash)
    await client.connect()
    try:
        print("Testing easobi...")
        entity = await client.get_entity('easobi')
        print(f"Found: {entity.title}")
        it = client.iter_messages(entity, reverse=True)
        msg = await it.__anext__()
        print(f"First message: {msg.date}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.disconnect()

asyncio.run(test())
