from utils.crawler import Crawler, Updater
from utils import crawler
import config as cfg
import os

def crawlDetail(start):
    crawl = Crawler()
    while True:
        ids = crawler.getIds(start)
        if not ids:
            print('complete')
            break
        crawl.crawlAll(ids)
        start += 1
        if start % 10 == 0:
            print('----------------------{} pages crawled----------------------'.format(start))
        
    crawl.saveJson()
    

def crawl(option, date):
    start = cfg.STARTPAGE
    if option == 'ca':
        crawlDetail(start)
        
    elif option == 'un':
        assert not os.path.isfile(cfg.ROOTDATA), \
            'Any file does not exist in datas directory. You should crawl all data first.'
        updater = Updater()
        while True:
            ids = crawler.getIds(start)
            if not updater.isCompleteUpdate(ids) or not ids:
                break
            start += 1
        updater.makeNewJson()
        print('complete')
    
    elif option == 'ad':
        cfg.START_YMD = date
        crawlDetail(start)
        
    else:
        print('retry')
