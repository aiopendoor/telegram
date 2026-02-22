---
name: phase-4-api
description: |
  백엔드 API를 설계하고 구현하는 스킬입니다.
  테스트 스크립트 없이 API를 검증하는 제로 스크립트 QA 방법론을 포함합니다.

  백엔드 API 설계나 구현이 필요할 때 선제적으로 사용하십시오.

  Triggers: API design, REST API, backend, endpoint, API 설계, API設計, API设计,
  diseño de API, diseño API, diseño de backend, conception API, conception d'API, backend,
  API-Design, API-Entwurf, Backend, progettazione API, design API, backend

  Do NOT use for: 프론트엔드 전용 프로젝트, 정적 웹사이트 또는 스타터 레벨 프로젝트에는 사용하지 마십시오.
imports:
  - ${PLUGIN_ROOT}/templates/pipeline/phase-4-api.template.md
  - ${PLUGIN_ROOT}/templates/shared/api-patterns.md
  - ${PLUGIN_ROOT}/templates/shared/error-handling-patterns.md
# hooks: Managed by hooks/hooks.json (unified-stop.js) - GitHub #9354 workaround
agent: bkit:qa-monitor
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
user-invocable: false
next-skill: phase-5-design-system
pdca-phase: do
task-template: "[Phase-4] {feature}"
---

# Phase 4: API 설계/구현 + 제로 스크립트 QA

> 백엔드 API 구현 및 스크립트 없는 품질 검증

## 프로젝트 목적

데이터를 저장하고 불러올 수 있는 백엔드 API를 구현합니다. 테스트 코드를 짜는 대신 구조화된 로그를 통해 기능을 검증합니다.

## 이 단계에서 할 일

1. **API 설계**: 엔드포인트(URL), 요청/응답 구조 정의
2. **API 구현**: 실제 백엔드 코드 작성
3. **제스크 QA (Zero Script QA)**: 로그 기반의 기능 검증

## 결과물 (Deliverables)

```
docs/02-design/
└── api-spec.md             # API 명세서

src/api/                    # API 구현 코드
├── routes/
├── controllers/
└── services/

docs/03-analysis/
└── api-qa.md               # QA 결과 보고서
```

---

## 제로 스크립트 QA란?

```
테스트 코드를 작성하는 대신, 구조화된 디버그 로그를 통해 기능을 검증합니다.

[API] POST /api/users
[INPUT] { "email": "test@test.com", "name": "테스트" }
[PROCESS] 이메일 중복 체크 → 통과
[PROCESS] 비밀번호 해싱 → 완료
[PROCESS] DB 저장 → 성공
[OUTPUT] { "id": 1, "email": "test@test.com" }
[RESULT] ✅ 성공

장점:
- 테스트 코드 작성 시간 절약
- 실제 동작 과정을 눈으로 확인 가능
- 디버깅이 매우 용이함
```

---

## RESTful API 설계 원칙

### REST란?
웹 서비스 설계 시 사용하는 아키텍처 스타일로, 자원(Resource)을 중심으로 인터페이스를 설계합니다.

### 주요 설계 규칙

#### 1. 자원 중심의 URL (Noun 위주)
- ✅ 좋음: `GET /users`, `POST /products`
- ❌ 나쁨: `GET /getUsers`, `POST /create-product`

#### 2. HTTP 메서드의 적절한 사용
| 메서드 | 용도 | 설명 |
|--------|---------|------|
| `GET` | 조회 | 데이터를 가져올 때 사용 |
| `POST` | 생성 | 새로운 데이터를 생성할 때 사용 |
| `PUT` | 전체 수정 | 기존 데이터를 완전히 교체할 때 사용 |
| `PATCH` | 부분 수정 | 특정 필드만 수정할 때 사용 |
| `DELETE` | 삭제 | 데이터를 삭제할 때 사용 |

#### 3. 일관된 응답 상태 코드
- `200 OK`: 요청 성공
- `201 Created`: 생성 성공
- `400 Bad Request`: 잘못된 요청 (입력값 오류 등)
- `401 Unauthorized`: 인증 필요
- `404 Not Found`: 존재하지 않는 자원
- `500 Server Error`: 서버 내부 오류

---

## 다음 단계

Phase 5: 디자인 시스템 → API가 준비되었으니, 이제 UI 컴포넌트 구축에 집중합니다.
