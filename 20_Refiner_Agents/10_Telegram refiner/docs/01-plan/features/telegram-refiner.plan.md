# Telegram Refiner (Librarian Agent) Planning Document

> **Summary**: RAG 기반 맥락 인식 텔레그램 정제 시스템 - 의미 기반 중복 제거, 지능형 분류, 동적 Obsidian 지식 구조 자동 관리
>
> **Project**: Antigravity - Telegram Refiner (Librarian Agent)
> **Version**: 3.0.0 (RAG Pipeline)
> **Author**: AI Assistant + Pro
> **Date**: 2026-02-22
> **Status**: Approved - Ready for Implementation

---

## 1. 개요 (Overview)

### 1.1 목적 (Purpose)
- **M2M 콘텐츠 자동화 마스터플랜의 '단계 2'**를 수행하는 핵심 에이전트입니다. `00_Inbox` 혹은 `@opendoorai` 채널에 무작위로 쌓이는 날것의 데이터를 AI 친화적인 Obsidian `.md` 파일(만능 YAML 템플릿 적용)로 정제하여 제2의 뇌 `20_Areas`로 분류/저장합니다.

### 1.2 배경 (Background)
- Collector 에이전트들이 퍼나르는 방대한 데이터 더미에서 **중복 제거**, **카테고리 분류**, **메타데이터(엔티티, 감성 지수 등) 추출**을 자동으로 수행해야 후속 Creator Agent들이 데이터를 읽고 가치 있는 콘텐츠(유튜브/블로그 등)를 생산할 수 있습니다.

---

## 2. 범위 (Scope)

### 2.1 포함 대상 (In Scope) - v3.0 확장
- [x] `@opendoorai` 채널의 과거(`sync_history`) 및 실시간(`sync_batch`) 메시지 파싱
- [x] **RAG 기반 맥락 인식 처리**: 과거 대화, 관련 주제, 엔티티 이력을 고려한 LLM 분석
- [x] **벡터 기반 중복 검사**: 의미적 유사도로 중복 감지 (threshold > 0.88)
- [x] **10개 Area 자동 분류**: 부동산, 금융, 대체투자, 커리어, 세금, 경제, 인생설계, 심리, AI, 사회문화
- [x] **AI 자율 폴더 관리**: Area 하위의 중분류/소분류를 AI가 자동 생성/관리
- [x] 확장된 YAML 메타데이터 (엔티티, 감성, 맥락, 관련 노트 링크)
- [x] **Obsidian 제2의 뇌**: Google Drive 동기화를 통한 모바일/PC 크로스플랫폼 활용
- [x] **Supabase + Obsidian 이중 저장**: Supabase는 Source of Truth, Obsidian은 View Layer

### 2.2 제외 대상 (Out of Scope)
- 데이터 수집(원천 채널 -> Inbox): 10_Collector_Agents에서 처리
- 프론트엔드 포스팅 및 콘텐츠 창작: Creator Agent 및 n8n에서 처리

---

## 3. 요구 사항 (Requirements)

### 3.1 기능적 요구 사항 (Functional Requirements)

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-01 | **[파싱]** Inbox의 `🕒 [시간] | 📢 [채널명]\n텍스트` 구조 파싱 | High | Pending |
| FR-02 | **[LLM 분석]** LLM API를 호출하여 카테고리(부동산/금융/IT 등), 키워드, 심리지수, 3줄 요약 도출 | High | Pending |
| FR-03 | **[YAML 생성]** 도출된 정보를 바탕으로 Obsidian 전용 `만능 YAML 템플릿` 포맷의 `.md` 텍스트 렌더링 | High | Pending |
| FR-04 | **[중복/병합]** 벡터/키워드 혹은 단순 채널/날짜 기반 중복을 체크하여 기존 `.md` 파일에 내용 추가 병합 | Medium | Pending |
| FR-05 | **[저장]** 옵시디언 볼트(Vault)의 지정 경로(`20_Areas/...`)로 마크다운 파일 생성 및 쓰기 | High | Pending |

### 3.2 비기능적 요구 사항 (Non-Functional Requirements)

| Category | Criteria | Measurement Method |
|----------|----------|-------------------|
| Reliability | 파싱 실패나 LLM 타임아웃 발생 시 에러 로그 생성 (`99_System_Logs`) | 예외 처리 모니터링 |
| Performance | 일일 수백~수천 개 메시지 처리를 위한 비동기 처리 및 로컬 모델(Ollama) 활용 고려 | 실행 속도 및 LLM 토큰 비용 |

---

## 4. 아키텍처 및 구현 방식 (Architecture Considerations)

### 4.1 핵심 프로세스 (v3.0 - RAG Pipeline)
1. **Fetch:** Telegram 메시지 수집 (체크포인트 기반)
2. **Preprocess & Vectorize:** 텍스트 정제 + 임베딩 생성 (768차원 벡터)
3. **Deduplication (Vector DB):** 의미 유사도 > 0.88이면 중복 판정 → 병합
4. **Context Retrieval (RAG):**
   - 유사 과거 메시지 검색 (0.75~0.87)
   - 동일 엔티티 이력 조회
   - 대화 스레드 재구성
5. **LLM Processing (맥락 인식):**
   - 입력: 현재 메시지 + 과거 맥락
   - 출력: Area(21~30), 중분류/소분류, 요약, 엔티티, 태그, Gravity Score, 관련 노트 링크
