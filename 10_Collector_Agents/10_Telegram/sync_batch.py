import os
import json
import asyncio
import logging
import heapq
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
# 역할별 전용 세션 우선 적용 (없으면 기존 세션 사용)
SESSION_STRING = os.getenv("TELEGRAM_SESSION_REALTIME") or os.getenv("TELEGRAM_SESSION_STRING")

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
    FORWARD_MEDIA_DEFAULT = general_settings.get("batch_forward_media", True)

    checkpoints = load_checkpoints()

    user_client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    bot_client = TelegramClient('bot_batch_session', API_ID, API_HASH)

    try:
        await user_client.connect()
        await bot_client.start(bot_token=BOT_TOKEN)
        
        # 2026-02-22 00:00:00 KST (UTC+9) 기준 시간
        start_of_day = datetime(2026, 2, 22, tzinfo=timezone(timedelta(hours=9)))
        # GitHub Actions 중단 시간을 고려하여 24시간 전까지 확인 (체크포인트가 없을 경우 대비)
        # 하지만 min_id(last_id)가 있다면 Telethon은 min_id 이후의 모든 메시지를 가져옴
        time_threshold = max(datetime.now(timezone.utc) - timedelta(hours=24), start_of_day.astimezone(timezone.utc))
        logger.info(f"🕒 {time_threshold} (KST) 이후의 새로운 메시지를 타임라인 병합 방식으로 확인합니다.")

        # 타임라인 병합을 위한 우선순위 큐(Heap)
        heap = []
        iterators = {}

        # 1. 각 채널별 초기 데이터 확보
        for channel_id in SOURCE_CHANNELS:
            try:
                channel_key = str(channel_id)
                entity = await user_client.get_entity(channel_id)
                chat_title = getattr(entity, 'title', channel_id)
                last_id = checkpoints.get(channel_key, 0)
                
                # 새로운 메시지 이터레이터 생성 (가장 과거부터: reverse=True)
                it = user_client.iter_messages(entity, min_id=last_id, offset_date=time_threshold, reverse=True)
                iterators[channel_key] = (it, chat_title)
                
                # 첫 번째 메시지 로드하여 힙에 삽입
                try:
                    msg = await it.__anext__()
                    heapq.heappush(heap, (msg.date, channel_key, msg))
                except StopAsyncIteration:
                    continue
            except Exception as e:
                logger.error(f"채널 {channel_id} 초기화 중 오류: {e}")

        # 2. 힙에서 가장 과거 메시지부터 꺼내어 순차 처리
        while heap:
            msg_date, channel_key, message = heapq.heappop(heap)
            it, chat_title = iterators[channel_key]
            
            # 메시지 필터링 및 가공
            msg_text = message.text or ""
            if KEYWORDS and not any(kw.lower() in msg_text.lower() for kw in KEYWORDS):
                pass # 키워드 미일치 시 전송만 건너뜀
            else:
                kst = timezone(timedelta(hours=9))
                original_time = message.date.astimezone(kst).strftime('%Y-%m-%d %H:%M:%S')
                forward_msg = f"🕒 **[{original_time}]** | 📢 **[{chat_title}]**\n{msg_text}"
                
                # 미디어 처리
                has_media = message.media and not isinstance(message.media, MessageMediaWebPage)
                is_excluded = any([
                    getattr(message, 'video', None),
                    getattr(message, 'voice', None),
                    getattr(message, 'audio', None)
                ])
                allow_media_file = FORWARD_MEDIA_DEFAULT and not is_excluded
                
                try:
                    if has_media and allow_media_file:
                        await bot_client.send_message(DESTINATION, forward_msg, file=message.media)
                    else:
                        await bot_client.send_message(DESTINATION, forward_msg)
                    logger.info(f"✅ [{chat_title}] {original_time} 메시지 전달 완료")
                except Exception as send_err:
                    logger.error(f"❌ 전송 실패 ({chat_title}): {send_err}")

            # 체크포인트 업데이트 및 저장
            checkpoints[channel_key] = message.id
            save_checkpoints(checkpoints)
            
            # 해당 채널의 다음 메시지를 가져와 힙에 보충
            try:
                next_msg = await it.__anext__()
                heapq.heappush(heap, (next_msg.date, channel_key, next_msg))
            except StopAsyncIteration:
                pass
            
            # Flood 방지 및 자연스러운 메시지 흐름을 위한 대기
            await asyncio.sleep(1.5)

    finally:
        await user_client.disconnect()
        await bot_client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
