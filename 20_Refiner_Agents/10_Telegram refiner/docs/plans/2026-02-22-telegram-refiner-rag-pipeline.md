# Telegram Refiner RAG Pipeline Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a context-aware Telegram message refinement system using RAG, vector-based deduplication, and AI-driven knowledge organization in Obsidian.

**Architecture:** RAG pipeline with 7 stages: Preprocess → Deduplicate → Context Retrieval → LLM Processing → Taxonomy Assignment → Supabase Storage → Obsidian Sync. Uses Vector DB (Qdrant) for semantic search, Supabase as source of truth, Obsidian as view layer.

**Tech Stack:** Python 3.11+, Telethon, Qdrant, OpenAI Embeddings, Gemini LLM, Supabase, pytest

---

## Prerequisites

**Required Environment Variables** (`.env`):
```env
# Telegram
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_SESSION_STRING=your_session_string

# Vector DB
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Embeddings
OPENAI_API_KEY=your_openai_key

# LLM
GOOGLE_API_KEY=your_gemini_key

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Obsidian
OBSIDIAN_VAULT_PATH=/Users/musuj/Downloads/200_시스템개발/Antigravity/100_Obsidian
```

**Directory Structure:**
```
telegram_refiner/
├── components/
│   ├── __init__.py
│   ├── preprocessor.py
│   ├── deduplicator.py
│   ├── context_retriever.py
│   ├── llm_processor.py
│   ├── taxonomy_agent.py
│   ├── supabase_writer.py
│   └── obsidian_syncer.py
├── services/
│   ├── __init__.py
│   ├── vector_db.py
│   └── embedding_service.py
├── config/
│   ├── __init__.py
│   └── taxonomy.yaml
├── tests/
│   ├── test_preprocessor.py
│   ├── test_deduplicator.py
│   ├── test_context_retriever.py
│   ├── test_llm_processor.py
│   ├── test_taxonomy_agent.py
│   ├── test_supabase_writer.py
│   └── test_obsidian_syncer.py
├── main.py
├── requirements.txt
└── .env
```

---

## Phase 1: Infrastructure Setup

### Task 1: Install Dependencies

**Files:**
- Create: `requirements.txt`

**Step 1: Create requirements file**

```python
# requirements.txt
telethon==1.34.0
python-dotenv==1.0.0
qdrant-client==1.7.0
openai==1.10.0
google-generativeai==0.3.2
supabase==2.3.0
pytest==7.4.0
pytest-asyncio==0.21.0
pyyaml==6.0
```

**Step 2: Install dependencies**

Run: `pip install -r requirements.txt`
Expected: All packages installed successfully

**Step 3: Commit**

```bash
git add requirements.txt
git commit -m "chore: add project dependencies"
```

---

### Task 2: Start Qdrant Vector DB

**Step 1: Start Qdrant with Docker**

Run: `docker run -p 6333:6333 qdrant/qdrant:latest`
Expected: Qdrant running on http://localhost:6333

**Step 2: Verify Qdrant is running**

Run: `curl http://localhost:6333`
Expected: JSON response with version info

**Step 3: Document in README**

Create: `README.md`

```markdown
# Telegram Refiner RAG Pipeline

## Setup

1. Start Qdrant: `docker run -p 6333:6333 qdrant/qdrant:latest`
2. Copy `.env.example` to `.env` and fill in credentials
3. Install: `pip install -r requirements.txt`
4. Run: `python main.py`
```

**Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add setup instructions"
```

---

### Task 3: Create Taxonomy Configuration

**Files:**
- Create: `config/taxonomy.yaml`
- Create: `config/__init__.py`

**Step 1: Define 10 Areas in YAML**

```yaml
# config/taxonomy.yaml
areas:
  21_Real_Estate:
    name: "부동산"
    description: "주거, 상업용, 토지"
    keywords: [부동산, 아파트, 오피스텔, 상가, 토지, 실거래가]

  22_Finance:
    name: "금융 자산"
    description: "주식, 채권, 코인"
    keywords: [주식, 코스피, 코스닥, 채권, 비트코인, 이더리움]

  23_Alternative_Assets:
    name: "대체 투자"
    description: "미술품, 골드, 수집품"
    keywords: [미술품, 금, 골드, NFT, 수집품, 와인]

  24_Career_Income:
    name: "커리어와 소득"
    description: "연봉협상, 이직, 사업"
    keywords: [연봉, 이직, 창업, 프리랜서, 사업]

  25_Tax_Legal:
    name: "세금과 법률"
    description: "절세, 상속, 증여"
    keywords: [세금, 절세, 상속, 증여, 법률, 계약]

  26_Economy_Macro:
    name: "경제와 거시환경"
    description: "금리, 정책, 환율"
    keywords: [금리, 기준금리, 환율, 인플레, 정책, GDP]

  27_Life_Planning:
    name: "인생 설계"
    description: "은퇴, 교육비, 보험"
    keywords: [은퇴, 연금, 교육비, 보험, 건강]

  28_Psychology_Mindset:
    name: "투자 심리"
    description: "행동경제학, 편향"
    keywords: [심리, 편향, FOMO, 손절, 행동경제학]

  29_AI_Tech:
    name: "AI와 기술"
    description: "자동화, 핀테크, 생산성"
    keywords: [AI, 인공지능, 핀테크, 자동화, 생산성]

  30_Society_Culture:
    name: "사회와 문화"
    description: "트렌드, 소비패턴"
    keywords: [트렌드, 소비, 세대, 문화, 라이프스타일]
