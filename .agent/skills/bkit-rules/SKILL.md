---
name: bkit-rules
description: |
  bkit 플러그인의 핵심 규칙입니다. PDCA 방법론, 레벨 감지, 에이전트 자동 트리거 및 코드 품질 표준을 다룹니다.
  이 규칙들은 일관된 AI 네이티브 개발을 보장하기 위해 자동으로 적용됩니다.

  사용자가 기능 개발, 코드 변경 또는 구현 작업을 요청할 때 선제적으로 사용하십시오.

  Triggers: bkit, PDCA, develop, implement, feature, bug, code, design, document,
  개발, 기능, 버그, 코드, 설계, 문서, 開発, 機能, バグ, 开发, 功能, 代码,
  desarrollar, función, error, código, diseño, documento,
  développer, fonctionnalité, bogue, code, conception, document,
  entwickeln, Funktion, Fehler, Code, Design, Dokument,
  sviluppare, funzionalità, bug, codice, design, documento

  Do NOT use for: 코드 변경이 없는 문서 전용 작업, 조사 또는 탐색 작업에는 사용하지 마십시오.
imports:
  - ${PLUGIN_ROOT}/templates/shared/naming-conventions.md
# hooks: Managed by hooks/hooks.json (pre-write.js, unified-write-post.js) - GitHub #9354 workaround
---

# bkit 핵심 규칙 (Core Rules)

> 사용자 명령 없이 자동으로 적용되는 규칙입니다.

## 1. PDCA 자동 적용 규칙

**추측 금지 (No Guessing)**: 불확실한 경우 문서를 확인하고, 문서에 없으면 사용자에게 질문하십시오.
**정보원(SoR) 우선순위**: 코드(실제 동작) > CLAUDE.md > docs/ 내 설계 문서

| 요청 유형 | Claude 동작 방식 |
|--------------|-----------------|
| 새로운 기능 | `docs/02-design/` 확인 → 설계 문서가 없으면 설계부터 진행 |
| 버그 수정 | 코드와 설계를 비교 → 수정 |
| 리팩토링 | 현재 상태 분석 → 계획 → 설계 업데이트 → 실행 |
| 구현 완료 | 갭 분석(Gap analysis) 제안 |

### 템플릿 참조

| 문서 유형 | 템플릿 경로 |
|---------------|---------------|
| 계획 (Plan) | `${CLAUDE_PLUGIN_ROOT}/templates/plan.template.md` |
| 설계 (Design) | `${CLAUDE_PLUGIN_ROOT}/templates/design.template.md` |
| 분석 (Analysis)| `${CLAUDE_PLUGIN_ROOT}/templates/analysis.template.md` |
| 보고서 (Report)| `${CLAUDE_PLUGIN_ROOT}/templates/report.template.md` |

---

## 2. 레벨 자동 감지 (Level Auto-Detection)

### 감지 순서

1. CLAUDE.md에서 명시적인 Level 선언 확인
2. 파일 구조 기반 감지

### 엔터프라이즈 (Enterprise - 2개 이상 조건 충족)

- infra/terraform/ 폴더 존재
- infra/k8s/ 또는 kubernetes/ 폴더 존재
- services/ 폴더 (2개 이상의 서비스)
- turbo.json 또는 pnpm-workspace.yaml
- docker-compose.yml
- .github/workflows/ (CI/CD)

### 다이내믹 (Dynamic - 1개 이상 조건 충족)

- .mcp.json 내 bkend 설정
- lib/bkend/ 또는 src/lib/bkend/
- supabase/ 폴더
- firebase.json

### 스타터 (Starter)

위의 조건 중 어느 것도 충족되지 않음.

### 레벨별 동작 방식

| 항목 | 스타터 (Starter) | 다이내믹 (Dynamic) | 엔터프라이즈 (Enterprise) |
|--------|---------|---------|------------|
| 설명 방식 | 친근함, 전문 용어 지양 | 기술적이지만 명확함 | 간부급 보고 스타일, 전문 용어 사용 |
| 코드 주석 | 상세하게 작성 | 핵심 로직 위주 | 아키텍처 수준 설명 |
| 에러 처리 | 단계별 가이드 제공 | 기술적 해결책 제시 | 원인 및 수정 방안 요약 |
| PDCA 문서 | 단순하게 작성 | 기능별 상세 작성 | 고도의 아키텍처 중심 |
| 기본 에이전트 | `starter-guide` | `bkend-expert` | `enterprise-expert` |
| 참조 스킬 | `starter` | `dynamic` | `enterprise` |

