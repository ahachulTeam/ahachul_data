# Data Operation Rulebook

Last Updated: 2026-02-18

## 1. 목적
- 유실물/뉴스 데이터 수집과 전달(S3 + Redis Stream)의 안정 운영

## 2. 필수 가드레일
- 자격증명 하드코딩 금지
- 운영 실행 전 대상 환경 변수 확인
- 산출 스키마 변경 시 소비자(back-end, consumer) 영향 문서화

## 3. 실행 체크
- `python3 main.py -o ca`
- `python3 main.py -o un`
- `python3 main.py -o ad -d 20260101`
- `python3 utils/news_crawling.py`

## 4. 실패 시 중단 조건
- Redis 연결 실패 상태로 데이터 적재를 강행하지 않는다.
- S3 버킷/권한이 불확실한 상태에서 overwrite를 강행하지 않는다.
