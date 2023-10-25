from bs4 import BeautifulSoup
import requests
import json
import warnings
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config as cfg
warnings.filterwarnings('ignore')


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
    url = f'https://www.lost112.go.kr/find/findList.do?PLACE_SE_CD=LL1003&pageIndex={page}'
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
            'source': 'lost112',
            'page': url
            }


class Crawler:
    def __init__(self):
        self.info = []
        
    def crawlAll(self, ids):
        for id in ids:          
            self.info.append({id: getInfo(id)})
    
    def toJson(self):
        separate_data = []
        count = 0
        file_num = 1
        for data in self.info:
            count += 1
            separate_data.append(data)
            if count == len(self.info) // cfg.SEPARATE_NUM and file_num != cfg.SEPARATE_NUM:
                with open(os.path.join(cfg.ROOTDATA, f'{file_num}.json'), 'w', encoding='utf-8') as file:
                    json.dump(separate_data, file, ensure_ascii=False, indent=4)
                    
                count = 0
                separate_data = []
                file_num += 1
        
        with open(os.path.join(cfg.ROOTDATA, f'{file_num}.json'), 'w', encoding='utf-8') as file:
            json.dump(separate_data, file, ensure_ascii=False, indent=4)



class Updater:
    def __init__(self):
        self.new_datas = []
        self.keys = []
        
        for file in os.listdir(cfg.ROOTDATA):
            if file != 'all.json':
                with open(os.path.join(cfg.ROOTDATA, file), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                keys = list(map(lambda x: list(x.keys())[0], data))   
                self.keys.extend(keys)

   
    def isCompleteUpdate(self, ids):
        for id in ids:
            if id in self.keys: return False 
            self.new_datas.append({id: getInfo(id)})
        return True
    
    def makeNewJson(self):
        updated_all_data = self.new_datas
        file_num = 1
        
        if len(updated_all_data) < cfg.SEPARATE_NUM:
            with open(os.path.join(cfg.ROOTDATA, f"{file_num}.json"), 'w', encoding='utf-8') as f:
                json.dump(updated_all_data, f, ensure_ascii=False, indent=4)
        
            for f_num in range(2, cfg.SEPARATE_NUM + 1):
                with open(os.path.join(cfg.ROOTDATA, f"{f_num}.json"), 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=4)

        else:
            separate_data = []
            count = 0
            
            for data in updated_all_data:
                count += 1
                separate_data.append(data)
                if count == len(updated_all_data) // cfg.SEPARATE_NUM and file_num != cfg.SEPARATE_NUM:
                    with open(os.path.join(cfg.ROOTDATA, f'{file_num}.json'), 'w', encoding='utf-8') as file:
                        json.dump(separate_data, file, ensure_ascii=False, indent=4)
                        
                    count = 0
                    separate_data = []
                    file_num += 1
            
            with open(os.path.join(cfg.ROOTDATA, f'{file_num}.json'), 'w', encoding='utf-8') as file:
                json.dump(separate_data, file, ensure_ascii=False, indent=4)
