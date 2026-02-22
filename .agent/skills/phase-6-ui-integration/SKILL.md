---
name: phase-6-ui-integration
description: |
  실제 UI를 구현하고 API와 연동하는 스킬입니다.
  프론트엔드-백엔드 통합, 상태 관리 및 API 클라이언트 아키텍처를 다룹니다.

  프론트엔드를 백엔드 API와 연결해야 할 때 선제적으로 사용하십시오.

  Triggers: UI implementation, API integration, state management, UI 구현, API連携, 状态管理,
  implementación UI, integración API, gestión de estado,
  implémentation UI, integración API, gestion d'état,
  UI-Implementierung, API-Integration, Zustandsverwaltung,
  implementazione UI, integrazione API, gestione dello stato

  Do NOT use for: 목업 생성, 백엔드 전용 개발 또는 디자인 시스템 설정에는 사용하지 마십시오.
imports:
  - ${PLUGIN_ROOT}/templates/pipeline/phase-6-ui.template.md
# hooks: Managed by hooks/hooks.json (unified-write-post.js, unified-stop.js) - GitHub #9354 workaround
agent: bkit:pipeline-guide
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
user-invocable: false
next-skill: phase-7-seo-security
pdca-phase: do
task-template: "[Phase-6] {feature}"
---

# Phase 6: UI 구현 + API 연동 (UI Implementation + API Integration)

> 실제 UI 구현 및 API 연동 단계입니다.

## 프로젝트 목적

디자인 시스템 컴포넌트를 사용하여 실제 화면을 구현하고, 백엔드 API와 연결하여 데이터를 동적으로 처리합니다.

## 이 단계에서 할 일

1. **페이지 구현**: 각 화면 개발 (Next.js App Router 등 활용)
2. **상태 관리**: 클라이언트 상태(Zustand, Context 등) 및 서버 상태(TanStack Query) 관리
3. **API 연동**: 설계된 백엔드 API 호출 및 데이터 연결
4. **에러 핸들링**: 로딩 상태, 데이터 부재, 에러 발생 시 UI 처리

## 결과물 (Deliverables)

```
src/
├── app/                # Next.js 페이지 컴포넌트
├── features/           # 기능별 컴포넌트 및 로직
└── hooks/              # API 호출을 위한 커스텀 훅 (useAuth, useProducts 등)
```

---

## API 클라이언트 아키텍처

### 왜 중앙 집중식 API 클라이언트가 필요한가요?
- **공통 에러 처리**: 한곳에서 에러를 관리하여 사용자에게 일관된 메시지 제공
- **인증 토큰 관리**: 모든 요청에 자동으로 인증 헤더 주입
- **일관된 응답 형식**: API 응답 타입을 표준화하여 타입 안전성 확보

### 3계층 API 구조
1. **API 클라이언트 계층**: 공통 설정, 인터셉터, 에러 처리 (axios/fetch 래퍼)
2. **서비스 계층**: 도메인별 API 호출 함수 (auth.service, product.service 등)
3. **UI 계층**: 커스텀 훅을 통해 컴포넌트에서 데이터 사용

## 에러 핸들링 및 상태 관리 가이드

```
서버 상태 (API 데이터) → TanStack Query / SWR 권장
클라이언트 상태 (UI 상태) → useState / useReducer
전역 상태 (인증 정보 등) → Zustand / Context API
폼 상태 → React Hook Form 권장
```

---

## 다음 단계

Phase 7: SEO/보안 → 기능 구현이 완료되었으니, 이제 검색 엔진 최적화와 보안 강화 단계로 이동합니다.
