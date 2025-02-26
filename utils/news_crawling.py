import re
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import config as cfg
from bs4 import BeautifulSoup
import requests

import json
from datetime import datetime
import urllib3
import warnings

urllib3.disable_warnings()
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


class Crawler:
    def __init__(self):
        self.keywords = ["지연", "운행 중단", "고장", "사고", "혼잡", "폭행", "도난", "파업"]  # 검색 키워드
        self.lines = [str(i) for i in range(1, 10)]  # 1호선 ~ 9호선
        # self.lines = [str(i) for i in range(1, 2)]  # 1호선 ~ 9호선
        self.url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=news&ssc=tab.news.all&query={keyword}&oquery={keyword}&tqi=iJY5UlpzLiwssk0akZwssssssMw-173881&nso=so%3Add%2Cp%3Aall"
        self.total_datas = {}  # 게시판에서 게시물 url들을 담아 리턴할 리스트
        self.lastPage = 1  # 마지막 페이지 설정 네이버의 경우 상품 리스트가 40개가 안될시 마지막 페이지로 인식

    def get_news_contents(self) -> list:
        for line in self.lines:
            line_col = f"line_{line}"
            self.total_datas[line_col] = []
            time.sleep(2)
            for keyword in self.keywords:
                time.sleep(1)
                search_keyword = f"서울지하철 {line}호선 {keyword}"
                print("search keyword", search_keyword)
                req = requests.get(self.url.format(keyword=search_keyword), verify=False)
                soup = BeautifulSoup(req.text, "html.parser")
                news_div = soup.find("div", class_="group_news")  # 해당 div 찾기
                li_tags = news_div.find_all("li", class_="bx")  # 모든 <li class="bx"> 찾기
                for li in li_tags[:3]:
                    date_tag = li.find("span", class_="info")  # <span class="info">를 찾음
                    news_contents = li.find("div", class_="news_contents")  # 해당 li 내부에서 첫 번째 <a> 태그 찾기
                    news_dict = {
                        "title": "",
                        "date": "",
                        "content": "",
                        "url": ""
                    }
                    if news_contents:
                        news_tit = news_contents.find("a", class_="news_tit")  # news_tit 태그 찾기
                        news_dsc = news_contents.find("div", class_="news_dsc")  # news_dsc 태그 찾기
                        if news_tit:
                            href = news_tit.get("href")  # 링크 추출
                            title = news_tit.get("title")  # 제목 추출
                            news_dict['title'] = title
                            news_dict['url'] = href
                        if news_dsc:
                            content = news_dsc.get_text(strip=True)  # 기사 내용 텍스트 추출
                            news_dict['content'] = content
                        if date_tag:
                            date = date_tag.get_text(strip=True)  # 날짜 텍스트만 추출
                            news_dict['date'] = date
                    self.total_datas[line_col].append(news_dict)
        print(self.total_datas)
        self.save_to_json()

    def save_to_json(self) -> None:
        """ 데이터를 JSON 파일로 저장하는 함수 """
        os.makedirs("datas", exist_ok=True)  # datas 폴더 생성 (없다면 생성)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(cfg.ROOTDATA, f"datas/subway_news_{timestamp}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.total_datas, f, ensure_ascii=False, indent=4)
        print(f" {file_path}에 저장 완료.")


if __name__ == "__main__":
    # 크롤러
    c = Crawler()
    c.get_news_contents()
