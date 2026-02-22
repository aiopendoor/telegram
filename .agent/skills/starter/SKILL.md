---
name: starter
description: |
  초보자 및 비개발자를 위한 정적 웹 개발 스킬입니다.
  HTML/CSS/JavaScript 및 Next.js App Router 기초를 다룹니다.

  "init starter" 또는 "starter init" 명령어로 프로젝트를 시작하십시오.

  사용자가 초보자이거나 단순한 정적 웹사이트를 구축하고자 할 때 선제적으로 사용하십시오.

  Triggers: static website, portfolio, landing page, HTML CSS, beginner, first website,
  simple web, personal site, init starter, starter init,
  정적 웹, 포트폴리오, 랜딩페이지, 초보자, 첫 웹사이트, 간단한 웹,
  静的サイト, ポートフォリオ, 初心者, 静态网站, 个人网站, 初学者

  Do NOT use for: 백엔드 앱, 인증 기능 또는 데이터베이스가 필요한 프로젝트에는 사용하지 마십시오.
argument-hint: "[init|guide|help]"
agent: bkit:starter-guide
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - WebFetch
user-invocable: true
imports:
  - ${PLUGIN_ROOT}/templates/design-starter.template.md
next-skill: phase-1-schema
pdca-phase: plan
task-template: "[Init-Starter] {feature}"
---

# 초급 (Starter) 스킬 가이드

## 제공 액션 (Actions)

| 액션 | 설명 | 예시 |
|--------|-------------|---------|
| `init` | 프로젝트 초기화 (/init-starter 기능) | `/starter init my-portfolio` |
| `guide` | 개발 가이드 표시 | `/starter guide` |
| `help` | 기초 도움말 | `/starter help` |

### init (프로젝트 초기화)
1. 프로젝트 디렉토리 구조 생성 (HTML/CSS/JS 또는 Next.js 선택 가능)
2. CLAUDE.md 생성 (스타터 프로젝트 레벨 명시)
3. docs/ 폴더 구조 생성 (PDCA 문서용)
4. .bkit-memory.json 초기화

## 권장 대상

- 프로그래밍을 처음 시작하는 분
- 단순한 웹사이트나 포트폴리오 사이트가 필요한 분
- 서버 없이 작동하는 페이지를 만들고 싶은 분

## 기술 스택 (Tech Stack)

### 옵션 A: 순수 HTML/CSS/JS (완전 초보자용)
- **HTML5**: 웹 페이지의 구조 정의
- **CSS3**: 디자인 및 스타일링
- **JavaScript**: 간단한 동작 추가 (선택 사항)

### 옵션 B: Next.js (프레임워크 활용)
- **Next.js 14+**: 현대적인 웹 개발 프레임워크
- **Tailwind CSS**: 디자인을 빠르게 입히는 도구
- **TypeScript**: 안정적인 코드 작성 (선택 사항)

---

## 배포 방법

### GitHub Pages (무료)
1. GitHub 리포지토리 생성 및 코드 푸시
2. Settings → Pages에서 main 브랜치 선택
3. 웹 주소에서 내 사이트 확인 가능

### Vercel (Next.js 추천)
1. vercel.com 계정 생성 (GitHub 연동)
2. 리포지토리 선택 후 "Deploy" 클릭
3. 자동으로 주소가 생성되고 배포 완료

---

## 한계 및 업그레이드 시점

```
❌ 한계점:
- 로그인 및 회원가입 불가 (서버 필요)
- 데이터 영구 저장 불가 (데이터베이스 필요)
- 결제 기능 등 복잡한 비즈니스 로직 불가
```

다음과 같은 경우 **다이내믹 레벨**로 전환하십시오:
- → "로그인 기능이 필요할 때"
- → "사용자 데이터를 저장하고 싶을 때"
- → "관리자 페이지가 필요할 때"
- → "사용자끼리 소통하는 기능이 필요할 때"
