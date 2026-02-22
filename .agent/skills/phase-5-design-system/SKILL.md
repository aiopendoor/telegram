---
name: phase-5-design-system
description: |
  플랫폼에 독립적인 디자인 시스템을 구축하는 스킬입니다.
  모든 UI 프레임워크를 위한 일관된 컴포넌트 라이브러리를 개발합니다.

  일관된 UI 컴포넌트가 필요하거나 디자인 토큰을 언급할 때 선제적으로 사용하십시오.

  Triggers: design system, component library, design tokens, shadcn, 디자인 시스템, デザインシステム, 设计系统,
  sistema de diseño, biblioteca de componentes, tokens de diseño,
  système de design, bibliothèque de composants, jetons de design,
  Design-System, Komponentenbibliothek, Design-Tokens,
  sistema di design, libreria di componenti, token di design

  Do NOT use for: 일회성 UI 변경, 백엔드 개발 또는 단순한 정적 사이트에는 사용하지 마십시오.
imports:
  - ${PLUGIN_ROOT}/templates/pipeline/phase-5-design-system.template.md
# hooks: Managed by hooks/hooks.json (unified-write-post.js, unified-stop.js) - GitHub #9354 workaround
agent: bkit:pipeline-guide
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
user-invocable: false
next-skill: phase-6-ui-integration
pdca-phase: do
task-template: "[Phase-5] {feature}"
---

# Phase 5: 디자인 시스템 (Design System)

> 플랫폼 독립적인 디자인 시스템 구축

## 프로젝트 목적

재사용 가능한 UI 컴포넌트 라이브러리를 구축합니다. 이를 통해 일관된 디자인을 유지하고 개발 속도를 높일 수 있습니다.

---

## 디자인 시스템이란?

### 정의
디자인 시스템은 **재사용 가능한 컴포넌트와 명확한 표준의 집합**으로, 대규모 프로젝트에서도 일관된 사용자 경험을 제공할 수 있게 합니다.

### 디자인 시스템의 3개 계층
1. **디자인 토큰 (Design Tokens)**: 색상, 타이포그래피, 간격, 그림자 등 최소 단위 규칙
2. **핵심 컴포넌트 (Core Components)**: 버튼, 입력창, 카드, 배지 등 독립된 기능 단위
3. **복합 컴포넌트 (Composite Components)**: 폼, 데이터 테이블, 네비게이션 등 핵심 컴포넌트의 조합

---

## 이 단계에서 할 일

1. **기본 컴포넌트 설치**: Button, Input, Card 등 필수 요소 설치
2. **커스터마이징 (Customize)**: 프로젝트 고유 스타일 반영
3. **복합 컴포넌트 제작**: 여러 기본 컴포넌트를 조합하여 복잡한 UI 제작
4. **문서화 (Documentation)**: 컴포넌트 사용법 및 디자인 규칙 기록

## 결과물 (Deliverables)

```
components/
└── ui/                     # 기본 UI 컴포넌트 (shadcn/ui 등)
    ├── button.tsx
    ├── input.tsx
    └── ...

docs/02-design/
└── design-system.md        # 디자인 시스템 명세서
```

---

## shadcn/ui 활용 (웹 기준)

```bash
# 초기 설정
npx shadcn@latest init

# 컴포넌트 추가
npx shadcn@latest add button
npx shadcn@latest add input
npx shadcn@latest add card
```

### 디자인 토큰 관리 예시 (globals.css)

```css
:root {
  --primary: 221.2 83.2% 53.3%;  /* 브랜드 메인 색상 */
  --radius: 0.5rem;             /* 기본 둥글기 */
  --font-sans: 'Pretendard';    /* 본문 폰트 */
}
```

---

## 프로젝트 레벨별 적용

| 레벨 | 적용 방식 |
|-------|-------------------|
| 스타터 | 선택 사항 (간단한 프로젝트는 생략 가능) |
| 다이내믹 | 필수 요소 |
| 엔터프라이즈 | 필수 요소 (디자인 토큰 시스템 포함) |

---

## 다음 단계

Phase 6: UI 구현 + API 연동 → 컴포넌트가 준비되었으니, 이제 실제 화면을 구현하고 데이터를 연결합니다.
