---
name: phase-2-convention
description: |
  코딩 규칙과 컨벤션을 정의하는 스킬입니다.
  일관된 코드 스타일을 보장하고 AI 협업을 위한 코딩 표준을 명시합니다.

  새 프로젝트를 시작하거나 코딩 표준이 필요할 때 선제적으로 사용하십시오.

  Triggers: convention, coding style, naming rules, 컨벤션, コンベンション, 编码风格,
  convención, estilo de código, reglas de nombrado, convention, style de codage, règles de nommage,
  Konvention, Coding-Stil, Namensregeln, convenzione, stile di codice, regole di denominazione

  Do NOT use for: 이미 컨벤션이 설정된 기존 프로젝트, 배포 또는 테스트 작업에는 사용하지 마십시오.
agent: bkit:pipeline-guide
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
user-invocable: false
imports:
  - ${PLUGIN_ROOT}/templates/pipeline/phase-2-convention.template.md
  - ${PLUGIN_ROOT}/templates/shared/naming-conventions.md
next-skill: phase-3-mockup
pdca-phase: plan
task-template: "[Phase-2] {feature}"
---

# Phase 2: 코딩 컨벤션 (Coding Convention)

> 코드 작성 규칙을 정의합니다.

## 프로젝트 목적

일관된 코드 스타일을 유지합니다. 특히 AI와 협업할 때 AI가 코드를 작성할 때 어떤 스타일을 따라야 하는지 명확하게 지시하는 것이 중요합니다.

## 이 단계에서 할 일

1. **명명 규칙 (Naming Rules)**: 변수, 함수, 파일, 폴더 이름 규칙
2. **코드 스타일 (Code Style)**: 들여쓰기, 따옴표, 세미콜론 등
3. **구조 규칙 (Structure Rules)**: 폴더 구조, 파일 분리 기준
4. **패턴 정의 (Pattern Definition)**: 자주 사용되는 코드 패턴

## 결과물 (Deliverables)

```
Project Root/
├── CONVENTIONS.md          # 전체 컨벤션 문서
└── docs/01-plan/
    ├── naming.md           # 명명 규칙 상세
    └── structure.md        # 구조 규칙 상세
```

---

## 환경 변수 컨벤션 (Environment Variable Convention)

### 왜 설계 단계에서 정의하나요?

```
❌ 배포 직전에 환경 변수 정리
   → 변수 누락, 이름 불일치로 인한 배포 지연 발생

✅ 설계 단계에서 규칙 수립
   → 일관된 명명, 명확한 카테고리화로 빠른 배포 가능
```

### 환경 변수 명명 규칙

| 접두사 (Prefix) | 용도 | 노출 범위 | 예시 |
|--------|---------|----------------|---------|
| `NEXT_PUBLIC_` | 클라이언트 노출용 | 브라우저 | `NEXT_PUBLIC_API_URL` |
| `DB_` | 데이터베이스 관련 | 서버 전용 | `DB_HOST`, `DB_PASSWORD` |
| `API_` | 외부 API 키 | 서버 전용 | `API_STRIPE_SECRET` |
| `AUTH_` | 인증 관련 | 서버 전용 | `AUTH_SECRET`, `AUTH_GOOGLE_ID` |

---

## 클린 아키텍처 원칙 (Clean Architecture Principles)

### 4계층 아키텍처 (권장)

```
src/
├── presentation/        # UI 렌더링 및 사용자 이벤트 처리
│   ├── components/      # UI 컴포넌트
│   └── hooks/           # 상태 관리 훅
│
├── application/         # 비즈니스 로직 오케스트레이션
│   └── services/        # API 서비스 래퍼
│
├── domain/              # 비즈니스 규칙 및 타입 정의
│   ├── types/           # 타입 정의
│   └── constants/       # 상수
│
└── infrastructure/      # 외부 시스템 연동
    ├── api/             # API 클라이언트
    └── db/              # DB 연결
```

### 의존성 규칙

```typescript
// ❌ 나쁜 예: Presentation에서 직접 Infrastructure 호출
import { apiClient } from '@/lib/api/client'; // 직접 임포트 금지!

// ✅ 좋은 예: Presentation → Application → Infrastructure
import { userService } from '@/services/user.service';

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: userService.getList, // 서비스를 통해 호출
  });
}
```

---

## 재사용 및 확장 원칙

### 1. 함수 설계
- 한 가지 일만 수행하도록 작게 분리합니다.
- 특정 타입에 종속되지 않도록 제네릭을 활용합니다.

### 2. 컴포넌트 설계
- 조합 가능한(Composable) 구조로 설계합니다.
- Props 확장이 용이하도록 설계합니다.

### 3. 중복 방지 체크리스트
- [ ] utils/ 에 비슷한 함수가 있는가?
- [ ] components/ 에 비슷한 컴포넌트가 있는가?
- [ ] 같은 코드가 2곳 이상에서 반복되는가? → 추출(Extract)

---

## 다음 단계

Phase 3: 목업 개발 → 규칙이 정해졌으니, 이제 빠르게 프로토타입을 제작합니다.
