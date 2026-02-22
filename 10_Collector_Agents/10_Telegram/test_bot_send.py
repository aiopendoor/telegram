import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

async def test_bot():
    api_id = int(os.getenv("TELEGRAM_API_ID"))
    api_hash = os.getenv("TELEGRAM_API_HASH")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    client = TelegramClient('test_bot_session', api_id, api_hash)
    await client.start(bot_token=bot_token)
    
    try:
        dest = "@opendoorai"
        print(f"Sending test message to {dest}...")
        await client.send_message(dest, "🤖 항중력 프로젝트: 메시지 연결 테스트입니다.")
        print("✅ 전송 성공!")
    except Exception as e:
        print(f"❌ 전송 실패: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(test_bot())