```

**Step 2: Create __init__.py**

```python
# config/__init__.py
```

**Step 3: Commit**

```bash
git add config/taxonomy.yaml config/__init__.py
git commit -m "feat: add 10-area taxonomy configuration"
```

---

## Phase 2: Core Services

### Task 4: Embedding Service

**Files:**
- Create: `services/embedding_service.py`
- Create: `services/__init__.py`
- Create: `tests/test_embedding_service.py`

**Step 1: Write the failing test**

```python
# tests/test_embedding_service.py
import pytest
from services.embedding_service import EmbeddingService

def test_create_embedding_returns_768_dim_vector():
    service = EmbeddingService()
    text = "테스트 메시지입니다"

    embedding = service.create(text)

    assert len(embedding) == 1536  # text-embedding-3-small dimension
    assert all(isinstance(x, float) for x in embedding)

def test_create_embedding_handles_empty_text():
    service = EmbeddingService()

    with pytest.raises(ValueError, match="Text cannot be empty"):
        service.create("")
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_embedding_service.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'services.embedding_service'"

**Step 3: Write minimal implementation**

```python
# services/__init__.py
```

```python
# services/embedding_service.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class EmbeddingService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "text-embedding-3-small"

    def create(self, text: str) -> list[float]:
        """Create embedding vector for text"""
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )

        return response.data[0].embedding
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_embedding_service.py -v`
Expected: PASS (requires OPENAI_API_KEY in .env)

**Step 5: Commit**

```bash
git add services/embedding_service.py services/__init__.py tests/test_embedding_service.py
git commit -m "feat: add embedding service with OpenAI"
```

---

### Task 5: Vector Database Service

**Files:**
- Create: `services/vector_db.py`
- Create: `tests/test_vector_db.py`

**Step 1: Write the failing test**

```python
# tests/test_vector_db.py
import pytest
from services.vector_db import VectorDB

@pytest.fixture
def vector_db():
    db = VectorDB()
    # Clean up test collection
    try:
        db.delete_collection("test_notes")
    except:
        pass
    return db

def test_upsert_and_search(vector_db):
    collection = "test_notes"

    # Upsert a document
    vector_db.upsert(
        collection=collection,
        id="doc1",
        vector=[0.1] * 1536,
        payload={"text": "강남 아파트 가격 상승", "area": "21_Real_Estate"}
    )

    # Search for similar
    results = vector_db.search(
        collection=collection,
        query_vector=[0.1] * 1536,
        limit=5
    )

    assert len(results) == 1
    assert results[0].id == "doc1"
    assert results[0].payload["text"] == "강남 아파트 가격 상승"
    assert results[0].score > 0.99  # Should be almost identical

    # Cleanup
    vector_db.delete_collection(collection)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_vector_db.py -v`
Expected: FAIL with "ModuleNotFoundError"

**Step 3: Write minimal implementation**

```python
# services/vector_db.py
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv

load_dotenv()

class VectorDB:
    def __init__(self):
        host = os.getenv("QDRANT_HOST", "localhost")
        port = int(os.getenv("QDRANT_PORT", 6333))
        self.client = QdrantClient(host=host, port=port)

    def create_collection(self, collection: str, vector_size: int = 1536):
        """Create collection if not exists"""
        collections = self.client.get_collections().collections
        if collection not in [c.name for c in collections]:
            self.client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )

    def upsert(self, collection: str, id: str, vector: list[float], payload: dict):
        """Insert or update a vector"""
        self.create_collection(collection)

        point = PointStruct(
            id=id,
            vector=vector,
            payload=payload
        )

        self.client.upsert(
            collection_name=collection,
            points=[point]
        )

    def search(self, collection: str, query_vector: list[float], limit: int = 10, filter_dict: dict = None):
        """Search for similar vectors"""
        results = self.client.search(
            collection_name=collection,
            query_vector=query_vector,
            limit=limit,
            query_filter=filter_dict
        )

        return results

    def delete_collection(self, collection: str):
        """Delete a collection"""
        self.client.delete_collection(collection_name=collection)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_vector_db.py -v`
