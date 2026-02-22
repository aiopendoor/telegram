---
name: pdca
description: |
  전체 PDCA 사이클을 관리하기 위한 통합 스킬입니다.
  "plan", "design", "analyze", "report", "status" 키워드에 의해 자동으로 트리거됩니다.
  기존의 개별 /pdca-* 명령어들을 대체합니다.

  사용자가 PDCA 사이클, 계획 수립, 설계 문서, 갭 분석, 반복 개선 또는 완료 보고서를 언급할 때 선제적으로 사용하십시오.

  Triggers: pdca, 계획, 설계, 분석, 검증, 보고서, 반복, 개선, plan, design, analyze,
  check, report, status, next, iterate, gap, 計画, 設計, 分析, 検証, 報告,
  计划, 设计, 分析, 验证, 报告, planificar, diseño, analizar, verificar,
  planifier, conception, analyser, vérifier, rapport,
  planen, Entwurf, analysieren, überprüfen, Bericht,
  pianificare, progettazione, analizzare, verificare, rapporto

  Do NOT use for: PDCA 문맥이 없는 단순 질의, 코드 전용 작업에는 사용하지 마십시오.
argument-hint: "[action] [feature]"
user-invocable: true
agents:
  analyze: bkit:gap-detector
  iterate: bkit:pdca-iterator
  report: bkit:report-generator
  default: null
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
  - TaskCreate
  - TaskUpdate
  - TaskList
  - AskUserQuestion
imports:
  - ${PLUGIN_ROOT}/templates/plan.template.md
  - ${PLUGIN_ROOT}/templates/design.template.md
  - ${PLUGIN_ROOT}/templates/do.template.md
  - ${PLUGIN_ROOT}/templates/analysis.template.md
  - ${PLUGIN_ROOT}/templates/report.template.md
  - ${PLUGIN_ROOT}/templates/iteration-report.template.md
next-skill: null
pdca-phase: null
task-template: "[PDCA] {feature}"
# hooks: Managed by hooks/hooks.json (unified-stop.js) - GitHub #9354 workaround
---

# PDCA 통합 스킬 (Unified Skill)

> PDCA 사이클 전체를 관리하는 통합 스킬입니다. 계획(Plan) → 설계(Design) → 실행(Do) → 검증(Check) → 개선(Act) 흐름을 지원합니다.

## 실행 인자 (Arguments)

| 인자 | 설명 | 예시 |
|----------|-------------|---------|
| `plan [feature]` | 계획 문서(Plan) 생성 | `/pdca plan user-auth` |
| `design [feature]` | 설계 문서(Design) 생성 | `/pdca design user-auth` |
| `do [feature]` | 실행 단계 가이드 (구현 시작) | `/pdca do user-auth` |
| `analyze [feature]` | 갭 분석 실행 (Check 단계) | `/pdca analyze user-auth` |
| `iterate [feature]` | 자동 개선 반복 (Act 단계) | `/pdca iterate user-auth` |
| `report [feature]` | 완료 보고서 생성 | `/pdca report user-auth` |
| `archive [feature]` | 완료된 PDCA 문서 보관 | `/pdca archive user-auth` |
| `status` | 현재 PDCA 상태 표시 | `/pdca status` |
| `next` | 다음 단계 가이드 | `/pdca next` |

## 주요 액션 상세 설명

### 1. 계획 (Plan)
- `docs/01-plan/features/{feature}.plan.md` 생성 또는 수정
- 기능의 범위, 요구사항, 성공 기준을 정의합니다.

### 2. 설계 (Design)
- 계획 문서를 기반으로 `docs/02-design/features/{feature}.design.md` 생성
- 아키텍처, 데이터 모델, API 사양 등을 상세 설계합니다.

### 3. 실행 (Do)
- 설계 문서를 바탕으로 구현 가이드 제공
- 구현 순서 체크리스트 및 필수 구성 요소를 안내합니다.

### 4. 검증 (Check / Analyze)
- **gap-detector 에이전트** 호출
- 설계 문서와 실제 코드 간의 일치율(Match Rate) 계산 및 차이점 분석 리포트 생성

### 5. 개선 (Act / Iterate)
- **pdca-iterator 에이전트** 호출
- 일치율이 90% 미만일 경우 코드를 자동 수정하고 재검증을 반복합니다. (최대 5회)

### 6. 완료 보고 (Report)
- **report-generator 에이전트** 호출
- 전체 과정을 통합하여 `docs/04-report/{feature}.report.md` 에 요약 보고서를 생성합니다.

## 상태 확인 예시 (Status)

```
📊 PDCA 현황
─────────────────────────────
기능명: 사용자-인증 (user-auth)
현재 단계: 검증 (Gap Analysis)
일치율: 85%
반복 횟수: 2/5
─────────────────────────────
[계획] ✅ → [설계] ✅ → [실행] ✅ → [검증] 🔄 → [개선] ⏳
```

## 에이전트 통합 정보

| 액션 | 에이전트 | 역할 |
|--------|-------|------|
| analyze | gap-detector | 설계 대 구현 일치 여부 비교 분석 |
| iterate | pdca-iterator | 코드 자동 수정 및 재검증 수행 |
| report | report-generator | 최종 완료 보고서 생성 및 요약 |
