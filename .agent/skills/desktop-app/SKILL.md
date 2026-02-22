---
name: desktop-app
description: |
  크로스 플랫폼 데스크톱 애플리케이션 개발을 위한 가이드입니다.
  Electron 및 Tauri 프레임워크를 다룹니다.

  사용자가 웹 기술을 사용하여 데스크톱 앱을 구축하고자 할 때 선제적으로 사용하십시오.

  Triggers: desktop app, Electron, Tauri, mac app, windows app, 데스크톱 앱, デスクトップアプリ, 桌面应用,
  aplicación de escritorio, app de escritorio,
  application de bureau, application desktop,
  Desktop-Anwendung, Desktop-App,
  applicazione desktop, app desktop

  Do NOT use for: 웹 전용 프로젝트, 모바일 앱 또는 서버 사이드 개발에는 사용하지 마십시오.
agent: bkit:pipeline-guide
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebSearch
user-invocable: false
---

# 데스크톱 앱 개발 가이드 (Desktop App Development)

## 개요 (Overview)

웹 기술(HTML, CSS, JavaScript)을 사용하여 데스크톱 앱을 개발하기 위한 가이드입니다.
단일 코드베이스로 Windows, macOS, Linux를 동시에 지원할 수 있습니다.

---

## 프레임워크 선택 가이드 (Framework Selection)

### 티어별 프레임워크 추천 (v1.3.0)

| 프레임워크 | 티어 (Tier) | 추천도 | 주요 특징 |
|-----------|------|----------------|----------|
| **Tauri** | Tier 2 | ⭐ 최우선 추천 | 가벼움 (3MB), Rust 기반 보안, 고성능 |
| **Electron** | Tier 3 | 지원 가능 | 성숙한 생태계, VS Code 등 검증된 사례 |

> **AI-Native 추천**: Tauri
> - 연간 35% 성장률
> - 메모리 사용량 20-40MB (Electron은 200-400MB)
> - Tauri 2.0을 통한 모바일(iOS/Android) 지원
> - Rust 백엔드를 통한 메모리 안전성 확보

> **생태계 추천**: Electron
> - 풍부한 라이브러리 및 도구
> - Node.js 기술 스택 완전 활용
> - VS Code, Slack 등 대규모 서비스에서 검증됨

### 프로젝트 레벨별 권장 사항

```
Starter (스타터) → Tauri (v2) [Tier 2]
  - Electron보다 설정이 간단함
  - 실행 파일 용량이 매우 작음 (~3MB vs ~150MB)

Dynamic (다이내믹) → Tauri + 자동 업데이트 [Tier 2]
  - 서버 연동 및 자동 업데이트 포함
  - 낮은 메모리 점유율로 쾌적한 환경 제공

Enterprise (엔터프라이즈) → Tauri [Tier 2] 또는 Electron [Tier 3]
  - 성능과 보안이 중요하다면 Tauri 추천
  - 복잡한 Node.js 통합이 필요하다면 Electron 추천
```

---

## Electron 가이드

### 프로젝트 생성

```bash
# electron-vite로 생성 (권장)
npm create @electron-vite/create my-electron-app
cd my-electron-app

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

### 폴더 구조

```
my-electron-app/
├── src/
│   ├── main/               # 메인 프로세스 (Node.js)
│   │   └── index.ts        # 앱 진입점, 윈도우 관리
│   ├── preload/            # 프리로드 스크립트
│   │   └── index.ts        # 렌더러↔메인 브릿지
│   └── renderer/           # 렌더러 프로세스 (Web)
│       ├── src/            # React/Vue 코드
│       └── index.html      # HTML 진입점
├── resources/              # 앱 아이콘, 에셋
├── electron.vite.config.ts # 빌드 설정
├── electron-builder.yml    # 배포 설정
└── package.json
```

### 핵심 개념: 프로세스 분리 (Process Separation)

```
┌─────────────────────────────────────────────────────┐
│                    데스크톱 앱 (Electron)             │
├─────────────────────────────────────────────────────┤
│  메인 프로세스 (Main Process - Node.js)               │
│  - 시스템 API 접근 (파일, 네트워크 등)                 │
│  - 윈도우 생성 및 관리                                │
│  - 메뉴, 트레이 관리                                  │
├─────────────────────────────────────────────────────┤
│  프리로드 스크립트 (Preload - Bridge)                  │
│  - 메인↔렌더러 간 안전한 통신                         │
│  - 특정 API만 선별적으로 노출                         │
├─────────────────────────────────────────────────────┤
│  렌더러 프로세스 (Renderer - Chromium)                │
│  - 웹 UI (React, Vue 등)                              │
│  - DOM 접근                                          │
│  - 보안을 위해 Node.js API 직접 접근 불가               │
└─────────────────────────────────────────────────────┘
```

---

## Tauri 가이드

### 프로젝트 생성

```bash
# 사전 준비: Rust 설치 필수 (https://rustup.rs)

# Tauri 앱 생성
npm create tauri-app my-tauri-app
cd my-tauri-app

# 의존성 설치
npm install

# 개발 서버 실행
npm run tauri dev
```

### 폴더 구조

```
my-tauri-app/
├── src/                    # 프론트엔드 (React, Vue 등)
│   ├── App.tsx
│   └── main.tsx
├── src-tauri/              # Tauri 백엔드 (Rust)
│   ├── src/
│   │   ├── main.rs         # 메인 진입점
│   │   └── lib.rs          # 명령어(Command) 정의
│   ├── tauri.conf.json     # Tauri 설정 파일
│   └── Cargo.toml          # Rust 의존성 관리
├── public/
└── package.json
```

---

## 웹 vs 데스크톱 차이점

### 파일 시스템 접근
- **웹**: 불가능 (사용자가 직접 파일을 선택해야 함)
- **데스크톱**: 자유로운 읽기/쓰기 권한

### 시스템 통합 기능
- 시스템 트레이 아이콘 (System Tray)
- 전역 단축키 (Global Shortcuts)
- 네이티브 알림 (Native Notifications)
- 드래그 앤 드롭 (파일 경로 직접 획득)
- 메뉴바(Menu) 구성

---

## 데스크톱용 PDCA 체크리스트

### Phase 1: 스키마 (Schema)
- [ ] 로컬 데이터 저장 방식 결정 (SQLite, JSON 파일 등)
- [ ] 클라우드 동기화 필요 여부 결정

### Phase 3: 목업 (Mockup)
- [ ] 플랫폼별 UI 가이드 준수 검토 (macOS, Windows)
- [ ] 키보드 단축키 기획
- [ ] 메뉴 구조 설계

### Phase 7: 보안 (Security)
- [ ] Node.js API 직접 노출 금지 (contextBridge 사용)
- [ ] 외부 URL 로드 시 보안 처리
- [ ] 민감 데이터 저장 시 암호화 처리

### Phase 9: 배포 (Deployment)
- [ ] 코드 서명 (Code Signing - macOS 공증, Windows 서명)
- [ ] 자동 업데이트 서버 설정
- [ ] 앱 스토어 심사 준비 (필요 시)
