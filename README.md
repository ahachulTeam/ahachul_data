## ahachul_data
더욱 쾌적한 지하철을 위해서, 아! 하철이형 서비스의 Data 레포입니다
***
### 1. git clone
- 해당 repository clone 후, root directory에 위치

### 2. 필요 라이브러리 설치
```
pip install -r requirements.txt
```
### 3. 유실물 크롤링 실행
cmd에서 세 가지 옵션으로 크롤링 가능
1. python3 main.py -o ca
- ca(crawling all) 옵션은 lost112의 모든 데이터를 크롤링
2. python3 main.py -o un
- un(update new) 옵션은 기존 data에 없는 새로 update된 data를 크롤링
3. python3 main.py -o ad -d YYYYMMDD
- ad(after date) 옵션은 입력한 날짜 이후 데이터만 크롤링
- 입력한 날짜를 포함해서 데이터를 크롤링합니다.

un 옵션은 datas directory에 all.json 파일이 존재할 때만 실행 가능<br>
현재는 all.json이 database 역할을 하고 있으며, 파일 이름은 config.py의 ALLDATA로 수정 가능

### 4. 뉴스 기사 크롤링 실행
cmd에서 세 가지 옵션으로 크롤링 가능
- 최상단 디렉토리에서 하위 명령어 실행
- python utils/news_crawling.py