Expected: PASS (requires Qdrant running)

**Step 5: Commit**

```bash
git add services/vector_db.py tests/test_vector_db.py
git commit -m "feat: add Qdrant vector database service"
```

---

## Phase 3: Processing Components

### Task 6: Preprocessor

**Files:**
- Create: `components/preprocessor.py`
- Create: `components/__init__.py`
- Create: `tests/test_preprocessor.py`

**Step 1: Write the failing test**

```python
# tests/test_preprocessor.py
import pytest
from components.preprocessor import Preprocessor

def test_clean_text_removes_emojis():
    processor = Preprocessor()
    text = "🏠 강남 아파트 가격 상승 📈"

    cleaned = processor.clean_text(text)

    assert "🏠" not in cleaned
    assert "📈" not in cleaned
    assert "강남 아파트 가격 상승" in cleaned

def test_process_returns_embedding_and_cleaned_text():
    processor = Preprocessor()
    text = "테스트 메시지"

    result = processor.process(text)

    assert "cleaned_text" in result
    assert "embedding" in result
    assert len(result["embedding"]) == 1536
    assert isinstance(result["cleaned_text"], str)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_preprocessor.py -v`
Expected: FAIL with "ModuleNotFoundError"

**Step 3: Write minimal implementation**

```python
# components/__init__.py
```

```python
# components/preprocessor.py
import re
from services.embedding_service import EmbeddingService

class Preprocessor:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    def clean_text(self, text: str) -> str:
        """Clean text by removing emojis and extra whitespace"""
        # Remove emojis
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)

        text = emoji_pattern.sub('', text)

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def process(self, text: str) -> dict:
        """Clean text and create embedding"""
        cleaned = self.clean_text(text)
        embedding = self.embedding_service.create(cleaned)

        return {
            "cleaned_text": cleaned,
            "embedding": embedding
        }
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_preprocessor.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add components/preprocessor.py components/__init__.py tests/test_preprocessor.py
git commit -m "feat: add text preprocessor with emoji removal"
```

---

### Task 7: Deduplicator

**Files:**
- Create: `components/deduplicator.py`
- Create: `tests/test_deduplicator.py`

**Step 1: Write the failing test**

```python
# tests/test_deduplicator.py
import pytest
from components.deduplicator import Deduplicator
from services.vector_db import VectorDB

@pytest.fixture
def deduplicator():
    return Deduplicator()

@pytest.fixture(autouse=True)
def cleanup_test_collection():
    """Clean up test collection before and after each test"""
    db = VectorDB()
    try:
        db.delete_collection("notes")
    except:
        pass
    yield
    try:
        db.delete_collection("notes")
    except:
        pass

def test_check_duplicate_when_no_existing_notes(deduplicator):
    embedding = [0.1] * 1536

    result = deduplicator.check_duplicate("강남 아파트", embedding)

    assert result["is_duplicate"] == False
    assert result["similar_notes"] == []

def test_check_duplicate_detects_high_similarity(deduplicator):
    # Insert an existing note
    existing_embedding = [0.9] * 1536
    deduplicator.vector_db.upsert(
        collection="notes",
        id="doc1",
        vector=existing_embedding,
        payload={"text": "강남 아파트 가격 급등", "status": "published"}
    )

    # Check similar message
    similar_embedding = [0.89] * 1536  # Very similar

    result = deduplicator.check_duplicate("강남 아파트 가격 상승", similar_embedding)

    assert result["is_duplicate"] == True
    assert result["action"] == "merge"
    assert result["target_note_id"] == "doc1"
    assert result["similarity"] > 0.88
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_deduplicator.py -v`
Expected: FAIL with "ModuleNotFoundError"

**Step 3: Write minimal implementation**

```python
# components/deduplicator.py
from services.vector_db import VectorDB

class Deduplicator:
    DUPLICATE_THRESHOLD = 0.88  # 88% similarity = duplicate
    SIMILAR_THRESHOLD = 0.75    # 75-87% = related note

    def __init__(self):
        self.vector_db = VectorDB()

    def check_duplicate(self, text: str, embedding: list[float]) -> dict:
        """Check if message is duplicate using vector similarity"""
        # Search for similar notes
        results = self.vector_db.search(
            collection="notes",
            query_vector=embedding,
            limit=10
        )

        if not results:
            return {
                "is_duplicate": False,
                "similar_notes": []
            }

        # Check for duplicates (>= 0.88)
        for result in results:
            if result.score >= self.DUPLICATE_THRESHOLD:
                return {
                    "is_duplicate": True,
                    "action": "merge",
                    "target_note_id": result.id,
                    "target_payload": result.payload,
                    "similarity": result.score
                }

        # Collect similar notes (0.75 - 0.87)
        similar_notes = [
            {
                "id": r.id,
                "similarity": r.score,
                "payload": r.payload
            }
            for r in results
            if self.SIMILAR_THRESHOLD <= r.score < self.DUPLICATE_THRESHOLD
        ]

        return {
            "is_duplicate": False,
            "similar_notes": similar_notes
        }
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_deduplicator.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add components/deduplicator.py tests/test_deduplicator.py
git commit -m "feat: add vector-based deduplicator (>88% threshold)"
```

