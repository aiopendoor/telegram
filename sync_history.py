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
                return json.load(f)
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
    
    # 수집 기간 설정 로드 (설정이 없으면 전체 기간 수집)
    history_settings = config.get("history_settings", {})
    start_date_str = history_settings.get("start_date")
    end_date_str = history_settings.get("end_date")
    
    start_date = None
    if start_date_str:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        
    end_date = None
    if end_date_str:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc) + timedelta(days=1)

    checkpoints = load_checkpoints()

    # StringSession을 사용하여 로그인 유지
    user_client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    bot_client = TelegramClient('bot_history_session', API_ID, API_HASH)

    try:
        await user_client.connect()
        await bot_client.start(bot_token=BOT_TOKEN)
        
        range_msg = f"{start_date_str or '시작'} ~ {end_date_str or '현재'}"
        logger.info(f"과거 데이터 수집 시작 (범위: {range_msg}, 체크포인트 사용)")

        for channel_id in SOURCE_CHANNELS:
            try:
                entity = await user_client.get_entity(channel_id)
                chat_title = getattr(entity, 'title', channel_id)
                channel_key = str(channel_id)
                
                # 해당 채널의 마지막 수집 ID 확인
                last_id = checkpoints.get(channel_key, 0)
                logger.info(f"채널 분석 중: {chat_title} (마지막 ID: {last_id})")
                
                count = 0
                # reverse=True와 min_id를 사용하여 전체 역사를 시간 순으로 가져옴
                async for message in user_client.iter_messages(entity, offset_date=start_date, min_id=last_id, reverse=True):
                    if end_date and message.date > end_date:
                        logger.info(f"{chat_title}: 설정된 종료 날짜에 도달하여 수집 중단")
                        break

                    msg_text = message.text or ""
                    if not msg_text and not message.media: continue
                    if KEYWORDS and not any(kw.lower() in msg_text.lower() for kw in KEYWORDS):
                        continue

                    # 시간 정보 구성
                    kst = timezone(timedelta(hours=9))
                    original_time = message.date.astimezone(kst).strftime('%Y-%m-%d %H:%M:%S')
                    forward_msg = f"🕒 **[원본 시간: {original_time}]**\n📢 **[{chat_title}]**\n\n{msg_text}"
                    
                    try:
                        from telethon.tl.types import MessageMediaWebPage
                        has_file = message.media and not isinstance(message.media, MessageMediaWebPage)

                        if has_file:
                            try:
                                await bot_client.send_message(DESTINATION, forward_msg, file=message.media)
                            except Exception as media_error:
                                logger.warning(f"미디어 전송 실패, 텍스트 전송: {media_error}")
                                await bot_client.send_message(DESTINATION, forward_msg)
                        else:
                            await bot_client.send_message(DESTINATION, forward_msg)
                        
                        # 체크포인트 업데이트 및 저장
                        checkpoints[channel_key] = message.id
                        count += 1
                        
                        # API 보호를 위해 10개마다 체크포인트 파일 저장
                        if count % 10 == 0:
                            save_checkpoints(checkpoints)
                            logger.info(f"{chat_title}: {count}개 전달 완료 (체크포인트 저장됨)")
                        
                        await asyncio.sleep(1.0) # 전송 속도 조절 (보수적)
                        
                    except Exception as send_error:
                        from telethon.errors import FloodWaitError
                        if isinstance(send_error, FloodWaitError):
                            logger.warning(f"FloodWait: {send_error.seconds}초 대기 필요")
                            await asyncio.sleep(send_error.seconds)
                        else:
                            logger.error(f"메시지 전송 오류: {send_error}")
                            await asyncio.sleep(5)

                # 채널 종료 시 최종 체크포인트 저장
                save_checkpoints(checkpoints)
                logger.info(f"채널 {chat_title} 완료. (이번 실행 수집: {count}개)")

            except Exception as e:
                logger.error(f"채널 {channel_id} 처리 중 오류: {e}")

    finally:
        save_checkpoints(checkpoints) # 예기치 못한 종료 시에도 저장 시도
        await user_client.disconnect()
        await bot_client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
