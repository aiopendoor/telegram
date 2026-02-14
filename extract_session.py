import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

if not API_ID or not API_HASH:
    print("에러: .env 파일에 TELEGRAM_API_ID와 TELEGRAM_API_HASH를 먼저 설정해주세요.")
    exit()

print("--------------------------------------------------")
print("GitHub Actions용 세션 문자열(StringSession) 추출기")
print("--------------------------------------------------")

with TelegramClient(StringSession(), int(API_ID), API_HASH) as client:
    session_string = client.session.save()
    print("\n✅ 아래의 문자열을 복사하여 GitHub Secrets에 'TELEGRAM_SESSION_STRING'으로 등록하세요:\n")
    print(session_string)
    print("\n--------------------------------------------------")
