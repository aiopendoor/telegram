---
name: development-pipeline
description: |
  9단계 개발 파이프라인에 대한 종합적인 가이드입니다.
  개발 순서를 잘 모르거나 처음부터 새로운 프로젝트를 시작할 때 사용하십시오.

  사용자가 개발 순서, 단계, 무엇부터 해야 할지 묻거나 명확한 방향 없이 프로젝트를 시작할 때 선제적으로 사용하십시오.

  Triggers: development pipeline, phase, development order, where to start, what to do first,
  how to begin, new project, 개발 파이프라인, 뭐부터, 어디서부터, 순서, 시작,
  開発パイプライン, 何부터, 어디서부터, 开发流程, 从哪里开始,
  pipeline de desarrollo, fase, orden de desarrollo, por dónde empezar, qué hacer primero,
  pipeline de développement, phase, ordre de développement, par où commencer, que faire d'abord,
  Entwicklungspipeline, Phase, Entwicklungsreihenfolge, wo anfangen, was zuerst tun,
  pipeline di sviluppo, fase, ordine di sviluppo, da 어디서부터 시작, 무엇을 먼저 해야 할지

  Do NOT use for: 이미 진행 중인 구현, 기존 기능 작업 또는 버그 수정에는 사용하지 마십시오.
agent: bkit:pipeline-guide
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - TodoWrite
user-invocable: true
# hooks: Managed by hooks/hooks.json (unified-stop.js handles development-pipeline) - GitHub #9354 workaround
---

# 개발 파이프라인 스킬 (Development Pipeline Skill)

> 9단계 개발 파이프라인에 대한 모든 지식을 포함하고 있습니다.

## 사용 시점

- 사용자가 "개발 경험이 부족하다"고 말할 때
- `/pipeline-*` 명령어를 사용할 때
- "개발을 어떻게 시작하나요?", "순서가 어떻게 되나요?"라고 질문받았을 때
- 처음부터 새로운 프로젝트를 시작할 때

## 선택적 적용 원칙

```
이 스킬은 필수 사항이 아닙니다.

활성화 조건:
- 비개발자/초보 개발자가 개발을 시작할 때
- 사용자가 명시적으로 가이드를 요청할 때
- /pipeline-start 명령어를 사용할 때

비활성화 조건:
- 숙련된 개발자가 "자유롭게 진행"하고 싶어 할 때
- 개발이 아닌 AI 작업(문서화, 분석 등)을 수행할 때
- 기존 프로젝트의 유지보수나 버그 수정을 할 때
```

## 9단계 파이프라인 개요

```
Phase 1: 스키마/용어 정의 (Schema/Terminology) ──→ 데이터 구조 및 도메인 용어 정의
Phase 2: 코딩 컨벤션 (Coding Convention) ────→ 코드 작성 규칙 정의
Phase 3: 목업 개발 (Mockup Development) ───→ HTML/CSS/JS + JSON으로 기능 검증
Phase 4: API 설계 및 구현 (API Design/Impl) ──────→ 백엔드 API + 제로 스크립트 QA
Phase 5: 디자인 시스템 (Design System) ────────→ 컴포넌트 시스템 구축
Phase 6: UI 구현 (UI Implementation) ────→ 실제 UI 구현 및 API 연동
Phase 7: SEO/보안 (SEO/Security) ─────────→ 검색 최적화 및 보안 강화
Phase 8: 리뷰 (Review) ───────────────→ 아키텍처/컨벤션 품질 검증
Phase 9: 배포 (Deployment) ───────────→ 운영 환경 배포
```

## PDCA와의 관계 (핵심 개념)

```
❌ 잘못된 이해: 전체 파이프라인을 PDCA에 매핑
❌ (Plan=Phase1-3, Do=Phase4-6, Check=Phase7-8, Act=Phase9)

✅ 올바른 이해: 각 단계(Phase) 내부에서 PDCA 사이클 실행

Phase N (특정 단계)
├── Plan: 이 단계에서 할 일 계획
├── Design: 이 단계의 상세 설계
├── Do: 실행/구현
├── Check: 검증/리뷰
└── Act: 확정 및 다음 단계로 이동
```

## 레벨별 단계 적용

| 단계 (Phase) | 스타터 (Starter) | 다이내믹 (Dynamic) | 엔터프라이즈 (Enterprise) |
|-------|---------|---------|------------|
| 1. 스키마/용어 | 단순하게 | 상세하게 | 상세하게 |
| 2. 컨벤션 | 기본적인 수준 | 확장된 수준 | 확장된 수준 |
| 3. 목업 | O | O | O |
| 4. API | - | bkend.ai 사용 | 직접 구현 |
| 5. 디자인 시스템 | 선택 사항 | O | O |
| 6. UI + API | 정적 UI | 통합 및 연동 | 통합 및 연동 |
| 7. SEO/보안 | SEO 위주 | O | O |
| 8. 리뷰 | - | O | O |
| 9. 배포 | 정적 호스팅 | Vercel 등 | K8s |

### Starter 레벨 흐름
```
Phase 1 → 2 → 3 → 5(선택) → 6(정적) → 7(SEO) → 9
```

### Dynamic 레벨 흐름
```
Phase 1 → 2 → 3 → 4(bkend.ai) → 5 → 6 → 7 → 8 → 9
```

### Enterprise 레벨 흐름
```
Phase 1 → 2 → 3 → 4(직접 구현) → 5 → 6 → 7 → 8 → 9
```

## 단계별 결과물 요약

| 단계 | 주요 결과물 |
|-------|-----------------|
| 1 | `docs/01-plan/schema.md`, `terminology.md` |
| 2 | `CONVENTIONS.md`, `docs/01-plan/naming.md` |
| 3 | `mockup/` 폴더, `docs/02-design/mockup-spec.md` |
| 4 | `docs/02-design/api-spec.md`, `src/api/` |
| 5 | `components/ui/`, `docs/02-design/design-system.md` |
| 6 | `src/pages/`, `src/features/` |
| 7 | `docs/02-design/seo-spec.md`, `security-spec.md` |
| 8 | `docs/03-analysis/architecture-review.md` |
| 9 | `docs/04-report/deployment-report.md` |

## 관련 스킬

- `phase-1-schema/` ~ `phase-9-deployment/`: 각 단계별 상세 가이드
- `pdca-methodology/`: PDCA 적용 방법
- `starter/`, `dynamic/`, `enterprise/`: 레벨별 특화 지식
