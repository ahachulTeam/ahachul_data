# Data Repo Conventions (ahachul_data)

## Commit Message

- Existing repo style baseline: `feat:`, `fix:`, `docs:`, `refactor:`
- 권장 형식: `<type>: <summary>`
- 예시:
  - `feat: 뉴스 크롤링 키워드 확장`
  - `fix: redis stream 전송 예외 처리`
  - `docs: 데이터 운영 가이드 업데이트`

## Runtime/Config

- 실행 진입점: `main.py`
- 옵션 계약:
  - `-o ca` (crawl all)
  - `-o un` (update new)
  - `-o ad -d YYYYMMDD` (after date)
- 민감 설정은 `config.py` + 환경변수로 주입

## Integration

- 산출물(`datas/all.json`, `datas/subway_news_data.json`) 스키마 변경 시 backend/consumer 영향 검토 필수
- Redis Stream key 변경 시 backend/consumer 동시 조정
