---
name: enterprise
description: |
  마이크로서비스, 쿠버네티스, 테라폼을 활용한 엔터프라이즈급 시스템 개발 스킬입니다.
  AI 네이티브 방법론과 모노레포 아키텍처 패턴을 포함합니다.
  고트래픽, 고가용성 및 복잡한 아키텍처 요구사항을 처리합니다.

  "init enterprise" 또는 "enterprise init" 명령어로 프로젝트를 시작하십시오.

  사용자가 고트래픽, 마이크로서비스, 사용자 정의 인프라 또는 AI 네이티브 개발 패턴이 필요할 때 선제적으로 사용하십시오.

  Triggers: microservices, kubernetes, terraform, k8s, AWS, monorepo, AI native, 10-day,
  init enterprise, enterprise init,
  마이크로서비스, 모노레포, マイクロサービス, モノレポ, 微服务, 单仓库,
  microservicios, estrategia empresarial, arquitectura, CTO, nativo de IA,
  microservices, stratégie d'entreprise, architecture, CTO, natif IA,
  Microservices, Unternehmensstrategie, Architektur, CTO, KI-nativ,
  microservizi, strategia aziendale, architettura, CTO, AI nativo

  Do NOT use for: 단순한 웹사이트, MVP 또는 인프라 요구사항이 없는 프로젝트에는 사용하지 마십시오.
argument-hint: "[init|guide|help]"
agents:
  default: bkit:enterprise-expert
  infra: bkit:infra-architect
  architecture: bkit:enterprise-expert
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
  - WebSearch
user-invocable: true
imports:
  - ${PLUGIN_ROOT}/templates/design-enterprise.template.md
next-skill: phase-1-schema
pdca-phase: plan
task-template: "[Init-Enterprise] {feature}"
---

# 고급 (Enterprise) 스킬 가이드

## 제공 액션 (Actions)

| 액션 | 설명 | 예시 |
|--------|-------------|---------|
| `init` | 프로젝트 초기화 (/init-enterprise 기능) | `/enterprise init my-platform` |
| `guide` | 개발 가이드 표시 | `/enterprise guide` |
| `help` | MSA/인프라 도움말 | `/enterprise help` |

### init (프로젝트 초기화)
1. Turborepo 모노레포 구조 생성
2. apps/, packages/, services/, infra/ 폴더 구조 구축
3. CLAUDE.md 생성 (엔터프라이즈 프로젝트 레벨 명시)
4. docs/ 5개 카테고리 구조 생성
5. infra/terraform/, infra/k8s/ 기본 템플릿 생성
6. .bkit-memory.json 초기화

### guide (개발 가이드)
- AI 네이티브 10일 개발 사이클 안내
- 마이크로서비스 아키텍처 패턴 가이드
- Phase 1-9 전체 파이프라인 (고급 버전)

### help (인프라 도움말)
- 쿠버네티스 기본 개념 설명
- 테라폼 IaC(Infrastructure as Code) 패턴
- AWS EKS, RDS 설정 가이드

## 기술 스택 (Tech Stack)

```
Frontend:
- Next.js 14+ (Turborepo 모노레포)
- TypeScript
- Tailwind CSS
- TanStack Query / Zustand

Backend:
- Python FastAPI (마이크로서비스)
- PostgreSQL (스키마 분리)
- Redis (캐시, Pub/Sub)
- RabbitMQ / SQS (메시지 큐)

Infrastructure:
- AWS (EKS, RDS, S3, CloudFront)
- Kubernetes (Kustomize)
- Terraform (IaC)
- ArgoCD (GitOps)

CI/CD:
- GitHub Actions
- Docker
```

## 클린 아키텍처 (4-Layer)

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer  (Router)                   │
├─────────────────────────────────────────────────────────┤
│                  Application Layer (Service)             │
├─────────────────────────────────────────────────────────┤
│                    Domain Layer (Entity)                 │
├─────────────────────────────────────────────────────────┤
│                 Infrastructure Layer (Repo)              │
└─────────────────────────────────────────────────────────┘
의존성 방향: 위 → 아래 (Domain Layer는 아무것도 의존하지 않음)
```

## AI 네이티브 개발 (AI Native Development)

### 3대 핵심 원칙
1. **문서 기반 설계 (Document-First)**: 코드 작성 전 설계 문서를 먼저 작성
2. **모노레포 컨텍스트 관리**: AI의 문맥 파악을 위해 모든 코드를 하나의 리포지토리에 보관
3. **PR 기반 협업**: 모든 변경 사항은 Pull Request를 통해 진행

### 10일 개발 패턴 (10-Day Development)
- **1일차**: 아키텍처 설계 (시장 분석 + 시스템 설계)
- **2-3일차**: 코어 구축 (인증, 사용자 + 비즈니스 서비스)
- **4-5일차**: UX 구현 (피드백 반영 → 문서화 → 구현)
- **6-7일차**: QA 진행 (제로 스크립트 QA + 버그 수정)
- **8일차**: 인프라 구축 (Terraform + GitOps)
- **9-10일차**: 프로덕션 배포 (보안 검토 + 정식 배포)

## 모노레포의 장점 (AI 활용 측면)
- AI가 전체 컨텍스트를 한 번에 이해 가능
- 타입 코드의 단일 진실원(SoR) 확보
- 여러 계층에 걸친 원자적(Atomic) 커밋 가능
- 일관된 개발 패턴 강제