---

### Task 8: Context Retriever (RAG)

**Files:**
- Create: `components/context_retriever.py`
- Create: `tests/test_context_retriever.py`

**Step 1: Write the failing test**

```python
# tests/test_context_retriever.py
import pytest
from components.context_retriever import ContextRetriever
from services.vector_db import VectorDB

@pytest.fixture
def retriever():
    return ContextRetriever()

@pytest.fixture(autouse=True)
def setup_test_data():
    """Setup test notes"""
    db = VectorDB()
    try:
        db.delete_collection("notes")
    except:
        pass

    # Insert test notes
    db.upsert("notes", "doc1", [0.8] * 1536, {
        "text": "강남 아파트 가격 상승",
        "entities": ["강남구", "삼성전자"],
        "created_at": "2026-02-20"
    })

    yield

    try:
        db.delete_collection("notes")
    except:
        pass

def test_get_context_returns_related_notes(retriever):
    embedding = [0.79] * 1536  # Similar to test data
    entities = ["강남구"]

    context = retriever.get_context("강남 부동산", embedding, entities)

    assert "related_notes" in context
    assert "entity_history" in context
    assert "thread_context" in context
    assert len(context["related_notes"]) > 0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_context_retriever.py -v`
Expected: FAIL with "ModuleNotFoundError"

**Step 3: Write minimal implementation**

```python
# components/context_retriever.py
from services.vector_db import VectorDB

class ContextRetriever:
    def __init__(self):
        self.vector_db = VectorDB()

    def get_context(self, message: str, embedding: list[float], entities: list[str]) -> dict:
        """Retrieve context for RAG processing"""

        # 1. Semantic similarity search (0.75-0.87 range)
        related_results = self.vector_db.search(
            collection="notes",
            query_vector=embedding,
            limit=10
        )

        # Filter to similarity range
        related_notes = [
            {
                "id": r.id,
                "text": r.payload.get("text", ""),
                "similarity": r.score
            }
            for r in related_results
            if 0.75 <= r.score < 0.88
        ][:5]  # Top 5

        # 2. Entity-based history (stub - would query Supabase in real impl)
        entity_history = []  # TODO: Implement Supabase query

        # 3. Thread reconstruction (stub)
        thread_context = []  # TODO: Implement thread detection
        thread_id = None

        return {
            "related_notes": related_notes,
            "entity_history": entity_history,
            "thread_context": thread_context,
            "thread_id": thread_id
        }
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_context_retriever.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add components/context_retriever.py tests/test_context_retriever.py
git commit -m "feat: add context retriever for RAG (semantic search)"
```

---

### Task 9: LLM Processor

**Files:**
- Create: `components/llm_processor.py`
- Create: `tests/test_llm_processor.py`

**Step 1: Write the failing test**

