import os
import json
import asyncio
import logging
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import MessageMediaWebPage

# .env 로드
load_dotenv(os.path.join(os.path.dirname(__file__), "../../00_Core/.env"))

# 환경 변수 및 설정
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SESSION_STRING = os.getenv("TELEGRAM_SESSION_STRING")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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

def save_checkpoints(checkpoints):
    try:
        with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f:
            json.dump(checkpoints, f, indent=4)
    except Exception as e:
        logger.error(f"체크포인트 저장 실패: {e}")

async def main():
    if not SESSION_STRING:
        logger.error("TELEGRAM_SESSION_STRING 환경 변수가 설정되지 않았습니다.")
        return

    config = load_config()
    if not config: return

    SOURCE_CHANNELS = config.get("source_channels", [])
    DESTINATION = config.get("destination_user_id", "@opendoorai")
    KEYWORDS = config.get("keywords", [])
    
    general_settings = config.get("settings", {})
    FORWARD_MEDIA_DEFAULT = general_settings.get("forward_media", True)

    checkpoints = load_checkpoints()

    user_client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    bot_client = TelegramClient('bot_batch_session', API_ID, API_HASH)

    try:
        await user_client.connect()
        await bot_client.start(bot_token=BOT_TOKEN)
        
        # 15분 주기에 맞춰 20분 전 기준 (안전 마진)
        time_threshold = datetime.now(timezone.utc) - timedelta(minutes=20)
        logger.info(f"{time_threshold} 이후의 새로운 메시지를 확인합니다.")

        for channel_id in SOURCE_CHANNELS:
            try:
                channel_key = str(channel_id)
                
                # 히스토리 수집 완료 여부와 관계없이 실시간 수집은 진행하도록 변경 (또는 체크 생략 가능)
                # if not checkpoints.get(f"{channel_key}_history_completed"): ...

                entity = await user_client.get_entity(channel_id)
                chat_title = getattr(entity, 'title', channel_id)
                last_id = checkpoints.get(channel_key, 0)
                
                # 모든 새로운 메시지를 순차적으로(reverse=True) 가져옴
                async for message in user_client.iter_messages(entity, min_id=last_id, offset_date=time_threshold, reverse=True):
                    msg_text = message.text or ""
                    
                    # 키워드 필터링 (설정된 경우)
                    if KEYWORDS and not any(kw.lower() in msg_text.lower() for kw in KEYWORDS):
                        continue

                    kst = timezone(timedelta(hours=9))
                    original_time = message.date.astimezone(kst).strftime('%Y-%m-%d %H:%M:%S')
                    forward_msg = f"🕒 **[{original_time}]** | 📢 **[{chat_title}]**\n{msg_text}"
                    
                    # 미디어 처리 로직
                    has_media = message.media and not isinstance(message.media, MessageMediaWebPage)
                    
                    # 제외 대상: 동영상(video), 음성(voice), 오디오/음악(audio/music)
                    is_excluded = any([
                        getattr(message, 'video', None),
                        getattr(message, 'voice', None),
                        getattr(message, 'audio', None)
                    ])
                    
                    # 2026년 이후 데이터는 설정에 따라 미디어 포함 (단, 제외 대상은 제외)
                    allow_media_file = FORWARD_MEDIA_DEFAULT and not is_excluded
                    
                    try:
                        if has_media and allow_media_file:
                            # 개별 전송 (미디어 포함)
                            await bot_client.send_message(DESTINATION, forward_msg, file=message.media)
                        else:
                            # 개별 전송 (텍스트만)
                            await bot_client.send_message(DESTINATION, forward_msg)
                        
                        logger.info(f"✅ [{chat_title}] {original_time} 메시지 전달 완료")
                    except Exception as send_err:
                        logger.error(f"❌ 전송 실패: {send_err}")
                    
                    # 체크포인트 즉시 업데이트 및 저장
                    checkpoints[channel_key] = message.id
                    save_checkpoints(checkpoints)
                    
                    # 개별 메시지 사이의 짧은 대기 (Flood 방지 및 하나씩 보이게 처리)
                    await asyncio.sleep(1.5)

            except Exception as e:
                logger.error(f"채널 {channel_id} 처리 중 오류: {e}")

            except Exception as e:
                logger.error(f"채널 {channel_id} 처리 중 오류: {e}")

    finally:
        await user_client.disconnect()
        await bot_client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
