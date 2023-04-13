from utils.crawler import Crawler, Updater
from utils import crawler
import config as cfg
import os

def crawl(option):
    start = cfg.STARTPAGE
    if option == 'ca':
        crawl = Crawler()
        while True:
            ids = crawler.getIds(start)
            if not ids:
                print('complete')
                break
            crawl.crawlAll(ids)
            start += 1
            
            if start % 100 == 0:
                print('----------------------{} pages crawled----------------------'.format(start * 100))
            
        crawl.toJson()
        
    elif option == 'un':
        assert os.path.isfile(os.path.join(cfg.ROOTDATA, cfg.ALLDATA)), f'{cfg.ALLDATA} file is not exist'
        updater = Updater()
        while True:
            ids = crawler.getIds(start)
            if not updater.isCompleteUpdate(ids):
                break
            start += 1
        updater.updateJson()
        print('complete')
        
    else:
        print('retry')