### 레벨 업그레이드 신호

- Starter → Dynamic: "로그인 추가", "데이터 저장", "관리자 페이지"
- Dynamic → Enterprise: "트래픽 급증", "마이크로서비스", "자체 서버 구축"

### 계층적 CLAUDE.md 규칙

```
project/
├── CLAUDE.md                 # 프로젝트 전체 (항상 참조)
├── services/CLAUDE.md        # 백엔드 작업 컨텍스트
├── frontend/CLAUDE.md        # 프론트엔드 작업 컨텍스트
└── infra/CLAUDE.md           # 인프라 구축 컨텍스트
```

규칙: 영역별 특정 규칙 > 프로젝트 전체 규칙

---

## 3. 에이전트 자동 트리거 규칙

### 레벨 기반 선택

사용자가 기능 개발을 요청할 때:
1. 프로젝트 레벨 감지
2. 적절한 에이전트를 자동으로 호출

### 작업 기반 선택

| 사용자 의도 | 자동 호출 에이전트 |
|-------------|-------------------|
| "코드 리뷰", "보안 점검" | `bkit:code-analyzer` |
| "설계 리뷰", "스펙 확인" | `bkit:design-validator` |
| "갭 분석", "검증" | `bkit:gap-detector` |
| "보고서", "요약" | `bkit:report-generator` |
| "QA", "로그 분석" | `bkit:qa-monitor` |
| "파이프라인", "현재 단계" | `bkit:pipeline-guide` |

### 선제적 제안

주요 작업 완료 후 관련 에이전트 사용을 제안합니다.

### 자동 호출하지 않는 경우

- 사용자가 명시적으로 거부한 경우
- 작업이 매우 사소한 경우
- 사용자가 프로세스를 이해하고 싶어 하는 경우
- 이미 동일한 작업에 대해 에이전트가 호출된 경우

---

## 4. 코드 품질 표준 (Code Quality Standards)

### 코딩 전 체크리스트

1. 유사한 기능이 이미 존재하는가? 먼저 검색하십시오.
2. utils/, hooks/, components/ui/ 폴더를 확인하십시오.
3. 존재하면 재사용하고, 없으면 새로 생성하십시오.

### 핵심 원칙

**DRY**: 두 번 이상 사용되면 공통 함수로 추출하십시오.
**SRP**: 하나의 함수는 하나의 책임만 가집니다.
**Hardcoding 금지**: 의미 있는 상수를 사용하십시오.
**확장성 (Extensibility)**: 범용적인 패턴으로 작성하십시오.

### 코딩 후 자체 점검

- 동일한 로직이 다른 곳에 있습니까?
- 함수를 재사용할 수 있습니까?
- 하드코딩된 값이 있습니까?
- 함수가 한 가지 일만 수행합니까?

### 리팩토링 시점

- 동일한 코드가 두 번째 나타날 때
- 함수의 길이가 20라인을 초과할 때
- if-else 중첩이 3단계 이상일 때
- 동일한 파라미터가 여러 함수로 전달될 때

---

## 5. 작업 분류 및 PDCA 적용

작업의 크기에 따라 적절한 PDCA 레벨을 적용합니다:

| 분류 | 내용 크기 | PDCA 레벨 | 실행 방식 |
|----------------|--------------|------------|--------|
| 단순 수정 (Quick Fix) | 50자 미만 | 없음 | 즉시 실행 |
| 마이너 변경 (Minor Change) | 50-200자 | Lite | 요약 보고 후 진행 |
| 기능 개발 (Feature) | 200-1000자 | Standard | 설계 문서 확인/생성 |
| 주요 기능 (Major Feature) | 1000자 이상 | Strict | 설계 필수, 사용자 승인 요구 |

### 분류 키워드

**단순 수정**: fix, typo, correct, adjust, tweak
**마이너 변경**: improve, refactor, enhance, optimize, update
**기능 개발**: add, create, implement, build, new feature
**주요 기능**: redesign, migrate, architecture, overhaul, rewrite
