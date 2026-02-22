# telegram_forwarder Planning Document

> **Summary**: 사용자가 참여 중인 특정 텔레그램 채널의 메시지를 실시간으로 감지하여 @opendoorai 봇을 통해 본인에게 전달하는 시스템 구축
>
> **Project**: Antigravity Telegram Tools
> **Version**: 1.0.0
> **Author**: Antigravity AI
> **Date**: 2026-02-14
> **Status**: Approved

---

## 1. Overview

### 1.1 Purpose
사용자가 가입된 다수의 텔레그램 채널(약 30개)에서 발생하는 정보를 일일이 확인하지 않고, 필요한 정보를 실시간으로 한곳(@opendoorai 봇)에서 받아보기 위함입니다.

### 1.2 Background
- 텔레그램 채널이 너무 많아 정보 과부하 발생.
- 봇(Bot API)만으로는 사용자가 참여 중인 타 채널의 메시지를 직접 읽을 수 없는 기술적 제약 존재.
- 사용자 계정(User API)을 활용한 자동화 필요.

---

## 2. Scope

### 2.1 In Scope
- [x] 텔레그램 API ID/Hash 및 봇 토큰 설정 연동
- [x] 실시간 메시지 리스너 (User API 기반) 구현
- [x] 지정된 소스 채널 목록 필터링
- [x] @opendoorai 봇을 통한 메시지 전달 (Forwarding)
- [x] 기본적인 키워드 필터링 기능

### 2.2 Out of Scope
- [ ] 메시지 복사가 금지된 채널의 미디어(사진/영상) 강제 복구
- [ ] 웹 대시보드 UI (터미널 기반 실행 우선)

---

## 3. Requirements

### 3.1 Functional Requirements
| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-01 | `.env` 파일로부터 API 자격 증명 로드 | High | Pending |
| FR-02 | `channels.json`에서 감시 대상 채널 목록 관리 | High | Pending |
| FR-03 | 새 메시지 발생 시 실시간 이벤트 트리거 | High | Pending |
| FR-04 | 특정 키워드(예: "공시", "급등") 포함 시에만 전달 | Medium | Pending |
| FR-05 | 텔레그램 봇을 활용한 최종 메시지 전송 | High | Pending |

### 3.2 Non-Functional Requirements
| Category | Criteria | Measurement Method |
|----------|----------|-------------------|
| Stability | 끊김 없는 세션 유지 | 자동 재연결 로직 유무 |
| Security | API 키 노출 방지 | `.env` 관리 및 `.gitignore` 확인 |
| Performance | 실시간성 (딜레이 3초 이내) | 전송 시간 로그 확인 |

---

## 4. Success Criteria

### 4.1 Definition of Done
- [ ] 지정된 채널에 메시지가 올라왔을 때 봇이 나에게 즉시 전달 완료
- [ ] 파이썬 실행 환경에서 에러 없이 24시간 구동 가능 확인
- [ ] `channels.json`을 통해 손쉽게 채널 추가/삭제 가능

---

## 5. Risks and Mitigation
| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| 텔레그램 계정 일시 차단 | High | Medium | 전송 간격 조절 및 과도한 스팸 방지 로직 적용 |
| 세션 만료 | Medium | Low | `session` 파일 영구 저장 및 재인증 가이드 제공 |

---

## 6. Architecture Considerations

### 6.1 Project Level Selection
| Level | Characteristics | Recommended For | Selected |
|-------|-----------------|-----------------|:--------:|
| **Dynamic** | Feature-based modules, services layer | Web apps with backend, SaaS MVPs | [x] |

### 6.2 Key Architectural Decisions
| Decision | Options | Selected | Rationale |
|----------|---------|----------|-----------|
| Library | Telethon / Pyrogram | Telethon | 강력한 비동기 지원 및 풍부한 문서화 |
| Config | JSON / YAML | JSON | 파이썬 기본 라이브러리로 손쉬운 처리 |

---

## 7. Next Steps
1. [ ] 상세 설계 문서 작성 (`telegram_forwarder.design.md`)
2. [ ] 라이브러리 설치 및 세션 인증 환경 구축
3. [ ] 핵심 코드 구현

---

## Version History
| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-02-14 | Initial plan for Telegram forwarder | Antigravity AI |
