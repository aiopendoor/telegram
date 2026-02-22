import os
import json
import asyncio
import logging
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import MessageMediaWebPage

# .env 파일 로드
load_dotenv()

# 환경 변수 설정
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SESSION_STRING = os.getenv("TELEGRAM_SESSION_STRING")

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CHECKPOINT_FILE = 'last_processed_ids.json'

def load_config():
    try:
        with open('channels.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("channels.json 파일을 찾을 수 없습니다.")
        return None

def load_checkpoints():
    try:
        if os.path.exists(CHECKPOINT_FILE):
            with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content: return {}
                return json.loads(content)
    except Exception as e:
        logger.error(f"체크포인트 로드 실패: {e}")
    return {}

config = load_config()
if not config:
    exit(1)

SOURCE_CHANNELS = config.get("source_channels", [])
KEYWORDS = config.get("keywords", [])

# Telegram Client 설정 (User 계정용)
if SESSION_STRING:
    user_client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
else:
    user_client = TelegramClient('user_session', API_ID, API_HASH)

# Telegram Client 설정 (Bot용 - 메시지 전송 전담)
bot_client = TelegramClient('bot_session', API_ID, API_HASH)

async def main():
    # 클라이언트 시작
    await user_client.start()
    await bot_client.start(bot_token=BOT_TOKEN)
    
    logger.info("텔레그램 실시간 리스너가 시작되었습니다.")

    @user_client.on(events.NewMessage(chats=SOURCE_CHANNELS))
    async def forwarder_handler(event):
        try:
            # 설정 및 체크포인트 최신화
            current_config = load_config()
            checkpoints = load_checkpoints()
            
            chat = await event.get_chat()
            chat_title = getattr(chat, 'title', '알 수 없는 채널')
            channel_id = str(event.chat_id)
            # chat_id가 숫자인 경우(예: -100...) handle 문자열과 비교를 위해 변환 필요할 수 있음
            # Telethon의 chats=SOURCE_CHANNELS는 username이나 id 모두 지원하므로 호환성 유지
            
            # [의존성 체크] 히스토리 완료 여부 확인
            # username으로 설정된 경우를 위해 username과 id 모두 체크 루프 필요할 수 있음
            is_completed = False
            for key in checkpoints:
                if key.endswith("_history_completed"):
                    cid_part = key.replace("_history_completed", "")
                    # source_channels에 포함된 값(ID 또는 Username) 중 하나라도 일치하면 체크
                    if cid_part in str(event.chat_id) or (getattr(chat, 'username', '') and cid_part == chat.username):
                         if checkpoints.get(key):
                             is_completed = True
                             break
            
            if not is_completed:
                logger.info(f"[{chat_title}] 히스토리가 아직 수집 중이므로 실시간 전달을 제외합니다.")
                return

            message_text = event.raw_text
            if KEYWORDS and not any(kw.lower() in message_text.lower() for kw in KEYWORDS):
                return

            destination = current_config.get("destination_user_id", "me")
            forward_msg = f"📢 **[{chat_title}]**\n\n{message_text}"
            
            # 미디어 설정
            general_settings = current_config.get("settings", {})
            forward_media_default = general_settings.get("forward_media", True)
            
            has_file = event.message.media and not isinstance(event.message.media, MessageMediaWebPage)
            allow_media = (event.message.date.year >= 2026) or forward_media_default
            
            if has_file and allow_media:
                await bot_client.send_message(destination, forward_msg, file=event.message.media)
            else:
                await bot_client.send_message(destination, forward_msg)
                
            logger.info(f"봇을 통해 '{destination}'로 실시간 전달 완료.")

        except Exception as e:
            logger.error(f"메시지 전달 중 오류 발생: {e}")

    # 연결 유지
    await user_client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("스크립트가 사용자에 의해 종료되었습니다.")
