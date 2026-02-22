---
name: phase-9-deployment
description: |
  프로덕션 환경으로 배포하는 스킬입니다.
  CI/CD, 환경 설정 및 배포 전략을 다룹니다.

  사용자가 배포 준비가 되었거나 운영 환경 설정에 대해 물을 때 선제적으로 사용하십시오.

  Triggers: deployment, CI/CD, production, Vercel, Kubernetes, Docker, 배포, デプロイ, 部署,
  despliegue, implementación, producción,
  déploiement, mise en production,
  Bereitstellung, Produktion,
  distribuzione, messa in produzione

  Do NOT use for: 로컬 개발, 설계 단계 또는 기능 구현에는 사용하지 마십시오.
imports:
  - ${PLUGIN_ROOT}/templates/pipeline/phase-9-deployment.template.md
# hooks: Managed by hooks/hooks.json (unified-bash-pre.js, unified-stop.js) - GitHub #9354 workaround
agent: bkit:infra-architect
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
user-invocable: false
next-skill: null
pdca-phase: act
task-template: "[Phase-9] {feature}"
---

# Phase 9: 배포 (Deployment)

> 프로덕션(운영) 환경 배포 단계입니다.

## 프로젝트 목적

개발 및 검증이 완료된 애플리케이션을 실제 사용자에게 서비스하기 위해 배포합니다.

## 이 단계에서 할 일

1. **배포 환경 준비**: 인프라 설정 (Vercel, AWS 등)
2. **빌드 (Build)**: 운영 환경용 결과물 생성
3. **배포 실행**: 실제 서버에 반영
4. **검증**: 배포 후 정상 동작 여부 확인 및 모니터링

## 결과물 (Deliverables)

```
docs/04-report/
└── deployment-report.md        # 배포 결과 보고서

(인프라 설정 파일들)
├── vercel.json                 # Vercel 설정
├── Dockerfile                  # 도커 이미지 설정
└── .github/workflows/          # CI/CD 파이프라인 설정
```

---

## 레벨별 배포 방식

| 레벨 | 배포 방식 및 도구 |
|-------|-------------------|
| **스타터** | 정적 호스팅 (GitHub Pages, Netlify) |
| **다이내믹** | Vercel, Railway, Supabase 등 |
| **엔터프라이즈** | AWS (EKS, ECS), Kubernetes, Docker |

---

## 환경 변수 및 비밀 정보 관리 (Secrets)

### 중요 원칙
- 실제 DB 비밀번호나 API 키와 같은 **민감 정보(Secrets)**는 절대 코드나 Git에 포함해서는 안 됩니다.
- 배포 플랫폼(Vercel, GitHub Actions 등)의 관리 기능을 통해 주입해야 합니다.

### 배포 후 체크리스트
- [ ] HTTPS 접속이 정상적인가?
- [ ] 핵심 기능(로그인, 데이터 저장 등)이 운영 서버에서도 잘 작동하는가?
- [ ] 에러 로그에 배포 관련 이슈가 찍히지 않는가?
- [ ] 성능 저하 현상이 없는가?

---

## 완료 확인

프로젝트의 모든 단계가 완료되었습니다! 새로운 기능 개발이 필요하면 다시 Phase 1부터 개발 사이클을 시작할 수 있습니다.
