---
name: phase-8-review
description: |
  전체 코드베이스 품질과 갭 분석을 확인하는 스킬입니다.
  아키텍처 일관성, 컨벤션 준수 여부, 설계-구현 간 차이 및 잠재적 이슈 탐지를 다룹니다.

  구현이 완료되고 품질 검증이 필요할 때 선제적으로 사용하십시오.

  Triggers: code review, architecture review, quality check, refactoring, gap analysis,
  코드 리뷰, 설계-구현 분석, 코드 검토, 품질 체크, 갭 분석

  Do NOT use for: 초기 개발, 설계 단계 또는 배포 작업에는 사용하지 마십시오.
imports:
  - ${PLUGIN_ROOT}/templates/pipeline/phase-8-review.template.md
# hooks: Managed by hooks/hooks.json (unified-stop.js) - GitHub #9354 workaround
agents:
  default: bkit:code-analyzer
  validate: bkit:design-validator
  gap: bkit:gap-detector
allowed-tools:
  - Read
  - Glob
  - Grep
  - LSP
  - Task
user-invocable: false
next-skill: phase-9-deployment
pdca-phase: check
task-template: "[Phase-8] {feature}"
---

# Phase 8: 아키텍처/컨벤션 리뷰 (Review)

> 전체 코드베이스 품질 검증 단계입니다.

## 프로젝트 목적

배포 전 전체 코드를 검토하여 아키텍처 일관성, 컨벤션 준수 여부 및 잠재적인 이슈를 식별하고 해결합니다.

## 이 단계에서 할 일

1. **아키텍처 리뷰**: 구조적 일관성 검토 (계층 분리 등)
2. **컨벤션 리뷰**: 약속된 코딩 규칙 준수 여부 확인
3. **코드 품질 리뷰**: 중복 코드, 복잡도, 잠재적 버그 탐지
4. **리팩토링**: 발견된 이슈 수정 및 개선

## 결과물 (Deliverables)

```
docs/03-analysis/
├── architecture-review.md      # 아키텍처 리뷰 결과
├── convention-review.md        # 컨벤션 준수 현황
└── refactoring-plan.md         # 개선 및 리팩토링 계획
```

---

## 갭 분석 (Gap Analysis)

### 설계 vs 구현 일치도 확인
Phase 8에서는 **설계 문서(Design)**와 **실제 코드(Implementation)**가 얼마나 일치하는지 분석합니다.

- **Match Rate (일치율)**: 설계된 기능 중 실제 구현된 비율
- **Gap 항목**: 구현되지 않았거나, 설계에 없는데 추가된 항목 식별

### 계층 분리 원칙 점검 (Clean Architecture)
```
[Presentation] ─→ [Application] ─→ [Domain]
       │               │             │
       └─────── [Infrastructure] ────┘
```
- 의존성 방향이 외부에서 내부로 향하는지 확인합니다.
- 내부 계층이 외부 계층(라이브러리 등)에 의존하고 있지 않은지 점검합니다.

---

## 리뷰 체크리스트 요약

- [ ] 명명 규칙(Naming)이 Phase 2 규칙과 일치하는가?
- [ ] 정해진 폴더 구조를 따르고 있는가?
- [ ] 환경 변수가 규칙(NEXT_PUBLIC_ 등)에 맞게 관리되고 있는가?
- [ ] API 호출이 서비스 계층을 통해 이루어지는가?
- [ ] 중복되는 로직이 3곳 이상 존재하는가? (리팩토링 대상)

---

## 다음 단계

Phase 9: 배포 → 리뷰 및 수정이 완료되었으니, 이제 운영 환경으로 배포를 준비합니다.
