from bs4 import BeautifulSoup
from collections import OrderedDict
import requests
import json
import warnings
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config as cfg
warnings.filterwarnings('ignore')


def isEnd(soup):
    item_num = len(soup.find('table', {'class': 'type01'}).find('tbody').find_all('tr'))
    return True if item_num > 0 else False


def wait(url):
    while True:
        try:
            req = requests.get(url, verify=False)
            soup = BeautifulSoup(req.text, 'html.parser')
            return soup
        except Exception as e:
            print('"{}" error occurred in page {}, reconnect ... '.format(e, url))
            time.sleep(3)


def getIds(page):
    url = f'https://www.lost112.go.kr/find/findList.do?PLACE_SE_CD=LL1003&pageIndex={page}'
    soup = wait(url)
    return [i.find('td').text for i in soup.find('table', {'class': 'type01'}).find('tbody').find_all('tr')] \
        if isEnd(soup) else [] # 관리번호


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
        
    return {'title': title,
            'getDate': infos[1],
            'getPlace': infos[2],
            'type': infos[3],
            'receiptPlace': infos[4],
            'storagePlace': infos[5],
            'lostStatus': infos[6],
            'phone': infos[7],
            'context': getText(soup),
            'image': cfg.LOSTURL + soup.find('p', {'class': 'lost_img'}).find('img').get('src'),
            'source': 'lost112'
            }


class Crawler:
    def __init__(self):
        self.info = OrderedDict()
        
    def crawlAll(self, ids):
        for id in ids:          
            self.info[id] = getInfo(id)
    
    def toJson(self):
        with open(os.path.join(cfg.ROOTDATA, cfg.ALLDATA), 'w', encoding='utf-8') as f:
            json.dump(self.info, f, ensure_ascii=False, indent=4)


class Updater:
    def __init__(self):
        with open(os.path.join(cfg.ROOTDATA, cfg.ALLDATA), 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.keys = list(self.data.keys())
        self.new_datas = {}
            
    def isCompleteUpdate(self, ids):
        for id in ids:
            if id in self.keys:
                self.data = dict([(k, v) for k, v in self.new_datas.items()] \
                                + [(k, v) for k, v in self.data.items()])
                return False
            self.new_datas[id] = getInfo(id)
            
        return True
    
    def updateJson(self):
        with open(os.path.join(cfg.ROOTDATA, cfg.ALLDATA), 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
