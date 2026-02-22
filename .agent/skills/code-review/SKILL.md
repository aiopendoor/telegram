---
name: code-review
description: |
  코드 품질 분석, 버그 탐지 및 모범 사례 준수 여부를 확인하는 코드 리뷰 스킬입니다.
  실행 가능한 피드백과 함께 종합적인 코드 리뷰를 제공합니다.

  사용자가 코드 리뷰, 품질 체크 또는 버그 탐지를 요청할 때 선제적으로 사용하십시오.

  Triggers: code review, review code, check code, analyze code, bug detection,
  코드 리뷰, 코드 검토, 버그 검사, 코드 리뷰, バグ検出, 코드 리뷰, 코드 리뷰,
  revisión de código, revisar código, detección de errores,
  revue de code, réviser le code, détection de bugs,
  Code-Review, Code überprüfen, Fehlererkennung,
  revisione del codice, rivedere codice, rilevamento bug

  Do NOT use for: 설계 문서 생성, 배포 작업 또는 갭 분석(이 경우 phase-8-review 사용)에는 사용하지 마십시오.
argument-hint: "[file|directory|pr]"
user-invocable: true
agent: bkit:code-analyzer
allowed-tools:
  - Read
  - Glob
  - Grep
  - LSP
  - Task
  - Bash
imports:
  - ${PLUGIN_ROOT}/templates/pipeline/phase-8-review.template.md
next-skill: null
pdca-phase: check
task-template: "[Code-Review] {feature}"
# hooks: Managed by hooks/hooks.json (unified-stop.js) - GitHub #9354 workaround
---

# 코드 리뷰 스킬 (Code Review Skill)

> 코드 품질 분석 및 리뷰 전용 스킬입니다.

## 실행 인자 (Arguments)

| 인자 | 설명 | 예시 |
|----------|-------------|---------|
| `[file]` | 특정 파일 리뷰 | `/code-review src/lib/auth.ts` |
| `[directory]` | 전체 디렉토리 리뷰 | `/code-review src/features/` |
| `[pr]` | Pull Request 리뷰 (PR 번호) | `/code-review pr 123` |

## 리뷰 카테고리 (Review Categories)

### 1. 코드 품질 (Code Quality)
- 중복 코드 탐지
- 함수/파일 복잡도 분석
- 명명 규칙(Naming Convention) 확인
- 타입 안전성(Type Safety) 검증

### 2. 버그 탐지 (Bug Detection)
- 잠재적 버그 패턴 탐지
- Null/Undefined 처리 확인
- 에러 핸들링 검사
- 경계 조건(Boundary Condition) 검증

### 3. 보안 (Security)
- XSS/CSRF 취약점 확인
- SQL Injection 패턴 탐지
- 민감 정보 노출 확인
- 인증/인가 로직 검토

### 4. 성능 (Performance)
- N+1 쿼리 패턴 탐지
- 불필요한 리렌더링 확인
- 메모리 누수 패턴 탐지
- 최적화 기회 식별

## 리뷰 출력 형식 (Output Format)

```
## 코드 리뷰 보고서 (Code Review Report)

### 요약 (Summary)
- 리뷰된 파일 수: N
- 발견된 이슈: N (긴급: N, 주요: N, 일반: N)
- 점수: N/100

### 긴급 이슈 (Critical Issues)
1. [파일:라인] 이슈 설명
   제안: ...

### 주요 이슈 (Major Issues)
...

### 일반 사항 (Minor Issues)
...

### 권장 사항 (Recommendations)
- ...
```

## 에이전트 통합

이 스킬은 심층적인 코드 분석을 위해 `code-analyzer` 에이전트를 호출합니다.

| 에이전트 | 역할 |
|-------|------|
| code-analyzer | 코드 품질, 보안, 성능 분석 수행 |

## 사용 예시 (Usage Examples)

```bash
# 특정 파일 리뷰
/code-review src/lib/auth.ts

# 전체 디렉토리 리뷰
/code-review src/features/user/

# PR 리뷰
/code-review pr 42

# 현재 변경된 사항 리뷰
/code-review staged
```

## 신뢰도 기반 필터링 (Confidence-Based Filtering)

`code-analyzer` 에이전트는 신뢰도 기반 필터링을 사용합니다:

| 신뢰도 | 표시 여부 | 설명 |
|------------|---------|-------------|
| 높음 (90%+) | 항상 표시 | 확실한 이슈 |
| 중간 (70-89%) | 선택적 표시 | 발생 가능성 있는 이슈 |
| 낮음 (<70%) | 숨김 | 불확실한 제안 |

## PDCA 통합

- **단계**: Check (품질 검증)
- **트리거**: 구현 완료 후 자동 제안
- **출력물**: docs/03-analysis/code-review-{날짜}.md
