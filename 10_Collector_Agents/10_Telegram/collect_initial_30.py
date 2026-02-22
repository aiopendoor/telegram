import os
import json
import asyncio
import heapq
from telethon import TelegramClient
from telethon.sessions import StringSession
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# .env 로드
load_dotenv(os.path.join(os.path.dirname(__file__), "../../00_Core/.env"))

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SESSION_STRING = os.getenv("TELEGRAM_SESSION_STRING")

# 대상 채널 목록 (중복 제거됨)
TARGET_CHANNELS = [
    "KISGregKim", "globaletfi", "darthacking", 
    "bornlupin", "easobi", "quantmalgo", "free_life59", 
    "insidertracking", "tambangwang", "Macrojunglemicrolens", "cahier_de_market"
]

DESTINATION = "@opendoorai"
CHECKPOINT_FILE = 'last_processed_ids.json'
SEPARATOR = "\n" + "━" * 20 + "\n"
LIMIT_PER_CHANNEL = 30
BUNDLE_SIZE = 20

def save_checkpoints(checkpoints):
    try:
        with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f:
            json.dump(checkpoints, f, indent=4)
        print("💾 체크포인트가 저장되었습니다.")
    except Exception as e:
        print(f"❌ 체크포인트 저장 실패: {e}")

async def send_split_message(bot_client, destination, text):
    """텔레그램 메시지 길이 제한(4096)을 고려하여 분할 전송"""
    if len(text) <= 4000:
        await bot_client.send_message(destination, text)
        return

    parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
    for part in parts:
        await bot_client.send_message(destination, part)
        await asyncio.sleep(0.5)

async def main():
    checkpoints = {}
    if not SESSION_STRING:
        print("❌ TELEGRAM_SESSION_STRING이 없습니다.")
        return

    # 세션 파일 충돌을 피하기 위해 타임스탬프 기반 세션명 사용
    session_name = f'bot_collect_30_{int(datetime.now().timestamp())}'
    user_client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    bot_client = TelegramClient('bot_history_session', API_ID, API_HASH)

    try:
        await user_client.connect()
        await bot_client.start(bot_token=BOT_TOKEN)
        print("🚀 신규 채널 초기 30개 '날짜순 정렬' 수집을 시작합니다.")

        # 체크포인트 로드
        if os.path.exists(CHECKPOINT_FILE):
            with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
                checkpoints = json.load(f)

        heap = []
        iterators = {}
        channel_counts = {chan: 0 for chan in TARGET_CHANNELS}
        channel_titles = {}

        # 각 채널의 첫 번째 메시지 로드하여 힙 초기화
        for chan in TARGET_CHANNELS:
            print(f"🔍 [{chan}] 초기화 시도 중...")
            try:
                entity = await user_client.get_entity(chan)
                title = getattr(entity, 'title', chan)
                channel_titles[chan] = title
                
                # reverse=True: 가장 오래된 것부터
                print(f"📑 [{chan}] 이터레이터 생성 중...")
                it = user_client.iter_messages(entity, reverse=True)
                iterators[chan] = it
                
                print(f"📥 [{chan}] 첫 메시지 로드 시도 중...")
                msg = await it.__anext__()
                if msg:
                    # (날짜, 채널ID, 메시지객체)
                    heapq.heappush(heap, (msg.date, chan, msg))
                    print(f"✅ [{chan}] 초기화 성공 (첫 메시지 날짜: {msg.date})")
            except StopAsyncIteration:
                print(f"⚠️ [{chan}] 메시지가 없습니다.")
            except Exception as e:
                print(f"❌ [{chan}] 초기화 오류: {e}")

        bundle_buffer = []
        bundle_checkpoints = {}
        kst = timezone(timedelta(hours=9))

        while heap:
            # 1. 가장 과거 메시지 추출
            date, chan, msg = heapq.heappop(heap)
            
            if channel_counts[chan] % 10 == 0:
                 print(f"🔄 진행 중... 힙 크기: {len(heap)}, [{chan}] 수집: {channel_counts[chan]}/30")
            
            if channel_counts[chan] < LIMIT_PER_CHANNEL:
                # 메시지 가공
                original_time = msg.date.astimezone(kst).strftime('%Y-%m-%d %H:%M:%S')
                text = (msg.text or "").strip()
                if not text and msg.media:
                    text = "[미디어 메시지]"
                
                if text:
                    formatted = f"🕒 **[{original_time}]** | 📢 **[{channel_titles[chan]}]**\n{text}\n"
                    bundle_buffer.append(formatted)
                    bundle_checkpoints[chan] = msg.id
                    channel_counts[chan] += 1
                
                # 번들 전송
                if len(bundle_buffer) >= BUNDLE_SIZE:
                    combined = SEPARATOR.join(bundle_buffer)
                    await send_split_message(bot_client, DESTINATION, combined)
                    checkpoints.update(bundle_checkpoints)
                    bundle_buffer = []
                    bundle_checkpoints = {}
                    print(f"📤 {BUNDLE_SIZE}개 메시지 번들 전송 완료 (정렬 중...)")
                    await asyncio.sleep(2)

            # 2. 해당 채널의 다음 메시지 보충 (30개 미만일 때만)
            if channel_counts[chan] < LIMIT_PER_CHANNEL:
                try:
                    next_msg = await iterators[chan].__anext__()
                    heapq.heappush(heap, (next_msg.date, chan, next_msg))
                except StopAsyncIteration:
                    print(f"🏁 [{channel_titles[chan]}] 채널 종료 (총 {channel_counts[chan]}개 수집)")
                except Exception as e:
                    print(f"❌ [{chan}] 보충 중 오류: {e}")

        # 마지막 남은 번들 처리
        if bundle_buffer:
            combined = SEPARATOR.join(bundle_buffer)
            await send_split_message(bot_client, DESTINATION, combined)
            checkpoints.update(bundle_checkpoints)
            print(f"📤 마지막 {len(bundle_buffer)}개 메시지 전송 완료.")

        print("\n📊 최종 수집 현황:")
        for chan, count in channel_counts.items():
            print(f"- {chan}: {count}개")

        print("작업 완료!")

    except Exception as e:
        print(f"🔥 프로그램 실행 중 치명적 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        save_checkpoints(checkpoints)
        await user_client.disconnect()
        await bot_client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
