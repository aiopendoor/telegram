# Telegram Refiner RAG Pipeline - 상세 설계 문서

> **Summary**: RAG 기반 맥락 인식 텔레그램 정제 시스템 - 의미 기반 중복 제거, 지능형 분류, 동적 Obsidian 지식 구조 자동 관리
>
> **Project**: Antigravity - Telegram Refiner v3.0 (RAG Pipeline)
> **Version**: 3.0.0
> **Author**: AI Assistant + Pro
> **Date**: 2026-02-22
> **Status**: Design Approved

---

## 📋 목차

1. [설계 배경 및 문제 인식](#1-설계-배경-및-문제-인식)
2. [전체 아키텍처](#2-전체-아키텍처)
3. [Obsidian 지식 구조 설계](#3-obsidian-지식-구조-설계)
4. [핵심 컴포넌트 상세](#4-핵심-컴포넌트-상세)
5. [데이터 흐름](#5-데이터-흐름)
6. [에러 처리 전략](#6-에러-처리-전략)
7. [성공 기준 및 테스트](#7-성공-기준-및-테스트)
8. [Obsidian 제2의 뇌 활용법](#8-obsidian-제2의-뇌-활용법)
9. [향후 확장 계획](#9-향후-확장-계획)
10. [기술 스택](#10-기술-스택)

---

## 1. 설계 배경 및 문제 인식

### 1.1 기존 시스템의 한계 (v2.0)

**데이터 품질 문제 (우선순위: 중복 > 분류 > 엔티티 > 노이즈)**
1. **중복 콘텐츠** (최고 우선순위): 같은 뉴스가 다른 표현으로 여러 번 저장됨
2. **분류 불일치**: 비슷한 내용이 다른 카테고리로 분산
3. **엔티티 추출 부실**: 중요한 고유명사 누락 또는 오추출
4. **노이즈 필터링 미흡**: 광고, 스팸성 메시지 유입

**처리 인텔리전스 문제**
1. **LLM 정확도 저하**: 환각, 잘못된 요약, 핵심 정보 누락
2. **맥락 손실**: 각 메시지를 독립적으로 처리하여 대화 흐름 파악 불가

**저장소 구조 문제**
1. **검색 어려움**: 관련 노트를 찾기 힘듦, 자동 링크 없음
2. **경직된 분류**: 고정된 폴더 구조로 유연성 부족
3. **중복 처리 전략 부재**: 발견된 중복을 어떻게 처리할지 미정의
4. **메타데이터 부족**: 현재 YAML 필드로는 고도화된 검색/분석 불가
5. **동기화 충돌**: Obsidian↔Supabase 불일치 발생

### 1.2 설계 목표

**핵심 철학**: "맥락을 기억하는 지능형 사서 (Context-Aware Librarian)"

1. **의미 기반 중복 제거**: 벡터 검색으로 "같은 내용"을 정확히 감지
2. **맥락 인식 처리**: 과거 대화, 관련 주제, 엔티티 이력을 고려한 LLM 분석
3. **동적 지식 구조**: AI가 자율적으로 폴더 계층을 생성/관리
4. **Obsidian 제2의 뇌**: Google Drive 동기화로 모바일/PC 크로스플랫폼 활용
5. **단일 진실 공급원**: Supabase 중심, Obsidian은 동기화된 뷰 레이어

---

## 2. 전체 아키텍처

### 2.1 시스템 구조

```
Telegram 메시지 (@opendoorai)
  ↓
┌─────────────────────────────────────┐
│ 1. Preprocessor                     │
│  - 텍스트 정제                       │
│  - 임베딩 생성 (768차원)             │
└──────────┬──────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ 2. Deduplicator (Vector DB)         │
│  - 유사도 > 0.88 → 중복              │
│  ├─ [중복] → 병합 로직               │
│  └─ [신규] → 계속 진행               │
└──────────┬──────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ 3. Context Retriever (RAG)          │
│  - 유사 과거 메시지 (0.75~0.87)     │
│  - 동일 엔티티 이력                  │
│  - 대화 스레드 재구성                │
└──────────┬──────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ 4. LLM Processor (맥락 인식)         │
│  입력: 메시지 + 맥락                 │
│  출력: Area, 요약, 엔티티, 태그      │
└──────────┬──────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ 5. Taxonomy Agent (AI 폴더 배치)    │
│  - Area 결정 (21~30)                │
│  - 하위 구조 분석 및 생성            │
└──────────┬──────────────────────────┘
           ↓
           ├──────────────────┐
           ↓                  ↓
┌──────────────────┐  ┌──────────────────┐
│ 6. Supabase      │  │ 7. Obsidian      │
│    Writer        │  │    Syncer        │
│                  │  │                  │
│ Source of Truth  │──▶│   View Layer     │
│ • notes 테이블   │  │ • Google Drive   │
│ • 벡터 저장      │  │ • .md 파일       │
└──────────────────┘  └──────────────────┘
                               ↓
                      ┌──────────────────┐
                      │ Obsidian App     │
                      │ (PC + Mobile)    │
                      │  제2의 뇌 활용    │
                      └──────────────────┘
```

### 2.2 핵심 컴포넌트

**인프라**
- **Vector DB**: Qdrant 또는 Chroma
- **Embedding**: OpenAI `text-embedding-3-small` 또는 Ollama
- **LLM**: Claude/Gemini 또는 Ollama
- **Storage**: Supabase (메인) + Obsidian (뷰)

**처리 파이프라인**
1. `telegram_fetcher.py` - 메시지 수집
2. `preprocessor.py` - 전처리 & 벡터화
3. `deduplicator.py` - 중복 검사 엔진
4. `context_retriever.py` - RAG 맥락 검색
5. `llm_processor.py` - 맥락 인식 LLM 분석
6. `taxonomy_agent.py` - AI 자율 폴더 배치 🆕
7. `supabase_writer.py` - DB 저장
8. `obsidian_syncer.py` - Obsidian 동기화

---

## 3. Obsidian 지식 구조 설계

### 3.1 Vault 위치

```
/Users/musuj/Downloads/200_시스템개발/Antigravity/100_Obsidian/
```

**Google Drive 동기화 설정**
- 100_Obsidian 폴더를 Google Drive와 동기화
- PC: Obsidian 데스크톱 앱에서 Vault로 열기
- Mobile: Obsidian 모바일 앱 + Google Drive 연동

### 3.2 10개 Area 구조 (고정)

```
100_Obsidian/
└── 20_Areas/
    ├── 21_Real_Estate/          # 부동산 (주거, 상업용, 토지)
    ├── 22_Finance/              # 금융 자산 (주식, 채권, 코인)
    ├── 23_Alternative_Assets/   # 대체 투자 (미술품, 골드, 수집품)
    ├── 24_Career_Income/        # 커리어와 소득 (연봉협상, 이직)
    ├── 25_Tax_Legal/            # 세금과 법률 (절세, 상속, 증여)
    ├── 26_Economy_Macro/        # 경제와 거시환경 (금리, 정책)
    ├── 27_Life_Planning/        # 인생 설계 (은퇴, 교육비, 보험)
    ├── 28_Psychology_Mindset/   # 투자 심리 (행동경제학, 편향)
    ├── 29_AI_Tech/              # AI와 기술 (자동화, 핀테크)
    └── 30_Society_Culture/      # 사회와 문화 (트렌드, 소비)
```

**Area 철학**
- 자산 직접 관리: 21, 22, 23
- 자산 획득: 24
- 자산 보호: 25
- 환경 분석: 26, 30
- 장기 전략: 27
- 내면 게임: 28
- 생산성: 29

### 3.3 동적 하위 구조 (AI 자율 생성)

**예시: 21_Real_Estate**

```
21_Real_Estate/                    # 고정
├── 거래동향/                       # AI 생성 (중분류)
│   ├── 강남구/                     # AI 생성 (소분류)
│   │   ├── 아파트/                 # AI 생성 (하위주제)
│   │   │   ├── 2026-02-22_래미안_급등.md
│   │   │   └── 2026-02-20_반포자이_거래.md
│   │   └── 오피스텔/
│   ├── 서초구/
│   └── 용산구/
├── 정책_규제/                      # AI 생성 (중분류)
│   ├── 금리정책/
│   └── 대출규제/
└── 시장분석/
    └── 전망_리포트/
```

**폴더 생성 규칙**
- 기존 폴더 유사도 > 0.85 → 재사용
- 새로운 주제 → 신규 폴더 생성
- 폴더명: 한글 + 언더스코어, 2~4단어
- 최대 3단계 깊이

### 3.4 YAML 메타데이터 스키마

```yaml
---
# 기본 정보
id: "doc_20260222_001"
title: "강남 아파트 가격 급등 조짐"
created_at: "2026-02-22T14:30:00Z"
updated_at: "2026-02-22T14:30:00Z"

# 분류
area: "21_Real_Estate"
folder_path: "21_Real_Estate/거래동향/강남구/아파트"
category: "부동산_거래동향"
tags: [강남구, 아파트, 가격상승, 래미안]

# 엔티티
entities:
  locations: [강남구, 대치동]
  organizations: [삼성물산, 한국부동산원]
  keywords: [아파트, 실거래가, 급등]

# 감성 분석
gravity_score: 0.75  # -1.0 ~ +1.0
sentiment: "긍정"
urgency: "높음"

# 중복 관리
is_duplicate: false
similar_notes: []
merged_count: 0

# 맥락 정보
thread_id: "thread_20260222_001"
related_notes: ["[[2026-02-20_금리_인하]]", "[[2026-01-15_강남_시장_전망]]"]

# 출처
source_channel: "@opendoorai"
source_url: "https://t.me/opendoorai/12345"
telegram_message_id: 12345

# 상태
status: "published"
---

# 📌 핵심 요약 (3줄)
- 강남구 대치동 래미안 아파트 실거래가 전월 대비 5% 상승
- 금리 인하 기대감과 학군 수요 증가가 주요 원인
- 전문가들은 단기 조정 후 추가 상승 전망

# 📝 본문
(원문 또는 AI 정제 텍스트)

# 🔗 연결된 노트
- [[2026-02-20_금리_인하]] - 기준금리 인하가 부동산 시장에 미치는 영향
- [[2026-01-15_강남_시장_전망]] - 강남 부동산 시장 2026년 전망

# 💡 인사이트
(사용자가 추가하는 개인 메모)
```

---

## 4. 핵심 컴포넌트 상세

### 4.1 Deduplicator (중복 검사 엔진)

```python
class Deduplicator:
    DUPLICATE_THRESHOLD = 0.88  # 88% 이상 = 중복
    SIMILAR_THRESHOLD = 0.75    # 75~87% = 관련 노트

    def check_duplicate(self, message: str, embedding: list) -> dict:
        """벡터 유사도 기반 중복 검사"""
        results = self.vector_db.search(
            embedding=embedding,
            limit=10,
            filter={"status": {"$in": ["published", "merged"]}}
        )

        # 중복 판정
        for result in results:
            if result.similarity >= self.DUPLICATE_THRESHOLD:
                return {
                    "is_duplicate": True,
                    "action": "merge",
                    "target_note_id": result.id,
                    "similarity": result.similarity
                }

        # 유사 노트 수집
        similar = [r for r in results
                   if self.SIMILAR_THRESHOLD <= r.similarity < self.DUPLICATE_THRESHOLD]

        return {
            "is_duplicate": False,
            "similar_notes": similar
        }
```

### 4.2 Context Retriever (RAG)

```python
class ContextRetriever:
    def get_context(self, message: str, embedding: list, entities: list) -> dict:
        """다차원 맥락 검색"""
        # 1. 의미 유사 메시지
        semantic = self.vector_db.search(
            embedding=embedding,
            limit=10,
            filter={"created_at": {"$gte": "30_days_ago"}}
        )

        # 2. 엔티티 기반 검색
        entity_history = self.db.query(
            "SELECT * FROM notes WHERE entities @> $1 LIMIT 10",
            entities
        )

        # 3. 스레드 재구성
        thread_id = self.detect_thread(message, semantic)
        thread = self.db.query(
            "SELECT * FROM notes WHERE thread_id = $1 ORDER BY created_at",
            thread_id
        )

        return {
            "related_notes": semantic[:5],
            "entity_history": entity_history[:5],
            "thread_context": thread,
            "thread_id": thread_id
        }
```

### 4.3 Taxonomy Agent (AI 폴더 배치)

```python
class TaxonomyAgent:
    def determine_path(self, content: dict, area: str) -> dict:
        """AI가 최적 폴더 경로 결정"""
        # 1. 현재 구조 로드
        current_structure = self.load_folder_tree(area)

        # 2. 폴더 임베딩 유사도 계산
        folder_embeddings = self.get_folder_embeddings(area)
        similarities = self.calculate_similarities(
            content['embedding'], folder_embeddings
        )

        # 3. LLM 결정
        decision = self.llm.analyze(
            prompt=f"""
            현재 폴더 구조: {current_structure}
            유사도: {similarities}

            새 노트:
            - 제목: {content['title']}
            - 요약: {content['summary']}
            - 엔티티: {content['entities']}

            최적 경로를 JSON으로:
            {{"path": "21_Real_Estate/거래동향/강남구",
              "created_folders": [],
              "reasoning": "..."}}
            """,
            response_format="json"
        )

        # 4. 폴더 생성
        self.create_folders_if_needed(decision.created_folders)
        return decision
```

### 4.4 LLM Processor (맥락 인식)

```python
class LLMProcessor:
    def process_with_context(self, message: str, context: dict) -> dict:
        """맥락 포함 LLM 처리"""
        prompt = f"""
        # 현재 메시지
        {message}

        # 관련 과거 맥락 (최근 30일)
        {context['related_notes']}

        # 동일 엔티티 이력
        {context['entity_history']}

        # 대화 스레드
        {context['thread_context']}

        ---
        위 맥락을 고려하여 JSON 추출:
        1. Area (21~30)
        2. 중분류/소분류
        3. 엔티티 (locations, organizations, keywords)
        4. 3줄 요약
        5. Gravity Score (-1.0 ~ +1.0)
        6. 태그 5개
        7. 관련 노트 링크 제안
        """

        return self.llm.extract(prompt, response_format="json")
```

---

## 5. 데이터 흐름

### 5.1 정상 처리 흐름

```
메시지 수신 → 전처리 & 벡터화 → 중복 체크
  ├─ [중복] → 기존 노트 병합 → 종료
  └─ [신규] → 맥락 검색 → LLM 처리 → 폴더 배치
                            → Supabase 저장 → Obsidian 동기화
```

### 5.2 중복 처리 시나리오

**완전 중복 (유사도 > 0.95)**
```python
action = "skip"  # 새 노트 미생성
update_yaml(existing_note, {
    "merged_count": merged_count + 1,
    "updated_at": now()
})
```

**부분 중복 (0.88 < 유사도 < 0.95)**
```python
action = "merge"
append_to_note(existing_note, f"""
## 📝 업데이트 ({now()})
{new_content}
""")
```

**유사 (0.75 < 유사도 < 0.88)**
```python
action = "create_with_link"
create_new_note(content)
add_related_link(new_note, existing_note)
```

---

## 6. 에러 처리 전략

### 6.1 Fail-Safe 원칙

**시스템은 절대 멈추지 않음**

```python
class RefinementPipeline:
    def process(self, message):
        # 임베딩 실패 → 벡터 검색 스킵
        try:
            embedding = self.embedding_service.create(message.text)
        except:
            embedding = None

        # 중복 검사 실패 → 신규로 간주
        duplicate_info = {"is_duplicate": False}
        if embedding:
            try:
                duplicate_info = self.deduplicator.check(message.text, embedding)
            except:
                pass

        # 맥락 검색 실패 → 맥락 없이 처리
        context = {}
        if embedding:
            try:
                context = self.context_retriever.get(message.text, embedding)
            except:
                pass

        # LLM 처리 (필수)
        try:
            refined_data = self.llm_processor.process(message.text, context)
        except Exception as e:
            self.save_to_error_log(message, str(e))
            raise

        # Supabase 실패해도 Obsidian은 저장
        try:
            self.supabase_writer.write(refined_data)
        except:
            pass
        finally:
            self.obsidian_syncer.write(refined_data)
```

### 6.2 에러 로그

```
100_Obsidian/99_System_Logs/2026-02-22_errors.md
```

---

## 7. 성공 기준 및 테스트

### 7.1 정량적 목표

| 항목 | 목표 |
|------|------|
| 중복 감지율 | > 90% |
| Area 분류 정확도 | > 85% |
| 맥락 검색 관련성 | > 80% |
| 폴더 배치 적절성 | > 80% |
| 시스템 안정성 | > 99% |

### 7.2 Zero Script QA

**Phase 1: 단위 검증**
- 더미 메시지 10개 × 10개 Area
- 동일 내용 변형 3개 → 중복 감지
- 대화 스레드 5개 → 맥락 연결

**Phase 2: 구조 검증**
- 각 Area 20개 메시지
- 폴더 구조 논리성 평가

**Phase 3: 장기 운영**
- 7일 실제 수집
- 일일 에러 모니터링

---

## 8. Obsidian 제2의 뇌 활용법

### 8.1 설정 방법

**1. Obsidian 설치**
- PC: https://obsidian.md 다운로드
- Mobile: App Store/Play Store 설치

**2. Vault 열기**
- "Open folder as vault" 클릭
- `/Users/musuj/.../100_Obsidian` 선택

**3. Google Drive 동기화**
- 100_Obsidian 폴더를 Google Drive와 동기화
- 모바일 Obsidian 앱에서도 동일 폴더 연결

### 8.2 활용 시나리오

**📁 폴더 탐색**
```
20_Areas/21_Real_Estate/거래동향/강남구/
→ 자동 생성된 노트들 시간순 정렬
```

**🔍 강력한 검색**
- 전체 검색: `강남 아파트`
- 태그: `#금리인하`
- 엔티티: `entities:삼성전자`

**🕸️ Graph View**
- 모든 노트 연결 시각화
- 위키링크 네트워크 탐색

**✍️ 개인 메모 추가**
- AI 생성 노트에 인사이트 추가
- 새로운 연결 발견

**📊 대시보드**
```markdown
# 부동산 대시보드
![[2026-02-22_래미안_급등]]
![[2026-02-21_금리_인하]]
```

### 8.3 모바일 활용

- 이동 중 노트 읽기
- 음성 메모 추가
- Google Drive 자동 동기화

---

## 9. 향후 확장 계획

### Phase 1 (현재)
- ✅ RAG 기반 시스템
- ✅ 10개 Area 분류
- ✅ 벡터 중복 제거
- ✅ AI 폴더 관리

### Phase 2 (Q2 2026)
- [ ] 자동 리팩토링
- [ ] 주간 지식 구조 리포트
- [ ] 사용자 피드백 학습

### Phase 3 (Q3 2026)
- [ ] 다국어 지원
- [ ] 이미지/PDF OCR
- [ ] NotebookLM 통합

---

## 10. 기술 스택

### 필수 의존성

```python
# requirements.txt
telethon==1.34.0          # Telegram
python-dotenv==1.0.0      # 환경 변수
qdrant-client==1.7.0      # Vector DB
openai==1.10.0            # Embedding
anthropic==0.18.0         # Claude LLM
supabase-py==2.3.0        # Supabase
```

### 선택적

```python
sentence-transformers==2.3.0  # 로컬 임베딩
ollama-python==0.1.0          # 로컬 LLM
```

---

## 다음 단계

1. ✅ 설계 승인 (2026-02-22)
2. [ ] 구현 계획 수립 (`writing-plans` 스킬)
3. [ ] Vector DB + Deduplicator 구현
4. [ ] Context Retriever 구현
5. [ ] Taxonomy Agent 구현
6. [ ] Obsidian Syncer 구현
7. [ ] 통합 테스트

---

**설계 승인일**: 2026-02-22
**다음 작업**: 구현 계획 수립 (writing-plans 스킬 실행)