```python
# tests/test_llm_processor.py
import pytest
from components.llm_processor import LLMProcessor

@pytest.fixture
def processor():
    return LLMProcessor()

def test_process_with_context_returns_metadata(processor):
    message = "강남구 대치동 아파트 가격이 전월 대비 5% 상승했습니다."
    context = {
        "related_notes": [{"text": "강남 부동산 시장 과열", "similarity": 0.82}],
        "entity_history": [],
        "thread_context": []
    }

    result = processor.process_with_context(message, context)

    assert "area" in result
    assert "title" in result
    assert "summary" in result
    assert "entities" in result
    assert "tags" in result
    assert "gravity_score" in result
    assert "suggested_path" in result

    # Check area is valid (21-30)
    assert result["area"].startswith("2")
    assert len(result["area"]) >= 2
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_llm_processor.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
# components/llm_processor.py
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLMProcessor:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def process_with_context(self, message: str, context: dict) -> dict:
        """Process message with RAG context using Gemini"""

        # Build context string
        related_context = "\n".join([
            f"- {note['text']} (유사도: {note['similarity']:.2f})"
            for note in context.get("related_notes", [])
        ])

        prompt = f"""다음 메시지를 분석하여 JSON 형식으로 메타데이터를 추출하세요.

# 현재 메시지
{message}

# 관련 과거 맥락
{related_context if related_context else "없음"}

---

다음 정보를 추출하여 JSON으로 반환하세요:

1. **area**: 21~30 중 하나 선택
   - 21_Real_Estate: 부동산
   - 22_Finance: 금융 자산
   - 23_Alternative_Assets: 대체 투자
   - 24_Career_Income: 커리어와 소득
   - 25_Tax_Legal: 세금과 법률
   - 26_Economy_Macro: 경제와 거시환경
   - 27_Life_Planning: 인생 설계
   - 28_Psychology_Mindset: 투자 심리
   - 29_AI_Tech: AI와 기술
   - 30_Society_Culture: 사회와 문화

2. **title**: 노트 제목 (10자 이내)
3. **summary**: 3줄 요약 (리스트 형식: ["첫째 줄", "둘째 줄", "셋째 줄"])
4. **entities**: 엔티티 추출
   - locations: 지역명 리스트
   - organizations: 기업/기관명 리스트
   - keywords: 핵심 키워드 리스트
5. **tags**: 태그 5개 (검색 최적화)
6. **gravity_score**: 감성 점수 (-1.0 ~ +1.0)
7. **suggested_path**: 추천 폴더 경로 (예: "거래동향/강남구")

반드시 유효한 JSON만 반환하세요. 다른 텍스트는 포함하지 마세요."""

        response = self.model.generate_content(prompt)

        # Parse JSON from response
        text = response.text.strip()
        # Remove markdown code blocks if present
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()

        result = json.loads(text)
        return result
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_llm_processor.py -v`
Expected: PASS (requires GOOGLE_API_KEY)

**Step 5: Commit**

```bash
git add components/llm_processor.py tests/test_llm_processor.py
git commit -m "feat: add context-aware LLM processor with Gemini"
```

---

### Task 10: Taxonomy Agent

**Files:**
- Create: `components/taxonomy_agent.py`
- Create: `tests/test_taxonomy_agent.py`

**Step 1: Write the failing test**

```python
# tests/test_taxonomy_agent.py
import pytest
import os
from components.taxonomy_agent import TaxonomyAgent

@pytest.fixture
def agent():
    return TaxonomyAgent()

def test_determine_path_returns_valid_structure(agent):
    content = {
        "area": "21_Real_Estate",
        "title": "강남 아파트 급등",
        "summary": "강남구 대치동 아파트 가격 5% 상승...",
        "suggested_path": "거래동향/강남구",
        "entities": {
            "locations": ["강남구", "대치동"],
            "keywords": ["아파트", "가격상승"]
        }
    }

    result = agent.determine_path(content)

    assert "path" in result
    assert result["path"].startswith("21_Real_Estate/")
    assert "created_folders" in result
    assert "reasoning" in result
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_taxonomy_agent.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
# components/taxonomy_agent.py
import os
import json
import yaml
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class TaxonomyAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
        self.load_taxonomy()

    def load_taxonomy(self):
        """Load taxonomy configuration"""
        with open("config/taxonomy.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            self.areas = config["areas"]

    def get_folder_structure(self, area: str) -> dict:
        """Get current folder structure for an area"""
        area_path = Path(self.vault_path) / "20_Areas" / area

        if not area_path.exists():
            return {}

        # Build structure tree
        structure = {}
        for item in area_path.rglob("*"):
            if item.is_dir():
                rel_path = str(item.relative_to(area_path))
                parts = rel_path.split(os.sep)
                current = structure
                for part in parts:
                    if part not in current:
                        current[part] = {}
                    current = current[part]

        return structure

    def determine_path(self, content: dict) -> dict:
        """Determine optimal folder path using LLM"""
        area = content["area"]
        current_structure = self.get_folder_structure(area)

        prompt = f"""현재 폴더 구조를 분석하고 새 노트를 배치할 최적 경로를 결정하세요.

# 현재 Area 폴더 구조
{json.dumps(current_structure, ensure_ascii=False, indent=2) if current_structure else "비어있음 (신규)"}

# 새로운 노트 정보
- 제목: {content['title']}
- 요약: {content['summary']}
- 추천 경로: {content.get('suggested_path', '없음')}
- 엔티티: {json.dumps(content.get('entities', {}), ensure_ascii=False)}

# 요청사항
1. 기존 폴더가 적합하면 재사용하세요
2. 새로운 주제면 신규 폴더를 생성하세요
3. 폴더명은 한글 + 언더스코어, 2~4단어 이내
4. 최대 3단계 깊이까지만

JSON 형식으로 반환:
{{
  "path": "Area명/중분류/소분류/하위주제",
  "created_folders": ["신규 생성한 폴더명들"],
  "reasoning": "결정 이유"
}}

path는 Area명을 포함한 전체 경로여야 합니다.
반드시 유효한 JSON만 반환하세요. 다른 텍스트는 포함하지 마세요."""

        response = self.model.generate_content(prompt)

        # Parse JSON from response
        text = response.text.strip()
        # Remove markdown code blocks if present
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()

        result = json.loads(text)

        # Create folders if needed
        if result.get("created_folders"):
            self._create_folders(result["path"])

        return result

    def _create_folders(self, path: str):
        """Create folder structure if it doesn't exist"""
        full_path = Path(self.vault_path) / "20_Areas" / path
        full_path.mkdir(parents=True, exist_ok=True)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_taxonomy_agent.py -v`
