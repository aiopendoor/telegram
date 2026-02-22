---
name: dynamic
description: |
  bkend.ai BaaS 플랫폼을 사용한 풀스택 개발 스킬입니다.
  다이내믹 웹 앱을 위한 인증, 데이터 저장, API 연동을 다룹니다.

  "init dynamic" 또는 "dynamic init" 명령어로 프로젝트를 시작하십시오.

  사용자가 서버 관리 없이 로그인, 데이터베이스 또는 백엔드 기능이 필요할 때 선제적으로 사용하십시오.

  Triggers: fullstack, BaaS, bkend, authentication, login feature, signup, database,
  web app, SaaS, MVP, init dynamic, dynamic init,
  풀스택, 인증, 로그인 기능, 회원가입, 데이터베이스, 웹앱,
  フルスタック, 認証, ログイン機能, データベース, 全栈, 身份验证, 登录功能,
  autenticación, inicio de sesión, registro, base de datos, fullstack, aplicación web,
  authentification, connexion, inscription, base de données, fullstack, application web,
  Authentifizierung, Anmeldung, Registrierung, Datenbank, Fullstack, Web-App,
  autenticazione, accesso, registrazione, database, fullstack, applicazione web

  Do NOT use for: 정적 웹사이트, 맞춤형 인프라가 필요한 엔터프라이즈급 시스템에는 사용하지 마십시오.
argument-hint: "[init|guide|help]"
agent: bkit:bkend-expert
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - mcp__bkend__*
user-invocable: true
imports:
  - ${PLUGIN_ROOT}/templates/design.template.md
next-skill: phase-1-schema
pdca-phase: plan
task-template: "[Init-Dynamic] {feature}"
---

# 중급 (Dynamic) 스킬 가이드

## 제공 액션 (Actions)

| 액션 | 설명 | 예시 |
|--------|-------------|---------|
| `init` | 프로젝트 초기화 (/init-dynamic 기능) | `/dynamic init my-saas` |
| `guide` | 개발 가이드 표시 | `/dynamic guide` |
| `help` | BaaS 연동 도움말 | `/dynamic help` |

### init (프로젝트 초기화)
1. Next.js + Tailwind 프로젝트 구조 생성
2. bkend.ai MCP 설정 (.mcp.json)
3. CLAUDE.md 생성 (다이내믹 프로젝트 레벨 명시)
4. docs/ 폴더 구조 생성
5. src/lib/bkend.ts 클라이언트 템플릿 생성
6. .bkit-memory.json 초기화

### guide (개발 가이드)
- bkend.ai 인증/데이터 설정 가이드
- Phase 1-9 전체 파이프라인 가이드
- API 연동 패턴 안내

### help (BaaS 도움말)
- bkend.ai 기본 개념 설명
- 인증, 데이터베이스, 파일 저장소 사용법
- MCP 연동 방법 설명

## 권장 대상

- 프론트엔드 개발자
- 1인 창업자
- 풀스택 서비스를 빠르게 구축하고자 하는 개발자

## 기술 스택 (Tech Stack)

```
Frontend:
- React / Next.js 14+
- TypeScript
- Tailwind CSS
- TanStack Query (데이터 패칭)
- Zustand (상태 관리)

Backend (BaaS):
- bkend.ai
  - 자동 REST API 생성
  - MongoDB 기반 데이터베이스
  - 내장 인증 시스템 (JWT)
  - 실시간 기능 (WebSocket)

Deployment:
- Vercel (프론트엔드)
- bkend.ai (백엔드)
```

### 언어 티어 가이드 (Language Tier Guidance)

> **권장**: 티어 1-2 언어
>
> 다이내믹 레벨은 AI와 높은 호환성을 가진 풀스택 개발을 지원합니다.

| 티어 | 허용 여부 | 이유 |
|------|---------|--------|
| Tier 1 | ✅ 최우선 | AI의 풀 지원 가능 |
| Tier 2 | ✅ 허용 | 모바일(Flutter/RN), 현대적 웹(Vue, Astro) |
| Tier 3 | ⚠️ 제한적 | 플랫폼 종속적인 필요성이 있을 때만 |
| Tier 4 | ❌ 부적합 | 이관(Migration) 권장 |

**모바일 개발**:
- React Native (TypeScript 기반 티어 1) - 권장
- Flutter (Dart 기반 티어 2) - 지원 가능

## 프로젝트 구조

```
project/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/            # 인증 관련 라우트
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── (main)/            # 주요 기능 라우트
│   │   │   ├── dashboard/
│   │   │   └── settings/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   │
│   ├── components/             # UI 컴포넌트
│   │   ├── ui/                # 공통 UI (Button, Input 등)
│   │   └── features/          # 기능별 특정 컴포넌트
│   │
│   ├── hooks/                  # 커스텀 훅
│   │   ├── useAuth.ts
│   │   └── useQuery.ts
│   │
│   ├── lib/                    # 유틸리티 및 클라이언트
│   │   ├── bkend.ts           # bkend.ai 클라이언트 설정
│   │   └── utils.ts
│   │
│   ├── stores/                 # 전역 상태 관리 (Zustand)
│   │   └── auth-store.ts
│   │
│   └── types/                  # TypeScript 타입 정의
│       └── index.ts
│
├── docs/                       # PDCA 문서
│   ├── 01-plan/
│   ├── 02-design/
│   │   ├── data-model.md      # 데이터 모델링
│   │   └── api-spec.md        # API 명세
│   ├── 03-analysis/
│   └── 04-report/
│
├── .mcp.json                   # bkend.ai MCP 설정
├── .env.local                  # 환경 변수
├── package.json
└── README.md
```

## 핵심 요약 및 한계

```
❌ 한계점:
- 복잡한 백엔드 로직 (Serverless function 제한)
- 대규모 트래픽 (BaaS 할당량 제한 이내)
- 인프라 직접 제어 불가
- 마이크로서비스 아키텍처 비적합
```

## 업그레이드 시점

다음과 같은 경우 **엔터프라이즈 레벨**로 전환하십시오:
- → "트래픽이 폭발적으로 증가할 것으로 예상될 때"
- → "마이크로서비스로 분리하고 싶을 때"
- → "자체 서버/인프라 구축이 필요할 때"
- → "복잡한 백엔드 비즈니스 로직이 필요할 때"
