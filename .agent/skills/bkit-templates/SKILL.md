---
name: bkit-templates
description: |
  일관된 문서화를 위한 PDCA 문서 템플릿입니다.
  올바른 구조를 갖춘 계획(Plan), 설계(Design), 분석(Analysis), 보고서(Report) 템플릿을 제공합니다.

  일관된 형식을 보장하기 위해 PDCA 문서를 생성할 때 선제적으로 사용하십시오.

  Triggers: template, plan document, design document, analysis document, report,
  템플릿, 계획서, 설계서, 분석서, 보고서, テンプレート, 計画書, 設計書, 模板, 计划书, 设计书,
  plantilla, documento de plan, documento de diseño, documento de análisis, informe,
  modèle, document de plan, document de conception, document d'analyse, rapport,
  Vorlage, Plandokument, Designdokument, Analysedokument, Bericht,
  modello, documento di piano, documento di progettazione, documento di analisi, rapporto

  Do NOT use for: 코드 구현, 배포 또는 비문서화 작업에는 사용하지 마십시오.
---

# bkit 문서 템플릿 (Document Templates)

> PDCA 문서를 생성할 때 이 템플릿들을 사용하십시오.

## 사용 가능한 템플릿

| 템플릿 | 경로 | 목적 |
|----------|------|---------|
| 계획 (Plan) | `${CLAUDE_PLUGIN_ROOT}/templates/plan.template.md` | 기능 기획 및 범위 설정 |
| 설계 (Design) | `${CLAUDE_PLUGIN_ROOT}/templates/design.template.md` | 기술적 설계 및 상세 사양 |
| 분석 (Analysis) | `${CLAUDE_PLUGIN_ROOT}/templates/analysis.template.md` | 설계와 구현 간의 갭 분석 |
| 보고서 (Report) | `${CLAUDE_PLUGIN_ROOT}/templates/report.template.md` | 작업 완료 및 레슨 런드 보고 |
| 인덱스 (Index) | `${CLAUDE_PLUGIN_ROOT}/templates/_INDEX.template.md` | 문서 목록 관리 |
| CLAUDE | `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.template.md` | CLAUDE.md 초기 설정용 |

## 템플릿 사용 방법

### 계획 (Plan) 템플릿
**P**lan 단계에 사용 - 설계 전 기능 기획 단계.

주요 섹션:
- 개요 및 목적 (Overview & Purpose)
- 범위 (Scope)
- 요구 사항 (Functional/Non-Functional)
- 성공 기준 (Success Criteria)
- 리스크 및 대응 방안 (Risks & Mitigation)

### 설계 (Design) 템플릿
**D**o (설계) 단계에 사용 - 구현 전 기술적 설계 단계.

주요 섹션:
- 아키텍처 (다이어그램, 데이터 흐름)
- 데이터 모델 (엔티티, 관계)
- API 사양 (엔드포인트, 요청/응답)
- UI/UX 디자인 (레이아웃, 컴포넌트)
- 에러 처리 (Error Handling)
- 보안 고려 사항
- 테스트 계획
- 구현 가이드

### 분석 (Analysis) 템플릿
**C**heck 단계에 사용 - 설계와 실제 구현 사이의 차이 분석.

주요 섹션:
- 설계 대비 구현 비교
- 누락된 기능
- 불일치 사항
- 품질 지표
- 권장 개선 사항

### 보고서 (Report) 템플릿
**A**ct 단계에 사용 - 완료 보고 및 학습 내용 요약.

주요 섹션:
- 완료된 작업 요약
- 지표 (코드 라인 수, 테스트 커버리지 등)
- 발생했던 문제점
- 학습한 내용 (Lessons Learned)
- 향후 개선 사항

## 전체 문서 출력 경로

```
docs/
├── 01-plan/
│   └── features/
│       └── {feature}.plan.md
├── 02-design/
│   └── features/
│       └── {feature}.design.md
├── 03-analysis/
│   └── features/
│       └── {feature}.analysis.md
└── 04-report/
    └── features/
        └── {feature}.report.md
```

## 변수 치환

템플릿은 `{variable}` 구문을 사용합니다:
- `{feature}`: 기능 이름
- `{date}`: 생성 날짜 (YYYY-MM-DD)
- `{author}`: 문서 작성자

## 파이프라인 템플릿

개발 파이프라인 단계별 추가 템플릿:
- `${CLAUDE_PLUGIN_ROOT}/templates/pipeline/` 디렉토리에 위치

---

## 문서 표준 (Document Standards)

### 파일 명명 규칙

```
{번호}_{영문_이름}.md      # 01_system_architecture.md
{번호}-{영문_이름}.md      # 01-system-architecture.md
{기능서}.{유형}.md         # login.design.md
```

### 공통 헤더

모든 문서는 다음 내용을 포함해야 합니다:

```markdown
# {문서 제목}

> **요약**: {한 줄 설명}
>
> **작성자**: {이름}
> **생성일**: {YYYY-MM-DD}
> **최종 수정일**: {YYYY-MM-DD}
> **상태**: {Draft | Review | Approved | Deprecated}

---
```

### 버전 관리

문서 내부에서 변경 사항을 추적합니다:

```markdown
## 버전 이력 (Version History)

| 버전 | 날짜 | 변경 사항 | 작성자 |
|---------|------|---------|--------|
| 1.0 | 2024-12-01 | 최초 초안 작성 | 홍길동 |
| 1.1 | 2024-12-05 | API 사양 추가 | 홍길동 |
```

### 상호 참조 (Cross-References)

관련 문서를 링크합니다:

```markdown
## 관련 문서
- 계획: [login.plan.md](../01-plan/features/login.plan.md)
- 설계: [login.design.md](../02-design/features/login.design.md)
- 분석: [login.analysis.md](../03-analysis/features/login.analysis.md)
```

### 상태 추적

각 폴더의 _INDEX.md를 사용하여 상태를 관리합니다:

| 상태 | 의미 | Claude 동작 방식 |
|--------|---------|-----------------|
| ✅ Approved | 승인됨 (참조 가능) | 그대로 따름 |
| 🔄 In Progress | 작성 중 | 변경 사항 통보 |
| ⏸️ On Hold | 일시 중단 | 승인 후 진행 |
| ❌ Deprecated | 폐기됨 | 무시 |

### 충돌 해결

- **코드 vs 설계 불일치**: 코드가 진실이며, 문서 업데이트를 제안하십시오.
- **다중 버전**: 항상 최신 버전만 참조하십시오.
