import os
import json
import asyncio
import logging
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

# .env 로드
load_dotenv()

# 환경 변수 및 설정
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SESSION_STRING = os.getenv("TELEGRAM_SESSION_STRING")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    try:
        with open('channels.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("channels.json 파일을 찾을 수 없습니다.")
        return None

async def main():
    if not SESSION_STRING:
        logger.error("TELEGRAM_SESSION_STRING 환경 변수가 설정되지 않았습니다.")
        return

    config = load_config()
    if not config: return

    SOURCE_CHANNELS = config.get("source_channels", [])
    DESTINATION = config.get("destination_user_id", "@opendoorai")
    KEYWORDS = config.get("keywords", [])

    # StringSession을 사용하여 로그인 유지
    user_client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    bot_client = TelegramClient('bot_batch_session', API_ID, API_HASH)

    try:
        await user_client.connect()
        await bot_client.start(bot_token=BOT_TOKEN)
        
        # 1시간 5분 전 기준 (안전 마진)
        time_threshold = datetime.now(timezone.utc) - timedelta(hours=1, minutes=5)
        logger.info(f"{time_threshold} 이후의 메시지를 수집합니다. (원본 시간 포함)")

        for channel_id in SOURCE_CHANNELS:
            try:
                entity = await user_client.get_entity(channel_id)
                chat_title = getattr(entity, 'title', channel_id)
                
                async for message in user_client.iter_messages(entity, limit=50, offset_date=time_threshold, reverse=True):
                    if message.date < time_threshold:
                        continue
                        
                    msg_text = message.text or ""
                    if KEYWORDS and not any(kw.lower() in msg_text.lower() for kw in KEYWORDS):
                        continue

                    # KST 변환 및 시간 포맷
                    kst = timezone(timedelta(hours=9))
                    original_time = message.date.astimezone(kst).strftime('%Y-%m-%d %H:%M:%S')
                    
                    forward_msg = f"🕒 **[원본 시간: {original_time}]**\n📢 **[{chat_title}]**\n\n{msg_text}"
                    
                    if message.media:
                        await bot_client.send_message(DESTINATION, forward_msg, file=message.media)
                    else:
                        await bot_client.send_message(DESTINATION, forward_msg)
                    
                    logger.info(f"[{chat_title}] {original_time} 메시지 전달 완료")
                    await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"채널 {channel_id} 처리 중 오류: {e}")

    finally:
        await user_client.disconnect()
        await bot_client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
