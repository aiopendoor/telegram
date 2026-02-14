import os
import json
import asyncio
import logging
import base64
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# .env 로드
load_dotenv()

# 환경 변수 및 설정
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# GitHub Secret으로 등록될 세션 문자열
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
    KEYWORDS = config.get("keywords", [])
    DESTINATION = config.get("destination_user_id", "me")

    # StringSession을 사용하여 로그인 유지
    user_client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    bot_client = TelegramClient('bot_batch_session', API_ID, API_HASH)

    try:
        await user_client.connect()
        await bot_client.start(bot_token=BOT_TOKEN)
        
        # 1시간 전 기준 시간 설정
        time_threshold = datetime.now(timezone.utc) - timedelta(hours=1)
        logger.info(f"{time_threshold} 이후의 메시지를 수집합니다.")

        for channel_id in SOURCE_CHANNELS:
            try:
                entity = await user_client.get_entity(channel_id)
                logger.info(f"채널 분석 중: {getattr(entity, 'title', channel_id)}")
                
                # 메시지 가져오기
                async for message in user_client.iter_messages(entity, limit=20, offset_date=time_threshold, reverse=True):
                    if message.date < time_threshold:
                        continue
                        
                    msg_text = message.text or ""
                    
                    # 키워드 필터링
                    if KEYWORDS and not any(kw.lower() in msg_text.lower() for kw in KEYWORDS):
                        continue

                    # 메시지 전송
                    chat_title = getattr(entity, 'title', '알 수 없는 채널')
                    forward_msg = f"📢 **[{chat_title}]** (Batch)\n\n{msg_text}"
                    await bot_client.send_message(DESTINATION, forward_msg)
                    logger.info(f"메시지 전달 완료: {msg_text[:20]}...")
                    
                    # API 제한 방지
                    await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"채널 {channel_id} 처리 중 오류: {e}")

    finally:
        await user_client.disconnect()
        await bot_client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
