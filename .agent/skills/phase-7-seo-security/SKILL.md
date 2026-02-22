---
name: phase-7-seo-security
description: |
  검색 최적화(SEO) 및 보안을 강화하는 스킬입니다.
  메타 태그, 시맨틱 HTML 및 보안 취약점 점검을 다룹니다.

  검색 순위, 보안 강화 또는 취약점 수정에 대해 질문할 때 선제적으로 사용하십시오.

  Triggers: SEO, security, meta tags, XSS, CSRF, 보안, セキュリティ, 安全,
  seguridad, etiquetas meta, optimización de búsqueda,
  sécurité, balises méta, optimisation pour les moteurs de recherche,
  Sicherheit, Meta-Tags, Suchmaschinenoptimierung,
  sicurezza, tag meta, ottimizzazione per i motori di ricerca

  Do NOT use for: 백엔드 전용 API, 내부 도구 또는 기본 개발 설정에는 사용하지 마십시오.
imports:
  - ${PLUGIN_ROOT}/templates/pipeline/phase-7-seo-security.template.md
agent: bkit:code-analyzer
allowed-tools:
  - Read
  - Edit
  - Glob
  - Grep
  - WebSearch
user-invocable: false
next-skill: phase-8-review
pdca-phase: do
task-template: "[Phase-7] {feature}"
---

# Phase 7: SEO/보안 (SEO/Security)

> 검색 최적화 및 보안 강화 단계입니다.

## 프로젝트 목적

애플리케이션이 검색 엔진에서 잘 발견될 수 있도록 최적화하고, 각종 보안 위협으로부터 시스템을 보호합니다.

## 이 단계에서 할 일

1. **SEO 최적화**: 메타 태그, 구조화된 데이터, 사이트맵(Sitemap) 구축
2. **성능 최적화**: Core Web Vitals 지표 개선 (이미지 최적화 등)
3. **보안 강화**: 인증/인가 강화, 취약점(XSS, CSRF 등) 방어

## 결과물 (Deliverables)

```
docs/02-design/
├── seo-spec.md             # SEO 명세서
└── security-spec.md        # 보안 명세서

src/
├── middleware/             # 보안 미들웨어
└── components/seo/         # SEO 관련 공통 컴포넌트
```

---

## SEO 체크리스트

### 기본 사항
- [ ] 페이지별 Title, Description 설정
- [ ] Open Graph(OG) 메타 태그 설정 (SNS 공유용)
- [ ] Canonical URL 설정 (중복 콘텐츠 방지)
- [ ] robots.txt 및 sitemap.xml 생성

### 성능 및 접근성
- [ ] 이미지 최적화 (Next.js Image 컴포넌트 활용)
- [ ] 웹 폰트 로딩 최적화
- [ ] 시맨틱 HTML 태그 사용 (header, main, nav, section 등)

---

## 보안 체크리스트

### 데이터 보호
- [ ] 입력값 검증 (Server-side Validation 필수)
- [ ] SQL Injection 방어
- [ ] XSS 방어 (HTML 이스케이프 처리)

### 통신 및 인증
- [ ] HTTPS 강제 적용
- [ ] 보안 헤더 설정 (CSP, HSTS, X-Frame-Options 등)
- [ ] 쿠키 보안 설정 (HttpOnly, Secure, SameSite)
- [ ] 민감 정보가 브라우저 로그나 로컬 스토리지에 노출되지 않는지 확인

---

## 다음 단계

Phase 8: 리뷰 → 최적화와 보안 적용이 완료되었으니, 전체 코드 품질을 최종 점검합니다.