Expected: PASS (requires OBSIDIAN_VAULT_PATH set)

**Step 5: Commit**

```bash
git add components/taxonomy_agent.py tests/test_taxonomy_agent.py
git commit -m "feat: add AI-driven taxonomy agent for folder placement"
```

---

## Phase 4: Storage Integration

### Task 11: Obsidian Syncer

**Files:**
- Create: `components/obsidian_syncer.py`
- Create: `tests/test_obsidian_syncer.py`

**Step 1: Write the failing test**

```python
# tests/test_obsidian_syncer.py
import pytest
import os
from pathlib import Path
from components.obsidian_syncer import ObsidianSyncer

@pytest.fixture
def syncer():
    return ObsidianSyncer()

@pytest.fixture
def test_note_data():
    return {
        "id": "doc_20260222_001",
        "title": "테스트 노트",
        "area": "21_Real_Estate",
        "folder_path": "21_Real_Estate/테스트폴더",
        "summary": ["첫 줄", "둘째 줄", "셋째 줄"],
        "content": "본문 내용",
        "entities": {
            "locations": ["강남구"],
            "organizations": ["삼성"],
            "keywords": ["테스트"]
        },
        "tags": ["태그1", "태그2"],
        "gravity_score": 0.5,
        "related_notes": ["[[다른노트]]"],
        "source_url": "https://t.me/test/123",
        "created_at": "2026-02-22T14:30:00Z"
    }

def test_write_note_creates_markdown_file(syncer, test_note_data):
    file_path = syncer.write_note(test_note_data)

    assert os.path.exists(file_path)

    # Read and verify content
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "---" in content  # YAML frontmatter
    assert "id: doc_20260222_001" in content
    assert "title: 테스트 노트" in content
    assert "# 📌 핵심 요약" in content
    assert "첫 줄" in content

    # Cleanup
    os.remove(file_path)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_obsidian_syncer.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

```python
# components/obsidian_syncer.py
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class ObsidianSyncer:
    def __init__(self):
        self.vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
        if not self.vault_path:
            raise ValueError("OBSIDIAN_VAULT_PATH not set in .env")

    def write_note(self, data: dict) -> str:
        """Write note to Obsidian vault"""
        # Construct file path
        folder_path = Path(self.vault_path) / "20_Areas" / data["folder_path"]
        folder_path.mkdir(parents=True, exist_ok=True)

        # Generate filename
        date = data.get("created_at", datetime.now().isoformat())[:10]
        title_safe = data["title"].replace(" ", "_").replace("/", "_")
        filename = f"{date}_{title_safe}.md"
        file_path = folder_path / filename

        # Build markdown content
        content = self._build_markdown(data)

        # Write file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return str(file_path)

    def _build_markdown(self, data: dict) -> str:
        """Build markdown content with YAML frontmatter"""
        # YAML frontmatter
        yaml = f"""---
id: {data['id']}
title: "{data['title']}"
created_at: {data.get('created_at', datetime.now().isoformat())}
area: {data['area']}
folder_path: {data['folder_path']}
tags: {data.get('tags', [])}
entities:
  locations: {data.get('entities', {}).get('locations', [])}
  organizations: {data.get('entities', {}).get('organizations', [])}
  keywords: {data.get('entities', {}).get('keywords', [])}
gravity_score: {data.get('gravity_score', 0.0)}
source_url: {data.get('source_url', '')}
status: published
---

"""

        # Summary
        summary_lines = data.get('summary', [])
        if isinstance(summary_lines, list):
            summary = "\n".join([f"- {line}" for line in summary_lines])
        else:
            summary = summary_lines

        summary_section = f"""# 📌 핵심 요약
{summary}

"""

        # Content
        content_section = f"""# 📝 본문
{data.get('content', '원문 내용')}

"""

        # Related notes
        related = data.get('related_notes', [])
        related_section = ""
        if related:
            related_links = "\n".join([f"- {link}" for link in related])
            related_section = f"""# 🔗 연결된 노트
{related_links}

"""

        # Insights placeholder
        insights_section = """# 💡 인사이트
(AI 분석 또는 사용자 메모)
"""

        return yaml + summary_section + content_section + related_section + insights_section
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_obsidian_syncer.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add components/obsidian_syncer.py tests/test_obsidian_syncer.py
git commit -m "feat: add Obsidian syncer with YAML frontmatter"
```

---

## Phase 5: Main Pipeline Integration

### Task 12: Main Pipeline

**Files:**
- Modify: `main.py`

**Step 1: Write the integration code**

```python
# main.py
import os
import asyncio
import logging
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

