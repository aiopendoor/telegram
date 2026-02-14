import os
import json
import asyncio
import logging
from datetime import datetime, timezone
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

    # StringSession을 사용하여 로그인 유지
    user_client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    bot_client = TelegramClient('bot_history_session', API_ID, API_HASH)

    try:
        await user_client.connect()
        await bot_client.start(bot_token=BOT_TOKEN)
        
        logger.info("과거 전체 메시지 수집을 시작합니다.")

        for channel_id in SOURCE_CHANNELS:
            try:
                entity = await user_client.get_entity(channel_id)
                chat_title = getattr(entity, 'title', channel_id)
                logger.info(f"채널 분석 중: {chat_title}")
                
                # 역순(오래된 것부터)으로 모든 메시지 가져오기
                count = 0
                async for message in user_client.iter_messages(entity, reverse=True):
                    msg_text = message.text or ""
                    if not msg_text and not message.media: continue
                    
                    # 메시지 전송
                    forward_msg = f"📢 **[{chat_title}]** (History)\n\n{msg_text}"
                    
                    try:
                        if message.media:
                            # 미디어가 있는 경우 다운로드 없이 바로 전달 시도 (봇 권한 필요)
                            await bot_client.send_message(DESTINATION, forward_msg, file=message.media)
                        else:
                            await bot_client.send_message(DESTINATION, forward_msg)
                        
                        count += 1
                        if count % 10 == 0:
                            logger.info(f"{count}개 메시지 전달 완료...")
                        
                        # 도배 방지를 위한 딜레이 (과거 데이터는 양이 많으므로 0.5초)
                        await asyncio.sleep(0.5)
                        
                    except Exception as send_error:
                        logger.error(f"메시지 전송 오류: {send_error}")
                        await asyncio.sleep(5) # 에러 발생 시 잠시 대기

                logger.info(f"채널 {chat_title}의 모든 메시지({count}개) 전달이 완료되었습니다.")

            except Exception as e:
                logger.error(f"채널 {channel_id} 처리 중 오류: {e}")

    finally:
        await user_client.disconnect()
        await bot_client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
