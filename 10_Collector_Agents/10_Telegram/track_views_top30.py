import os
import json
import asyncio
import logging
import heapq
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession
from supabase import create_client, Client
import google.generativeai as genai

# .env 로드
load_dotenv(os.path.join(os.path.dirname(__file__), "../../00_Core/.env"))

# 환경 변수 설정
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
# 조회수 전용 세션이 없다면 리얼타임 세션 사용
SESSION_STRING = os.getenv("TELEGRAM_SESSION_REALTIME") or os.getenv("TELEGRAM_SESSION_STRING")

# Supabase 설정
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_SERVICE_KEY")

# Gemini 설정
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def extract_topic_and_content(text):
    """Gemini를 사용하여 메시지에서 주제와 핵심 내용을 추출합니다."""
    if not GEMINI_API_KEY or not text.strip():
        # Gemini 설정이 없으면 텍스트 기반으로 단순 추출
        lines = text.strip().split('\n')
        topic = lines[0][:50] if lines else "No Title"
        content = text[:200]
        return topic, content

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        아래 텔레그램 메시지에서 '주제(Topic)'와 '주요 내용(Main Content)'을 추출해줘.
        주제는 한 문장으로 명확하게, 주요 내용은 2~3문장 이내로 핵심만 요약해줘.
        결과는 JSON 형식으로 답변해줘. {{"topic": "...", "content": "..."}}

        메시지 내용:
        {text}
        """
        response = model.generate_content(prompt)
        # JSON 파싱 시도 (백틱 제거 등 처리)
        result_text = response.text.replace('```json', '').replace('```', '').strip()
        result = json.loads(result_text)
        return result.get("topic", "No Topic"), result.get("content", "No Content")
    except Exception as e:
        logger.error(f"Gemini 요약 실패: {e}")
        return text.split('\n')[0][:50], text[:200]

async def main():
    if not SESSION_STRING:
        logger.error("텔레그램 세션 정보가 없습니다.")
        return

    # 1. 설정 로드
    with open('channels.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    source_channels = config.get("source_channels", [])
    
    # 2. 텔레그램 연결
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.connect()
    
    # 3. 지난 24시간 동안의 메시지 중 조회수가 높은 상위 30개 수집
    logger.info("🕒 지난 24시간 동안의 인기 메시지 분석을 시작합니다...")
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    
    all_messages = []
    
    for channel_id in source_channels:
        try:
            entity = await client.get_entity(channel_id)
            chat_title = getattr(entity, 'title', str(channel_id))
            
            # 조회수는 iter_messages에서 직접 정렬할 수 없으므로 모두 가져와서 정렬
            async for message in client.iter_messages(entity, offset_date=yesterday, reverse=True):
                if message.text:
                    views = message.views or 0
                    all_messages.append({
                        "views": views,
                        "text": message.text,
                        "channel_name": chat_title,
                        "message_id": message.id
                    })
        except Exception as e:
            logger.error(f"채널 {channel_id} 조회수 수집 실패: {e}")

    # 4. 조회수 기준 상위 30개 추출
    top_30 = sorted(all_messages, key=lambda x: x['views'], reverse=True)[:30]
    logger.info(f"📊 총 {len(all_messages)}개 메시지 중 상위 30개를 선별했습니다.")

    # 5. Supabase 연결 및 저장
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("Supabase 설정이 없습니다.")
        return
        
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    target_date = datetime.now().strftime('%Y-%m-%d')

    for i, msg in enumerate(top_30, 1):
        try:
            # 주제 및 내용 추출
            topic, content = await extract_topic_and_content(msg['text'])
            
            record = {
                "rank": i,
                "target_date": target_date,
                "topic": topic,
                "content": content,
                "views": msg['views'],
                "channel_name": msg['channel_name'],
                "message_id": msg['message_id']
            }
            
            # Upsert (동일 날짜/순위 중복 방지)
            supabase.table("telegram_daily_top30").upsert(
                record, on_conflict="target_date, rank"
            ).execute()
            
            logger.info(f"✅ [{i}위] {msg['views']}회 | {topic}")
            
            # API 제한 방지
            await asyncio.sleep(1)
            
        except Exception as e:
            logger.error(f"❌ {i}위 데이터 저장 실패: {e}")

    await client.disconnect()
    logger.info(f"🎉 {target_date} 일일 조회수 TOP 30 집계 완료!")

if __name__ == "__main__":
    asyncio.run(main())