6. **Taxonomy Agent (AI 자율 폴더 배치):**
   - 현재 폴더 구조 분석
   - 최적 경로 결정
   - 필요시 신규 폴더 생성
7. **Supabase Write:** Source of Truth에 저장 (원문, 메타데이터, 벡터)
8. **Obsidian Sync:** Google Drive 연동 폴더에 .md 파일 생성
   ```yaml
   ---
   id: "doc_20260222_001"
   title: "강남 아파트 가격 급등 조짐"
   area: "21_Real_Estate"
   folder_path: "21_Real_Estate/거래동향/강남구/아파트"
   tags: [강남구, 아파트, 가격상승]
   entities:
     locations: [강남구, 대치동]
     organizations: [삼성물산]
   gravity_score: 0.75
   related_notes: ["[[2026-02-20_금리_인하]]"]
   source_url: "https://t.me/opendoorai/12345"
   ---

   # 📌 핵심 요약 (3줄)
   ...

   # 🔗 연결된 노트
   - [[2026-02-20_금리_인하]]
   ```

### 4.2 시스템 고려사항 (Key Decisions)
- 언어/런타임: **Python**
- 폴더 위치: `20_Refiner_Agents/10_Telegram refiner/`
- **Obsidian Vault 위치**: `/Users/musuj/Downloads/200_시스템개발/Antigravity/100_Obsidian/`
- **Google Drive 동기화**: Obsidian 폴더를 Google Drive와 자동 동기화하여 모바일 접근 가능
- **Vector DB**: Qdrant 또는 Chroma (경량, Python 친화적)
- **Embedding**: OpenAI `text-embedding-3-small` 또는 Ollama 로컬 모델
- **LLM**: Claude/Gemini (고정밀) 또는 Ollama (비용 절감)

### 4.3 10개 Area 구조 (고정)
```
20_Areas/
├── 21_Real_Estate/          # 부동산 (주거, 상업용, 토지)
├── 22_Finance/              # 금융 자산 (주식, 채권, 코인)
├── 23_Alternative_Assets/   # 대체 투자 (미술품, 골드, 수집품)
├── 24_Career_Income/        # 커리어와 소득 (연봉협상, 이직, 사업)
├── 25_Tax_Legal/            # 세금과 법률 (절세, 상속, 증여)
├── 26_Economy_Macro/        # 경제와 거시환경 (금리, 정책, 환율)
├── 27_Life_Planning/        # 인생 설계 (은퇴, 교육비, 보험)
├── 28_Psychology_Mindset/   # 투자 심리 (행동경제학, 편향)
├── 29_AI_Tech/              # AI와 기술 (자동화, 핀테크, 생산성)
└── 30_Society_Culture/      # 사회와 문화 (트렌드, 소비패턴)
```

**하위 폴더**: AI가 자율적으로 중분류/소분류/하위주제를 생성 및 관리

---

## 5. 성공 기준 (Success Criteria)

### 5.1 정량적 기준
- [ ] 중복 감지율 > 90% (수동 검증 샘플 100개)
- [ ] Area 분류 정확도 > 85% (수동 검증 샘플 100개)
- [ ] 맥락 검색 관련성 > 80% (사용자 5점 척도 평가)
- [ ] 폴더 배치 적절성 > 80% (사용자 평가)
- [ ] 시스템 안정성 > 99% (에러율 모니터링)

### 5.2 정성적 기준
- [ ] 자동 생성된 노트를 Obsidian에서 열어 제2의 뇌처럼 활용 가능
- [ ] Google Drive 동기화를 통해 모바일에서도 노트 접근 가능
- [ ] Graph View에서 자동 생성된 위키링크 네트워크 시각화 확인
- [ ] AI가 생성한 폴더 구조가 논리적이고 직관적임
- [ ] 중복 노트가 적절히 병합되어 중복 최소화

---

## 6. 주요 변경 사항 (v2.0 → v3.0)

| 항목 | v2.0 (기존) | v3.0 (RAG Pipeline) |
|------|------------|---------------------|
| 중복 감지 | 해시/키워드 기반 | 벡터 유사도 기반 (의미 검색) |
| 처리 방식 | 메시지 독립 처리 | 맥락 인식 (RAG) |
| 분류 체계 | 4개 고정 카테고리 | 10개 Area + AI 자율 하위 구조 |
| 폴더 관리 | 수동 생성 | AI 자동 생성/관리 |
| Obsidian 활용 | 단순 저장 | 제2의 뇌 (Graph View, 위키링크, 크로스플랫폼) |
| 동기화 | Obsidian↔Supabase 별도 | Supabase 중심, Obsidian 뷰 레이어 |

## 7. 다음 단계 (Next Steps)
1. ✅ **계획 승인 완료** (2026-02-22)
2. ✅ **상세 설계 문서 작성**: `docs/02-design/2026-02-22-telegram-refiner-rag-pipeline.design.md`
3. [ ] **구현 계획 수립**: `/pdca plan` 또는 `writing-plans` 스킬 실행
4. [ ] **Phase 1 개발**: Vector DB + Deduplicator
5. [ ] **Phase 2 개발**: Context Retriever (RAG)
6. [ ] **Phase 3 개발**: Taxonomy Agent
7. [ ] **Phase 4 개발**: Obsidian Syncer
8. [ ] **통합 테스트 및 최적화**
