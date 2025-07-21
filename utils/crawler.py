from bs4 import BeautifulSoup
import boto3
import redis
import requests

import json
import time
import os
import sys
from collections import OrderedDict
import warnings

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config as cfg
warnings.filterwarnings('ignore')

# Redis 객체 전역 생성
r = redis.Redis(
    host=cfg.REDIS_HOST,
    port=cfg.REDIS_PORT,
    password=cfg.REDIS_PASSWORD,
    decode_responses=True
)


def send_message(message: str):
    """
    Redis Stream에 단일 메시지를 XADD
    """
    # Stream 전송
    r.xadd(cfg.REDIS_STREAM, message)


def wait(url):
    isEscapeLoop = False
    while True:
        try:
            req = requests.get(url, verify=False)
            soup = BeautifulSoup(req.text, 'html.parser')
            if isEscapeLoop:
                print('Successfully connect in page {}'.format(url))
            return soup
        except Exception as e:
            print('"{}" error occurred in page {}, reconnect ... '.format(e, url))
            time.sleep(3)
            isEscapeLoop = True


def getIds(page):
    url = f'https://www.lost112.go.kr/find/findList.do?START_YMD={cfg.START_YMD}&PLACE_SE_CD=LL1003&pageIndex={page}'
    soup = wait(url)
    ids = [i.find('td').text for i in soup.find('table', {'class': 'type01'}).find('tbody').find_all('tr')]
    return ids if ids != ['검색 결과가 없습니다.'] else []


def getInfo(id):
    def getText(soup):
        div = soup.find('div', {'class': 'find_info_txt'})
        try:
            text = [div.find('br').previous_sibling.strip()] + [br.nextSibling.strip() for br in div.find_all('br')]
            return ' '.join([i for i in text if i != ''])
        
        except AttributeError:
            return div.text.strip()


    url = f'https://www.lost112.go.kr/find/findDetail.do?ATC_ID={id}&FD_SN=1'
    soup = wait(url)
    infos = [i.text.strip() for i in soup.find_all('p', {'class': 'find02'})]
    title = soup.find('p', {'class': 'find_info_name'}).text.split(':')[-1].strip()

    return {
                'ID': id,
                'title': title,
                'personName': infos[1],
                'getDate': infos[2],
                'getPlace': infos[3],
                'type': infos[4],
                'receiptPlace': infos[5],
                'storagePlace': infos[6],
                'lostStatus': infos[7],
                'phone': infos[8],
                'context': getText(soup),
                'image': cfg.LOSTURL + soup.find('p', {'class': 'lost_img'}).find('img').get('src'),
                'source': 'lost112',
                'page': url
            } if len(infos) == 9 else \
     {  
        'ID': id,
        'title': title,
        'getDate': infos[1],
        'getPlace': infos[2],
        'type': infos[3],
        'receiptPlace': infos[4],
        'storagePlace': infos[5],
        'lostStatus': infos[6],
        'phone': infos[7],
        'context': getText(soup),
        'image': cfg.LOSTURL + soup.find('p', {'class': 'lost_img'}).find('img').get('src'),
        'source': 'lost112',
        'page': url
    }


def toJson(file_name, data):
    # 중복 유실물 제거
    unique_data = list(OrderedDict((item['ID'], item) for item in data).values())
    
    # S3 클라이언트 생성
    s3 = boto3.client(
        's3',
        aws_access_key_id=cfg.S3_ACCESS_KEY,
        aws_secret_access_key=cfg.S3_SECRET_KEY,
        region_name=cfg.S3_REGION
    )

    # JSON 문자열로 변환 후 바이트로 인코딩
    json_body = json.dumps(unique_data, ensure_ascii=False, indent=4).encode('utf-8')

    # S3에 업로드 (덮어쓰기)
    s3.put_object(
        Bucket=cfg.S3_BUCKET_NAME,
        Key=f"{file_name}",
        Body=json_body,
        ContentType='application/json'
    )


class Crawler:
    def __init__(self):
        self.info = []
        
        
    def crawlAll(self, ids):
        for id in ids:
            info = getInfo(id)
            self.info.append(info)

            # Redis-stream에 실시간 전송
            send_message(info)
    
    def saveJson(self):
        toJson(cfg.ALLDATA, self.info)


class Updater:
    def __init__(self):
        # S3 클라이언트 설정
        s3 = boto3.client(
            's3',
            aws_access_key_id=cfg.S3_ACCESS_KEY,
            aws_secret_access_key=cfg.S3_SECRET_KEY,
            region_name=cfg.S3_REGION
        )

        # S3에서 all.json 가져오기
        key = f"{cfg.ALLDATA}"
        resp = s3.get_object(Bucket=cfg.S3_BUCKET_NAME, Key=key)
        body = resp['Body'].read().decode('utf-8')
        self.data = json.loads(body)

        # ID 목록 추출
        self.keys = [item['ID'] for item in self.data]
        self.new_datas = []
   
    def isCompleteUpdate(self, ids):
        for id in ids:
            if id in self.keys: return False
            info = getInfo(id)
            self.new_datas.append(info)

            # Redis-stream에 실시간 전송
            send_message(info)

        return True
    
    
    def makeNewJson(self):
        updated_all_data = self.new_datas
        toJson(cfg.ALLDATA, updated_all_data)
