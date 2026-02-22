---
name: mobile-app
description: |
  크로스 플랫폼 모바일 앱 개발을 위한 가이드입니다.
  React Native, Flutter, Expo 프레임워크를 다룹니다.

  사용자가 모바일 앱을 구축하거나 웹 앱을 모바일로 전환하고자 할 때 선제적으로 사용하십시오.

  Triggers: mobile app, React Native, Flutter, Expo, iOS, Android, 모바일 앱, モバイルアプリ, 移动应用,
  |-- (이하 중략 --|
  aplicación móvil, app móvil, desarrollo móvil,
  application mobile, développement mobile,
  mobile Anwendung, mobile App, mobile Entwicklung,
  applicazione mobile, app mobile, sviluppo mobile

  Do NOT use for: 웹 전용 프로젝트, 백엔드 전용 개발 또는 데스크톱 앱에는 사용하지 마십시오.
agent: bkit:pipeline-guide
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebSearch
user-invocable: false
---

# 모바일 앱 개발 가이드 (Mobile App Development)

## 개요 (Overview)

웹 개발 경험을 바탕으로 모바일 앱을 개발하기 위한 가이드입니다.
크로스 플랫폼 프레임워크를 사용하여 iOS와 Android를 동시에 개발합니다.

---

## 프레임워크 선택 가이드 (Framework Selection)

### 티어별 프레임워크 추천 (v1.3.0)

| 프레임워크 | 티어 (Tier) | 추천도 | 주요 특징 |
|-----------|------|----------------|----------|
| **React Native (Expo)** | Tier 1 | ⭐ 최우선 추천 | TypeScript 생태계, AI 도구 최적화 |
| **React Native CLI** | Tier 1 | 필요 시 추천 | 네이티브 모듈 직접 제어 필요 시 |
| **Flutter** | Tier 2 | 지원 가능 | 6개 OS 지원, 고성능 렌더링 |

> **AI-Native 추천**: React Native + TypeScript
> - Copilot/Claude 완벽 지원
> - 방대한 npm 생태계 활용 가능
> - Dart 대비 압도적인 개발자 풀

> **성능 중심 추천**: Flutter
> - Impeller 렌더링 엔진 탑재
> - 단일 코드베이스로 6개 플랫폼 지원
> - 실행 파일 용량 최적화

### 프로젝트 레벨별 권장 사항

```
Starter (스타터) → Expo (React Native) [Tier 1]
  - 설정이 매우 간단하며 웹 지식 활용도가 높음
  - AI 도구의 지원을 100% 받을 수 있음

Dynamic (다이내믹) → Expo + EAS Build [Tier 1] 또는 Flutter [Tier 2]
  - 서버 연동 및 프로덕션 빌드 지원 포함
  - 멀티 플랫폼 지향 시 Flutter 고려 가능

Enterprise (엔터프라이즈) → React Native CLI [Tier 1] 또는 Flutter [Tier 2]
  - 복잡한 네이티브 기능이나 고도의 성능 최적화 필요 시
  - 일관된 크로스 플랫폼 UI가 핵심일 때 Flutter 추천
```

---

## Expo (React Native) 가이드

### 프로젝트 생성

```bash
# Expo CLI 설치
npm install -g expo-cli

# 새 프로젝트 생성
npx create-expo-app my-app
cd my-app

# 개발 서버 실행
npx expo start
```

### 폴더 구조

```
my-app/
├── app/                    # Expo Router 페이지 (App Router 방식)
│   ├── (tabs)/            # 탭 네비게이션
│   │   ├── index.tsx      # 홈 탭
│   │   ├── explore.tsx    # 탐색 탭
│   │   └── _layout.tsx    # 탭 레이아웃 설정
│   ├── _layout.tsx        # 루트 레이아웃
│   └── +not-found.tsx     # 404 페이지
├── components/            # 재사용 컴포넌트
├── assets/               # 이미지, 폰트 등 에셋
├── app.json              # Expo 설정 파일
└── package.json
```

---

## 웹 vs 모바일 차이점 요약

### UI/UX 구성 요소 차이

| 요소 | 웹 (Web) | 모바일 (Mobile) |
|---------|-----|--------|
| 클릭 | onClick | onPress / onTap |
| 스크롤 | overflow: scroll | ScrollView / FlatList |
| 입력창 | input | TextInput |
| 링크 | a href | Link / Navigation |
| 레이아웃 | div + CSS | View + StyleSheet |

### 네비게이션 방식
- **웹**: URL 기반 (브라우저 뒤로 가기)
- **모바일**: 스택 기반 (화면 쌓기 방식)

### 데이터 저장소
- **웹**: localStorage, Cookie
- **모바일**: AsyncStorage, SecureStore (민감 정보용 필수), SQLite

---

## 모바일 전용 PDCA 체크리스트

### Phase 1: 스키마 (Schema)
- [ ] 오프라인 캐싱이 필요한 데이터 식별
- [ ] 데이터 동기화 충돌 해결 전략 정의

### Phase 3: 목업 (Mockup)
- [ ] iOS/Android 네이티브 UX 가이드 준수 검토
- [ ] 제스처 활용 계획 (스와이프, 핀치 줌 등)
- [ ] 다양한 기기 크기 대응 레이아웃 설계 (Phone, Tablet)

### Phase 6: UI 구현
- [ ] 키보드 처리 (입력 시 화면 가림 방지)
- [ ] Safe Area 처리 (노치 디자인 대응)
- [ ] OS별 UI 차이점 대응

### Phase 9: 배포 (Deployment)
- [ ] 앱스토어 심사 가이드라인 준수 확인
- [ ] 개인정보처리방침 URL 준비
- [ ] 앱 스토어용 스크린샷 및 설명 준비