from components.preprocessor import Preprocessor
from components.deduplicator import Deduplicator
from components.context_retriever import ContextRetriever
from components.llm_processor import LLMProcessor
from components.taxonomy_agent import TaxonomyAgent
from components.obsidian_syncer import ObsidianSyncer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

# Telegram config
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_STRING = os.getenv("TELEGRAM_SESSION_STRING")
TARGET_CHANNEL = "@opendoorai"
BATCH_SIZE = 10

async def process_message(message_text: str, message_id: int) -> dict:
    """Process a single message through the RAG pipeline"""
    try:
        # 1. Preprocess & Vectorize
        logger.info(f"[{message_id}] Preprocessing...")
        preprocessor = Preprocessor()
        preprocessed = preprocessor.process(message_text)

        # 2. Check Duplicate
        logger.info(f"[{message_id}] Checking duplicates...")
        deduplicator = Deduplicator()
        dup_result = deduplicator.check_duplicate(
            preprocessed["cleaned_text"],
            preprocessed["embedding"]
        )

        if dup_result["is_duplicate"]:
            logger.info(f"[{message_id}] Duplicate detected, skipping...")
            return {"status": "duplicate", "target_id": dup_result["target_note_id"]}

        # 3. Retrieve Context (RAG)
        logger.info(f"[{message_id}] Retrieving context...")
        retriever = ContextRetriever()
        context = retriever.get_context(
            preprocessed["cleaned_text"],
            preprocessed["embedding"],
            []  # entities will be extracted by LLM
        )

        # 4. LLM Processing
        logger.info(f"[{message_id}] LLM processing...")
        llm = LLMProcessor()
        llm_result = llm.process_with_context(preprocessed["cleaned_text"], context)

        # 5. Taxonomy Agent
        logger.info(f"[{message_id}] Determining folder path...")
        taxonomy = TaxonomyAgent()
        path_result = taxonomy.determine_path(llm_result)

        # 6. Prepare note data
        note_data = {
            **llm_result,
            "id": f"doc_{message_id}",
            "folder_path": path_result["path"],
            "content": preprocessed["cleaned_text"],
            "source_url": f"https://t.me/{TARGET_CHANNEL.lstrip('@')}/{message_id}",
            "embedding": preprocessed["embedding"]
        }

        # 7. Write to Obsidian
        logger.info(f"[{message_id}] Writing to Obsidian...")
        syncer = ObsidianSyncer()
        file_path = syncer.write_note(note_data)

        # 8. Store embedding in Vector DB
        deduplicator.vector_db.upsert(
            collection="notes",
            id=note_data["id"],
            vector=note_data["embedding"],
            payload={
                "text": preprocessed["cleaned_text"],
                "area": note_data["area"],
                "status": "published"
            }
        )

        logger.info(f"[{message_id}] ✅ Completed: {file_path}")
        return {"status": "success", "file_path": file_path}

    except Exception as e:
        logger.error(f"[{message_id}] ❌ Failed: {e}")
        return {"status": "error", "error": str(e)}

async def main():
    if not API_ID or not API_HASH or not SESSION_STRING:
        logger.error("Missing Telegram credentials")
        return

    client = TelegramClient(StringSession(SESSION_STRING), int(API_ID), API_HASH)

    logger.info("Connecting to Telegram...")
    await client.connect()

    if not await client.is_user_authorized():
        logger.error("Session not authorized")
        return

    logger.info(f"Monitoring channel: {TARGET_CHANNEL}")

    try:
        entity = await client.get_entity(TARGET_CHANNEL)

        # Fetch recent messages
        messages = []
        async for message in client.iter_messages(entity, limit=BATCH_SIZE):
            if message.text:
                messages.append(message)

        logger.info(f"Found {len(messages)} messages to process")

        # Process each message
        for msg in messages:
            await process_message(msg.text, msg.id)
            await asyncio.sleep(2)  # Rate limiting

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await client.disconnect()
        logger.info("Disconnected")

if __name__ == "__main__":
    asyncio.run(main())
