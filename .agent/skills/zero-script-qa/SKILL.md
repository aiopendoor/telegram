---
name: zero-script-qa
description: |
  테스트 스크립트 없이 기능을 검증하는 제로 스크립트 QA 방법론입니다.
  구조화된 JSON 로깅과 실시간 모니터링을 사용하여 검증을 수행합니다.

  사용자가 테스트 스크립트 대신 로그 분석을 통해 기능을 검증해야 할 때 선제적으로 사용하십시오.

  Triggers: zero script qa, log-based testing, docker logs, 제로 스크립트 QA, ゼロ스크립트QA, 零脚本QA,
  QA sin scripts, pruebas basadas en logs, registros de docker,
  QA sans script, tests basés sur les logs, journaux docker,
  skriptloses QA, log-basiertes Testen, Docker-Logs,
  QA senza script, test basati sui log, log docker

  Do NOT use for: 유닛 테스트, 정적 분석 또는 도커 설정이 없는 프로젝트에는 사용하지 마십시오.
context: fork
agent: bkit:qa-monitor
# hooks: Managed by hooks/hooks.json (unified-bash-pre.js, unified-stop.js) - GitHub #9354 workaround
---

# 제로 스크립트 QA (Zero Script QA)

## 개요

제로 스크립트 QA는 별도의 테스트 기능을 구현하거나 테스트 코드를 작성하지 않고, **구조화된 로그(Structured Logs)**와 **실시간 모니터링**을 통해 기능을 검증하는 방법론입니다.

```
기존 방식: 테스트 코드 작성 → 실행 → 결과 확인 → 유지보수
제스크 QA: 로그 기반 인프라 구축 → 실제 UI 사용 → AI 로그 분석 → 자동 이슈 탐지
```

## 핵심 원칙

1. **모든 것을 기록하십시오 (Log Everything)**: 모든 API 호출, 에러, 주요 비즈니스 이벤트를 기록합니다.
2. **구조화된 JSON 로그**: AI가 파싱하기 쉬운 JSON 형식을 사용하고 필드(timestamp, level, request_id 등)를 표준화합니다.
3. **실시간 모니터링**: 로그 스트리밍을 통해 즉시 이슈를 탐지하고 문서화합니다.
4. **Request ID 전파**: 클라이언트에서 시작된 ID가 API, DB까지 동일하게 유지되어 전체 흐름을 추적할 수 있어야 합니다.

---

## 로깅 아키텍처

### JSON 로그 표준 포맷
```json
{
  "timestamp": "2026-01-08T10:30:00.000Z",
  "level": "INFO",
  "service": "api",
  "request_id": "req_abc123",
  "message": "API Request completed",
  "data": {
    "method": "POST",
    "path": "/api/users",
    "status": 200,
    "duration_ms": 45
  }
}
```

### 환경별 로그 레벨 정책
- **Local/Staging**: `DEBUG` (모든 상세 정보 기록 및 QA 수행)
- **Production**: `INFO` (운영 모니터링 위주)

---

## QA 자동화 워크플로우

1. **환경 시작**: `docker compose up` 등으로 개발 환경을 실행합니다.
2. **실시간 모니터링**: Claude가 로그 스트림을 모니터링하기 시작합니다.
3. **수동 UX 테스트**: 사용자가 실제 브라우저에서 기능을 조작합니다.
4. **AI 로그 분석**: Claude가 실시간으로 에러, 성능 저하, 비정상 흐름을 탐지합니다.
5. **이슈 보고서 생성**: 탐지된 문제를 Request ID와 함께 즉시 문서화합니다.

---

## 이슈 탐지 기준 (Thresholds)

| 심각도 | 조건 | 액션 |
|----------|-----------|--------|
| **Critical** | `level: ERROR` 또는 `status: 5xx` | 즉시 보고 |
| **Critical** | 응답 시간 > 3000ms | 즉시 보고 |
| **Warning** | 응답 시간 > 1000ms | 경고 보고 |
| **Info** | Request ID 미전파 | 개선 사항 기록 |

---

## 체크리스트

- [ ] JSON 로그 포맷이 적용되었는가?
- [ ] Request ID가 모든 계층(UI → API → DB)에서 전파되는가?
- [ ] 모든 API 호출이 기록되는가? (200 OK 포함)
- [ ] 실시간 로그 분석이 가능한 환경인가?
