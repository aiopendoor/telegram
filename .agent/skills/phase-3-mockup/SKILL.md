---
name: phase-3-mockup
description: |
  디자이너 없이 UI/UX 트렌드를 반영한 목업을 제작하는 스킬입니다.
  나중에 Next.js 컴포넌트로 변환하기 쉬운 HTML/CSS/JS 프로토타입을 설계합니다.

  구현 전 UI/UX 검증이 필요할 때 선제적으로 사용하십시오.

  Triggers: mockup, prototype, wireframe, UI design, 목업, 모크업, 원형, 原型,
  maqueta, prototipo, diseño UI, maquette, prototype, conception UI,
  Mockup, Prototyp, UI-Design, mockup, prototipo, design UI

  Do NOT use for: 프로덕션 코드, API 개발 또는 기존 컴포넌트 수정 작업에는 사용하지 마십시오.
agent: bkit:pipeline-guide
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - WebSearch
user-invocable: false
imports:
  - ${PLUGIN_ROOT}/templates/pipeline/phase-3-mockup.template.md
next-skill: phase-4-api
pdca-phase: design
task-template: "[Phase-3] {feature}"
---

# Phase 3: 목업 개발 (Mockup Development)

> 디자이너 없이 트렌디한 UI 제작 + Next.js 컴포넌트화 고려

## 프로젝트 목적

실제 구현에 들어가기 전 아이디어를 빠르게 검증합니다. **디자이너가 없더라도** UI/UX 트렌드를 조사하여 고품질의 프로토타입을 만들고, 나중에 Next.js 컴포넌트로 전환하기 쉬운 구조로 설계합니다.

## 이 단계에서 할 일

1. **화면 목업**: HTML/CSS를 이용한 UI 구현
2. **인터랙션**: 기본적인 JavaScript를 이용한 동작 구현
3. **데이터 시뮬레이션**: JSON 파일을 이용한 API 응답 시뮬레이션
4. **기능 검증**: 사용자 흐름(Flow) 테스트

## 결과물 (Deliverables)

```
mockup/
├── pages/          # HTML 페이지
├── styles/         # CSS 스타일
├── scripts/        # JavaScript 로직
└── data/           # JSON 가상 데이터
```

---

## UI/UX 트렌드 조사 방법

### 디자이너 없이 트렌디한 UI 만들기

#### 1. 트렌드 조사 사이트
- **Dribbble**: 디자인 트렌드 및 컬러 팔레트 참고 (dribbble.com)
- **Awwwards**: 수상작들을 통한 최신 웹 트렌드 파악 (awwwards.com)
- **Godly**: 랜딩 페이지 레퍼런스 (godly.website)

#### 2. 2025-2026 UI/UX 트렌드 키워드
- **Bento Grid**: 정보를 격자 형태로 깔끔하게 배치
- **Glassmorphism**: 투명한 유리 느낌의 레이어
- **Micro-interactions**: 사용자 작업에 반응하는 미세한 애니메이션
- **Dark Mode First**: 어두운 테마를 기본으로 고려

---

## Next.js 컴포넌트화를 고려한 설계

### 목업 → 컴포넌트 전환 전략

목업 단계부터 **컴포넌트 단위로 분리**하여 설계하면 Next.js 전환이 훨씬 쉽습니다.

#### 1. 컴포넌트 단위의 HTML 구조 설계
```html
<!-- ✅ 좋음: 컴포넌트 단위로 주석이나 data-component 속성 사용 -->
<!-- Header 컴포넌트 -->
<header data-component="Header">
  <nav>...</nav>
</header>

<!-- Hero 컴포넌트 -->
<section data-component="Hero">
  <h1>...</h1>
</section>
```

#### 2. 컴포넌트별 CSS 분리
- `styles/components/button.css`, `card.css` 처럼 파일을 쪼개어 관리합니다.

#### 3. Props를 고려한 데이터 구조 설계
- JSON 가상 데이터를 만들 때, 나중에 React 컴포넌트의 Props로 들어갈 구조를 미리 생각합니다.

---

## 데이터 시뮬레이션 예시

```json
// mockup/data/products.json
// 이 구조가 Phase 4 API 설계의 기초가 됩니다.
{
  "products": [
    {
      "id": 1,
      "name": "상품명",
      "price": 10000,
      "image": "/images/p1.jpg"
    }
  ]
}
```

---

## 다음 단계

Phase 4: API 설계 및 구현 → 목업 검증이 끝났으니, 이제 실제 데이터를 다룰 백엔드를 구축합니다.
