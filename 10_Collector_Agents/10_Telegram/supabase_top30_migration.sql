-- ============================================================
-- Telegram Daily Top 30 Views Tracker
-- Supabase Dashboard > SQL Editor에서 실행하세요.
-- ============================================================

CREATE TABLE IF NOT EXISTS telegram_daily_top30 (
    id          BIGSERIAL PRIMARY KEY,
    rank        INT NOT NULL,                  -- 1위 ~ 30위
    target_date DATE DEFAULT CURRENT_DATE,      -- 통계 기준 날짜
    topic       TEXT NOT NULL,                 -- 주제 (제목)
    content     TEXT,                          -- 주요 내용 요약
    views       INT DEFAULT 0,                 -- 조회수
    channel_name TEXT,                          -- 채널명
    message_id   BIGINT,                        -- 원본 메시지 ID
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    
    -- 동일 날짜, 동일 순위에 중복 데이터 방지
    UNIQUE(target_date, rank)
);

-- 검색 최적화 인덱스
CREATE INDEX IF NOT EXISTS idx_telegram_daily_top30_date ON telegram_daily_top30(target_date);
CREATE INDEX IF NOT EXISTS idx_telegram_daily_top30_views ON telegram_daily_top30(views);
