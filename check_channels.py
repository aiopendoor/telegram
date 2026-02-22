import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_STRING = os.getenv("TELEGRAM_SESSION_STRING")

async def check_channels():
    if not SESSION_STRING:
        print("❌ TELEGRAM_SESSION_STRING is missing in .env")
        return

    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    try:
        await client.connect()
        
        if not await client.is_user_authorized():
            print("❌ Client is not authorized. Please run extract_session.py again.")
            return
            
        me = await client.get_me()
        print(f"✅ Authenticated as: {me.first_name} (@{me.username})")
        
        channels = [
            "gaoshoukorea", "corevalue", "hanachina", "songjongsik", 
            "jake8lee", "HS_academy", "bumgore", "helpmeonestep", 
            "TNBfolio", "Barbarianglobal", "siglab", "stockgrandmaster", 
            "eqmirae"
        ]
        
        for channel in channels:
            try:
                entity = await client.get_entity(channel)
                print(f"✅ Found channel: {channel} - {entity.title}")
            except Exception as e:
                print(f"❌ Failed to find channel: {channel} - {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(check_channels())
