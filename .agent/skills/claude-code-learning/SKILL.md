---
name: claude-code-learning
description: |
  Claude Code 학습 및 교육 스킬입니다.
  사용자에게 Claude Code 설정을 구성하고 최적화하는 방법을 가르칩니다.
  모든 프로젝트와 모든 언어에서 작동합니다.

  "learn" 또는 "setup"으로 학습/설정을 시작하십시오.

  사용자가 Claude Code를 처음 사용하거나, 구성에 대해 묻거나,
  Claude Code 설정을 개선하고 싶어 할 때 선제적으로 사용하십시오.

  Triggers: learn claude code, claude code setup, CLAUDE.md, hooks, commands, skills,
  how to configure, 클로드 코드 배우기, 설정 방법, Claude Code 학습,
  クロードコード学習, 设置方法, how do I use claude code,
  aprender claude code, configuración, cómo configurar,
  apprendre claude code, configuration, comment configurer,
  Claude Code lernen, Konfiguration, wie konfigurieren,
  imparare claude code, configurazione, come configurare

  Do NOT use for: 실제 코딩 작업, 디버깅 또는 기능 구현에는 사용하지 마십시오.
argument-hint: "[learn|setup|upgrade] [level]"
agent: claude-code-guide
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
user-invocable: true
imports:
  - ${PLUGIN_ROOT}/templates/shared/naming-conventions.md
next-skill: null
pdca-phase: null
task-template: "[Learn] Claude Code {level}"
# hooks: Managed by hooks/hooks.json (unified-stop.js) - GitHub #9354 workaround
---

# Claude Code 학습 스킬 (Learning Skill)

> Claude Code 설정 및 최적화 마스터하기

## 제공 액션 (Actions)

| 액션 | 설명 | 예시 |
|--------|-------------|---------|
| `learn` | 학습 가이드 시작 | `/claude-code-learning learn 1` |
| `setup` | 설정 자동 생성 | `/claude-code-learning setup` |
| `upgrade` | 최신 기능 가이드 | `/claude-code-learning upgrade` |

### learn [level]

단계별 학습 내용:
- **Level 1**: 기초 - CLAUDE.md 작성법, Plan 모드 사용법
- **Level 2**: 자동화 - 명령어(Commands), 훅(Hooks), 권한 관리
- **Level 3**: 전문화 - 에이전트(Agents), 스킬(Skills), MCP 통합
- **Level 4**: 팀 최적화 - GitHub Action, 팀 규칙 표준화
- **Level 5**: PDCA 방법론 - bkit 방법론 학습

### setup

현재 프로젝트를 분석한 후 적절한 설정을 자동으로 생성합니다:
1. CLAUDE.md 분석 및 생성
2. .claude/ 폴더 구조 확인
3. 필수 구성 파일 제안

### upgrade

최신 Claude Code 기능과 모범 사례(Best Practices)를 안내합니다.

## 학습 단계 (Learning Levels)

### Level 1: 기초 (15분)

```markdown
## CLAUDE.md란 무엇인가요?

팀을 위한 공유 지식 저장소입니다. Claude가 실수를 했을 때,
동일한 실수가 반복되지 않도록 규칙을 추가하십시오.

## 예시

# 개발 워크플로우 (Development Workflow)

## 패키지 관리
- **항상 `pnpm`을 사용하십시오** (`npm`, `yarn` 사용 금지)

## 코딩 컨벤션 (Coding Conventions)
- `interface`보다 `type`을 선호하십시오.
- **`enum`을 절대 사용하지 마십시오** → 문자열 리터럴 유니온(Union) 사용

## 금지 사항
- ❌ console.log 사용 금지 (로거 사용)
- ❌ any 타입 사용 금지
```

### Level 2: 자동화 (30분)

```markdown
## 슬래시 명령어(/)란 무엇인가요?

반복적인 일일 작업을 `/명령어-이름`으로 실행합니다.

## 명령어 위치

.claude/commands/{명령어-이름}.md

## PostToolUse 훅 (Hook)

코드 수정 후 자동 포맷팅 등을 수행합니다.

// .claude/settings.local.json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "pnpm format || true"
      }]
    }]
  }
}
```

### Level 3: 전문화 (45분)

```markdown
## 서브 에이전트(Sub-agents)란 무엇인가요?

특정 작업에 전문화된 AI 에이전트입니다.

## 스킬(Skills)이란 무엇인가요?

도메인별 전문가 컨텍스트입니다. Claude는 관련 작업을 수행할 때 스킬을 자동으로 참조합니다.

## MCP 통합 (Integration)

.mcp.json을 통해 외부 도구(Slack, GitHub, Jira 등)를 연결합니다.
```

### Level 4: 팀 최적화 (1시간)

```markdown
## GitHub Action을 이용한 PR 자동화

PR 코멘트에 @claude를 언급하여 문서를 자동으로 업데이트합니다.

## 팀 규칙 표준화

1. Git으로 CLAUDE.md를 관리합니다.
2. PR 리뷰 중에 규칙을 추가합니다.
3. 팀의 지식을 점진적으로 축적합니다.
```

### Level 5: PDCA 방법론

```markdown
## PDCA란 무엇인가요?

문서 기반 개발 방법론입니다.

계획(Plan) → 설계(Design) → 실행(Do) → 검증(Check) → 개선(Act)

## 폴더 구조

docs/
├── 01-plan/      # 계획
├── 02-design/    # 설계
├── 03-analysis/  # 분석(검증)
└── 04-report/    # 보고서(결과)

## 더 배우기

/pdca 스킬을 사용하여 PDCA 방법론을 학습하십시오.
```

## 출력 형식

```
📚 Claude Code 학습 완료!

**현재 레벨**: {level}
**학습 내용**: {요약}

🎯 다음 단계:
- /claude-code-learning learn {다음_레벨} 로 계속 학습하기
- /claude-code-learning setup 으로 설정 자동 생성하기
- /claude-code-learning upgrade 로 최신 트렌드 확인하기
```

## 현재 설정 분석 대상

분석할 파일:
- CLAUDE.md (루트)
- .claude/settings.local.json
- .claude/commands/
- .claude/agents/
- .claude/skills/
- .mcp.json
