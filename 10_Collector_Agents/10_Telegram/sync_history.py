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
from telethon.errors import FloodWaitError

# .env 로드
load_dotenv(os.path.join(os.path.dirname(__file__), "../../00_Core/.env"))

# 환경 변수 및 설정
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# 역할별 전용 세션 우선 적용 (없으면 기존 세션 사용)
SESSION_STRING = os.getenv("TELEGRAM_SESSION_HISTORY") or os.getenv("TELEGRAM_SESSION_STRING")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CHECKPOINT_FILE = 'last_processed_ids.json'

def load_config():
    try:
        if os.path.exists('channels.json'):
            with open('channels.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"channels.json 로드 실패: {e}")
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
        pass

async def send_split_message(bot_client, destination, text, **kwargs):
    """텔레그램 메시지 길이 제한(4096)을 고려하여 분할 전송"""
    if len(text) <= 4000:
        await bot_client.send_message(destination, text, parse_mode=None, **kwargs)
        return

    parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
    file_handled = False
    for part in parts:
        # 파일은 첫 번째 파트와 함께 전송
        if "file" in kwargs and not file_handled:
            await bot_client.send_message(destination, part, parse_mode=None, **kwargs)
            file_handled = True
        else:
            # 파일 없이 텍스트만 전송
            temp_kwargs = kwargs.copy()
            if "file" in temp_kwargs: del temp_kwargs["file"]
            await bot_client.send_message(destination, part, parse_mode=None, **temp_kwargs)
        await asyncio.sleep(0.5)

async def process_message_for_bundle(message, chat_title, keywords, forward_media=False):
    """번들링을 위해 메시지를 가공하고 필터링 (전송은 하지 않음)"""
    msg_text = (message.text or "").strip()
    has_actual_file = message.media and not isinstance(message.media, MessageMediaWebPage)
    allow_media = forward_media  # 히스토리는 예외 없이 설정에 따름 (보통 False)

    # 미디어만 있고 텍스트가 없는데 미디어 전송이 비활성화된 경우 정보만 표시
    if not msg_text and has_actual_file and not allow_media:
        return None, "SKIP_MEDIA"

    if not msg_text and not message.media:
        return None, "SKIP_EMPTY"
    
    if keywords and not any(kw.lower() in msg_text.lower() for kw in keywords):
        return None, "SKIP_KEYWORD"

    kst = timezone(timedelta(hours=9))
    original_time = message.date.astimezone(kst).strftime('%Y-%m-%d %H:%M:%S')
    
    # 번들용 포맷 (가독성을 위한 구분 포함)
    formatted = f"🕒 **[{original_time}]** | 📢 **[{chat_title}]**\n{msg_text}\n"
    return formatted, "OK"

async def main():
    if not SESSION_STRING:
        logger.error("TELEGRAM_SESSION_STRING is missing")
        return

    config = load_config()
    if not config: return

    SOURCE_CHANNELS = config.get("source_channels", [])
    DESTINATION = config.get("destination_user_id", "@opendoorai")
    KEYWORDS = config.get("keywords", [])
    history_settings = config.get("history_settings", {})
    START_DATE_STR = history_settings.get("start_date")
    END_DATE_STR = history_settings.get("end_date")
    BATCH_SIZE = history_settings.get("batch_size_per_channel", 50)
    EXCLUDE_YEARS = history_settings.get("exclude_years", [])
    GENERAL_SETTINGS = config.get("settings", {})
    FORWARD_MEDIA = GENERAL_SETTINGS.get("history_forward_media", False)

    start_date = None
    if START_DATE_STR:
        start_date = datetime.strptime(START_DATE_STR, "%Y-%m-%d").replace(tzinfo=timezone.utc)

    end_date = None
    if END_DATE_STR:
        end_date = datetime.strptime(END_DATE_STR, "%Y-%m-%d").replace(tzinfo=timezone.utc).replace(hour=23, minute=59, second=59)

    checkpoints = load_checkpoints()
    user_client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    bot_client = TelegramClient('bot_history_session', API_ID, API_HASH)

    try:
        await user_client.connect()
        await bot_client.start(bot_token=BOT_TOKEN)
        
        logger.info(f"📅 전역 타임라인 정렬 수집 시작 (2025년까지)")

        # Priority Queue (Min-Heap)을 위한 데이터 구조
        # (date, channel_id, message_object, chat_title)
        heap = []
        channel_iterators = {}

        # 각 채널별로 첫 번째 메시지 뭉치 가져오기
        for cid in SOURCE_CHANNELS:
            channel_key = str(cid)
            if checkpoints.get(f"{channel_key}_history_completed"):
                continue
            
            try:
                logger.info(f"🔍 [{cid}] 정보 가져오는 중...")
                entity = await user_client.get_entity(cid)
                chat_title = getattr(entity, 'title', cid)
                last_id = checkpoints.get(channel_key, 0)
                
                logger.info(f"📑 [{chat_title}] 메시지 이터레이터 생성 (last_id: {last_id})")
                it_kwargs = {"min_id": last_id, "reverse": True}
                if last_id == 0 and start_date:
                    it_kwargs["offset_date"] = start_date
                
                it = user_client.iter_messages(entity, **it_kwargs)
                channel_iterators[channel_key] = (it, chat_title)
                
                logger.info(f"📥 [{chat_title}] 첫 메시지 로드 시도...")
                msg = await it.__anext__()
                heapq.heappush(heap, (msg.date, channel_key, msg))
                logger.info(f"✅ [{chat_title}] 초기화 완료 (날짜: {msg.date})")
            except StopAsyncIteration:
                logger.info(f"[{cid}] 메시지가 아예 없습니다.")
            except Exception as e:
                logger.error(f"[{cid}] 초기화 중 오류: {e}")

        # 힙을 사용한 시간 순 병합 수집
        bundle_buffer = []
        bundle_checkpoints = {}
        BUNDLE_SIZE = 20
        SEPARATOR = "\n" + "━" * 20 + "\n"

        while heap:
            # 1. 가장 과거의 메시지 추출
            msg_date, channel_key, message = heapq.heappop(heap)
            it, chat_title = channel_iterators[channel_key]

            # 2. 종료 조건 및 필터링 확인
            if start_date and message.date < start_date:
                checkpoints[channel_key] = message.id
            elif end_date and message.date > end_date:
                logger.info(f"[{chat_title}] 종료 날짜 도달 ({message.date} > {end_date}). 완료 처리.")
                checkpoints[f"{channel_key}_history_completed"] = True
            else:
                # 3. 메시지 가공 및 번들링
                formatted_part, status = await process_message_for_bundle(message, chat_title, KEYWORDS, FORWARD_MEDIA)
                
                if formatted_part:
                    bundle_buffer.append(formatted_part)
                    bundle_checkpoints[channel_key] = message.id
                else:
                    # 건너뛴 메시지들에 대한 체크포인트 즉시 업데이트
                    if status != "OK":
                        if status == "SKIP_MEDIA":
                             logger.info(f"⚪️ [{chat_title}] 미디어 전용 메시지 건너뜀 (ID: {message.id})")
                        elif status == "SKIP_EMPTY":
                             logger.info(f"⚪️ [{chat_title}] 빈 메시지 건너뜀 (ID: {message.id})")
                        checkpoints[channel_key] = message.id

                # 번들 전송 조건 충족 시
                if len(bundle_buffer) >= BUNDLE_SIZE:
                    combined_text = SEPARATOR.join(bundle_buffer)
                    try:
                        logger.info(f"📤 {BUNDLE_SIZE}개 메시지 번들 전송 중...")
                        await send_split_message(bot_client, DESTINATION, combined_text)
                        # 전송 성공 후 체크포인트 일괄 업데이트
                        checkpoints.update(bundle_checkpoints)
                        bundle_buffer = []
                        bundle_checkpoints = {}
                    except FloodWaitError as e:
                        logger.warning(f"FloodWait: {e.seconds}초 대기 필요.")
                        # 현재 메시지를 다시 힙에 넣고 대기 (번들은 유지)
                        heapq.heappush(heap, (msg_date, channel_key, message))
                        await asyncio.sleep(e.seconds)
                        continue
                    except Exception as e:
                        logger.error(f"❌ 번들 전송 중 오류 발생: {e}")
                        # 실패 시에도 진행을 위해 번들은 비움 (데이터 유실 방지를 위해 개별 전송 로직이 있으면 좋으나 일단 단순화)
                        bundle_buffer = []
                        bundle_checkpoints = {}

            # 4. 해당 채널의 다음 메시지를 가져와 힙에 보충
            if not checkpoints.get(f"{channel_key}_history_completed"):
                try:
                    next_msg = await it.__anext__()
                    heapq.heappush(heap, (next_msg.date, channel_key, next_msg))
                except StopAsyncIteration:
                    logger.info(f"[{chat_title}] 모든 메시지 수집 완료.")
                    checkpoints[f"{channel_key}_history_completed"] = True
                except Exception as e:
                    logger.error(f"[{chat_title}] 메시지 보충 중 오류: {e}")

            # 주기적으로 체크포인트 저장
            save_checkpoints(checkpoints)

        # 마지막 남은 번들 처리
        if bundle_buffer:
            combined_text = SEPARATOR.join(bundle_buffer)
            try:
                logger.info(f"📤 마지막 남은 {len(bundle_buffer)}개 메시지 번들 전송 중...")
                await send_split_message(bot_client, DESTINATION, combined_text)
                checkpoints.update(bundle_checkpoints)
            except Exception as e:
                logger.error(f"❌ 마지막 번들 전송 오류: {e}")

        logger.info("✅ 모든 채널의 전역 타임라인 병합 수집이 완료되었습니다.")

    finally:
        save_checkpoints(checkpoints)
        await user_client.disconnect()
        await bot_client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
