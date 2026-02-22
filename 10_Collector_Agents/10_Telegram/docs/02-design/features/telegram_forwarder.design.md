# telegram_forwarder Design Document

> **Summary**: 사용자의 텔레그램 계정(User API)과 봇(@opendoorai)을 결합하여 실시간 메시지 전달 시스템을 구현하기 위한 기술적 설계
>
> **Project**: Antigravity Telegram Tools
> **Version**: 1.0.0
> **Author**: Antigravity AI
> **Date**: 2026-02-14
> **Status**: Draft
> **Planning Doc**: [telegram_forwarder.plan.md](../01-plan/features/telegram_forwarder.plan.md)

---

## 1. Overview

### 1.1 Design Goals
- 실시간 리스너를 통한 지연 없는 메시지 포워딩.
- 비정상 종료 시 자동 재시작 및 세션 유지.
- `.env`와 `channels.json`을 통한 설정의 분리.

### 1.2 Design Principles
- **Separation of Concerns**: 메시지 수신(User API)과 메시지 발신(Bot API) 로직을 분리.
- **Asynchronous Execution**: `asyncio` 기반의 비동기 처리 라이브러리(`Telethon`) 사용.
- **Error Resilience**: 네트워크 오류 또는 API 제한에 대한 예외 처리 설계.

---

## 2. Architecture

### 2.1 Component Diagram

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  Telegram Cloud │       │   Forwarder     │       │  Telegram Cloud │
│  (Source Chans) │──────▶│   (Script)      │──────▶│   (Bot API)     │
└─────────────────┘       └─────────────────┘       └─────────────────┘
         ▲                         │                         │
         │                         ▼                         ▼
   (User Session)           (channels.json)            (@opendoorai)
```

### 2.2 Data Flow
1. **Event**: 사용자가 구독 중인 채널에 새 메시지 발생.
2. **Listener**: `Telethon` 리스너가 해당 이벤트를 감지.
3. **Filter**: 
   - `channels.json`에 정의된 대상 채널인지 확인.
   - (선택) 키워드 매칭 여부 확인.
4. **Action**: `Bot API`를 호출하여 본인의 텔레그램으로 메시지 전달.

---

## 3. Data Model

### 3.1 Configuration (channels.json)
```json
{
  "source_channels": [
    "@channel_username",
    -1001234567890
  ],
  "destination_user_id": "me",
  "keywords": ["공시", "급등", "매수"],
  "settings": {
    "forward_media": true,
    "remove_duplicates": true
  }
}
```

---

## 4. Implementation Details

### 4.1 Required Libraries
- `telethon`: 사용자 계정 자동화 핵심 라이브러리.
- `python-dotenv`: 환경 변수 로드.
- `asyncio`: 비동기 런타임.

### 4.2 Key Logic (Pseudo-code)
```python
@client.on(events.NewMessage)
async def handler(event):
    chat = await event.get_chat()
    if chat.id in SOURCE_CHANNELS:
        if any(kw in event.raw_text for kw in KEYWORDS):
            await bot.send_message("me", f"[{chat.title}]\n{event.raw_text}")
```

---

## 5. Error Handling

| Code/Situation | Cause | Handling |
|------|---------|----------|
| FloodWaitError | 너무 빠른 요청으로 인한 제한 | 해당 시간만큼 `sleep` 후 재시도 |
| ConnectionError | 네트워크 끊김 | `client.run_until_disconnected()`로 재연결 시도 |
| SessionError | 세션 파일 손상/로그아웃 | 사용자에게 재인증(로그인) 요청 메시지 출력 |

---

## 6. Implementation Order

1. [ ] **환경 구축**: `pip3 install telethon python-dotenv`
2. [ ] **설정 파일**: `channels.json` 생성 및 셈플 데이터 입력.
3. [ ] **핵심 스크립트**: `telegram_forwarder.py` 작성.
4. [ ] **세션 인증**: 최초 실행 시 본인 계정 로그인 연동.
5. [ ] **봇 연동**: 알려주신 봇 토큰을 통한 발신 테스트.

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-02-14 | Initial design for Telegram forwarder | Antigravity AI |