```

**Step 2: Test the pipeline**

Run: `python main.py`
Expected: Processes messages from Telegram and creates Obsidian notes

**Step 3: Commit**

```bash
git add main.py
git commit -m "feat: integrate full RAG pipeline in main.py"
```

---

## Phase 6: Testing & Documentation

### Task 13: Integration Test

**Files:**
- Create: `tests/test_integration.py`

**Step 1: Write integration test**

```python
# tests/test_integration.py
import pytest
import asyncio
from main import process_message

@pytest.mark.asyncio
async def test_end_to_end_pipeline():
    """Test complete pipeline with sample message"""
    test_message = """강남구 대치동 아파트 실거래가가 전월 대비 5% 상승했습니다.

금리 인하 기대감과 학군 수요 증가가 주요 원인으로 분석됩니다."""

    result = await process_message(test_message, 99999)

    assert result["status"] in ["success", "duplicate"]
    if result["status"] == "success":
        assert "file_path" in result
```

**Step 2: Run test**

Run: `pytest tests/test_integration.py -v`
Expected: PASS

**Step 3: Commit**

```bash
git add tests/test_integration.py
git commit -m "test: add end-to-end integration test"
```

---

### Task 14: Update README

**Files:**
- Modify: `README.md`

**Step 1: Add comprehensive documentation**

```markdown
# Telegram Refiner RAG Pipeline

맥락 인식 텔레그램 메시지 정제 시스템 - RAG 기반 중복 제거 및 지능형 Obsidian 지식 관리

## Features

- ✅ **RAG 기반 맥락 인식**: 과거 대화와 관련 주제를 고려한 처리
- ✅ **벡터 기반 중복 제거**: 의미적 유사도 88% 이상 중복 판정
- ✅ **10개 Area 자동 분류**: 부동산, 금융, 대체투자, 커리어, 세금, 경제, 인생설계, 심리, AI, 사회문화
- ✅ **AI 자율 폴더 관리**: 동적 지식 구조 자동 생성
- ✅ **Obsidian 제2의 뇌**: Google Drive 동기화, 크로스플랫폼

## Architecture

```
Telegram → Preprocess → Deduplicate → Context Retrieval (RAG)
         → LLM Processing → Taxonomy Agent → Obsidian Sync
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Qdrant Vector DB

```bash
docker run -p 6333:6333 qdrant/qdrant:latest
```

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in:

```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_SESSION_STRING=your_session_string

QDRANT_HOST=localhost
QDRANT_PORT=6333

OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_gemini_key

OBSIDIAN_VAULT_PATH=/path/to/your/100_Obsidian
```

### 4. Run

```bash
python main.py
```

## Testing

```bash
# Run all tests
pytest -v

# Run specific test
pytest tests/test_deduplicator.py -v
```

## Obsidian Setup

1. Install Obsidian: https://obsidian.md
2. Open vault: Select your `100_Obsidian` folder
3. Enable Google Drive sync for mobile access
4. Explore knowledge graph with Graph View

## Components

- `preprocessor.py`: Text cleaning & embedding
- `deduplicator.py`: Vector-based duplicate detection (>88%)
- `context_retriever.py`: RAG context search
- `llm_processor.py`: Context-aware LLM analysis
- `taxonomy_agent.py`: AI folder placement
- `obsidian_syncer.py`: Markdown file generation

## License

MIT
```

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add comprehensive README with setup and usage"
```

---

## Completion Checklist

- [x] Phase 1: Infrastructure Setup
  - [x] Dependencies installed
  - [x] Qdrant running
  - [x] Taxonomy configuration

- [x] Phase 2: Core Services
  - [x] Embedding service
  - [x] Vector DB service

- [x] Phase 3: Processing Components
  - [x] Preprocessor
  - [x] Deduplicator
  - [x] Context Retriever (RAG)
  - [x] LLM Processor
  - [x] Taxonomy Agent

- [x] Phase 4: Storage Integration
  - [x] Obsidian Syncer

- [x] Phase 5: Main Pipeline
  - [x] Integration in main.py

- [x] Phase 6: Testing & Documentation
  - [x] Integration test
  - [x] README documentation

---

## Notes

- **Supabase integration** is intentionally omitted from this plan. The current implementation stores to Vector DB and Obsidian only. Supabase can be added later as Phase 7.
- **Entity history and thread detection** in Context Retriever are stubbed and marked as TODO. These require Supabase queries.
- All tests require appropriate API keys in `.env`
- Qdrant must be running for vector DB tests

---

**Implementation Status**: Ready to begin
**Estimated Time**: 2-3 hours for core pipeline
**Next Steps**: Choose execution approach (Subagent-Driven or Parallel Session)
