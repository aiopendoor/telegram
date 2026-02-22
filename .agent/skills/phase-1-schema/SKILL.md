---
name: phase-1-schema
description: |
  프로젝트 전반에서 사용되는 용어와 데이터 구조를 정의하는 스킬입니다.
  도메인 용어, 엔티티, 관계 및 스키마 설계를 다룹니다.

  새 프로젝트를 시작하거나 데이터 구조가 불분명할 때 선제적으로 사용하십시오.

  Triggers: schema, terminology, data model, entity, 스키마, 用語, データモデル, 数据模型,
  esquema, terminología, modelo de datos, schéma, terminologie, modèle de données,
  Schema, Terminologie, Datenmodell, schema, terminologia, modello dati

  Do NOT use for: UI 전용 변경, 배포 작업 또는 스키마가 이미 정의된 경우에는 사용하지 마십시오.
agent: bkit:pipeline-guide
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
user-invocable: false
imports:
  - ${PLUGIN_ROOT}/templates/pipeline/phase-1-schema.template.md
  - ${PLUGIN_ROOT}/templates/shared/naming-conventions.md
next-skill: phase-2-convention
pdca-phase: plan
task-template: "[Phase-1] {feature}"
---

# Phase 1: 스키마/용어 정의 (Schema/Terminology Definition)

> 프로젝트 전반에서 사용되는 용어와 데이터 구조를 정의합니다.

## 프로젝트 목적

프로젝트의 언어를 통일합니다. 모든 팀원(또는 AI)이 동일한 용어를 사용하여 소통하고 데이터 구조를 명확하게 이해하도록 합니다.

## 이 단계에서 할 일

1. **용어 사전 구축 (Glossary)**: 비즈니스 용어와 글로벌 표준 용어를 매핑합니다.
2. **엔티티 식별 (Entities)**: 어떤 "사물"이나 "개념"이 존재하는지 결정합니다.
3. **관계 정의 (Relationships)**: 엔티티 간의 관계를 설정합니다.
4. **스키마 설계 (Schema)**: 실제 데이터 구조를 정의합니다.

## 용어 사전 (Glossary)

### 왜 필요한가요?

**Claude Code에게 매번 비즈니스 용어를 설명하는 것은 번거로운 일입니다.**
용어 사전을 만들어두면 다음과 같은 장점이 있습니다:
- AI가 자동으로 참고하여 문맥을 파악함
- 팀 소통의 일관성 유지
- 새로운 팀원/AI의 온보딩 시간 단축

### 용어 카테고리

| 카테고리 | 설명 | 예시 |
|----------|-------------|---------|
| **비즈니스 용어** | 내부적으로 사용하는 고유 용어 | "캐디" (골프 예약 도우미) |
| **글로벌 표준** | 업계 공통 또는 기술 표준 용어 | "OAuth", "REST API" |
| **매핑** | 비즈니스 ↔ 글로벌 표준 대응 | "회원" = User, "결제" = Payment |

### 용어 사전 템플릿 예시

```markdown
## 비즈니스 용어 (Internal Terms)

| 용어 | 영문명 | 정의 | 글로벌 표준 매핑 |
|------|---------|------------|------------------------|
| 캐디 | Caddy | 골프 라운드 예약을 도와주는 AI 비서 | Booking Assistant |
| 라운드 | Round | 18홀 골프 한 경기 | Session, Booking |
| 그린피 | Green Fee | 골프장 이용료 | Usage Fee |

## 글로벌 표준 (Global Standards)

| 용어 | 정의 | 참고 문헌 |
|------|------------|-----------|
| OAuth 2.0 | 인증 프로토콜 | RFC 6749 |
| REST | API 아키텍처 스타일 | - |
| UUID | 범용 고유 식별자 | RFC 4122 |

## 용어 사용 규칙

1. 코드에서는 **영문**을 사용합니다. (`Caddy`, `Round`)
2. UI/문서에서는 **한글**을 사용합니다. (캐디, 라운드)
3. API 응답은 **글로벌 표준**을 우선합니다. (`booking_assistant`)
```

## 결과물 (Deliverables)

```
docs/01-plan/
├── glossary.md         # 용어 사전 (신규 권장)
│   ├── Business Terms
│   ├── Global Standards
│   └── Mapping Table
├── schema.md           # 데이터 스키마
└── domain-model.md     # 도메인 모델
```

## PDCA 적용

- **Plan**: 필요한 엔티티와 용어가 무엇인지 식별
- **Design**: 스키마 구조 및 관계 설계
- **Do**: 문서 작성
- **Check**: 누락이나 모순이 없는지 검토
- **Act**: 확정 후 Phase 2로 이동

## 다음 단계

Phase 2: 코딩 컨벤션 → 용어가 정의되었으니, 이제 코드 작성 규칙을 정의합니다.
