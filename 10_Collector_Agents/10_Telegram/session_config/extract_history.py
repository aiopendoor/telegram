import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../../../00_Core/.env"))

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

if not API_ID or not API_HASH:
    print("에러: .env 파일에 TELEGRAM_API_ID와 TELEGRAM_API_HASH를 먼저 설정해주세요.")
    exit()

print("--------------------------------------------------")
print("역할: [HISTORY] - 과거 데이터 수집용 세션 추출")
print("--------------------------------------------------")

with TelegramClient('bot_history_session', int(API_ID), API_HASH) as client:
    session_string = StringSession.save(client.session)
    print("\n✅ 아래의 문자열을 복사하여 GitHub Secrets에 'TELEGRAM_SESSION_HISTORY'로 등록하세요:\n")
    print(session_string)
    print("\n--------------------------------------------------")
