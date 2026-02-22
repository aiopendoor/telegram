# Design: Telegram Sync Optimization

## 1. 데이터 구조 설계 (Data Structure Design)

### `channels.json` 확장
```json
{
    "source_channels": [...],
    "destination_user_id": "@opendoorai",
    "keywords": [],
    "history_settings": {
        "start_date": "2018-01-01",
        "end_date": "2020-12-31",
        "exclude_years": [2021, 2022, 2023, 2024, 2025],
        "batch_size_per_channel": 100,
        "direction": "old_to_new" 
    },
    "settings": { ... }
}
```

### `last_processed_ids.json` 유지
- 현재 방식 유지: `{"channel_id": last_id}`
- 추가적으로 `finished_channels` 목록을 관리하여 완료된 채널은 건너뜀.

## 2. 알고리즘 설계 (Algorithm Design)

### 라운드 로빈 수집 프로세스 (Round-robin)
1. 모든 채널 목록을 가져옴.
2. 완료되지 않은 채널들에 대해 반복:
    - 각 채널별로 `batch_size_per_channel` 만큼의 메시지를 `iter_messages`로 가져옴.
    - 메시지를 필터링(날짜, 키워드)하고 전달.
    - 마지막 메시지 ID를 `last_processed_ids.json`에 저장.
    - 만약 가져온 메시지가 `batch_size`보다 적거나 더 이상 메시지가 없으면 해당 채널을 `finished`로 표시.
3. 모든 채널이 `finished` 될 때까지 또는 전체 수집 제한 시간에 도달할 때까지 2번 과정을 반복.

### 날짜 필터링 로직
- `exclude_years`에 포함된 연도의 메시지는 `continue`.
- `start_date` 이전 또는 `end_date` 이후 메시지는 수집 범위에서 제외.

## 3. 예외 처리 가이드 (Exception Handling)
- **FloodWaitError**: 감지 시 `seconds` 만큼 `sleep` 후 재개.
- **Media Error**: 미디어 전송 실패 시 로그 남기고 텍스트만 재시도.
- **Channel Access Error**: 접근 불가 채널은 로그 남기고 다음 채널로 스킵.

## 4. 인터페이스 개선
- 로그에 현재 어떤 채널의 어떤 날짜 메시지를 처리 중인지 상세히 표시.
- 수집 진행률(전체 채널 중 몇 개 완료 등) 표시.
