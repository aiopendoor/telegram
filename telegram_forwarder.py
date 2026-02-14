import os
import json
import asyncio
import logging
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import User

# .env 파일 로드
load_dotenv()

# 환경 변수 설정
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 설정 파일 로드
def load_config():
    try:
        with open('channels.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("channels.json 파일을 찾을 수 없습니다.")
        return None

config = load_config()
if not config:
    exit(1)

SOURCE_CHANNELS = config.get("source_channels", [])
KEYWORDS = config.get("keywords", [])

# Telegram Client 설정 (User 계정용)
user_client = TelegramClient('user_session', API_ID, API_HASH)

# Telegram Client 설정 (Bot용 - 메시지 전송 전담)
bot_client = TelegramClient('bot_session', API_ID, API_HASH)

async def main():
    # 클라이언트 시작
    await user_client.start()
    await bot_client.start(bot_token=BOT_TOKEN)
    
    logger.info("텔레그램 전달 스크립트가 시작되었습니다.")
    print("--------------------------------------------------")
    print("실시간 메시지 리스너가 작동 중입니다...")
    print("메시지가 올라오면 자동으로 @opendoorai 봇이 전달합니다.")
    print("--------------------------------------------------")

    @user_client.on(events.NewMessage(chats=SOURCE_CHANNELS))
    async def forwarder_handler(event):
        try:
            # 보낸 채팅방(채널) 정보 가져오기
            chat = await event.get_chat()
            chat_title = getattr(chat, 'title', '알 수 없는 채널')
            
            # 메시지 텍스트
            message_text = event.raw_text
            
            # 키워드 필터링 (키워드가 설정된 경우에만)
            if KEYWORDS:
                if not any(kw.lower() in message_text.lower() for kw in KEYWORDS):
                    return

            logger.info(f"[{chat_title}] 메시지 감지: {message_text[:30]}...")

            # 봇을 통해 나에게 전달
            destination = config.get("destination_user_id", "me")
            
            # 메시지 형식 구성
            forward_msg = f"📢 **[{chat_title}]**\n\n{message_text}"
            
            # 봇으로 메시지 전송
            await bot_client.send_message(destination, forward_msg)
            logger.info(f"봇을 통해 '{destination}'로 전달 완료.")

        except Exception as e:
            logger.error(f"메시지 전달 중 오류 발생: {e}")

    # 연결 유지
    await user_client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("스크립트가 사용자에 의해 종료되었습니다.")
