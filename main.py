from utils import crawling
import argparse

parser = argparse.ArgumentParser(description='choose crawl all or update new or after date')
parser.add_argument('-o', '--option', type=str, help='ca for crawl all, un for update new, ad for crawl after date')
parser.add_argument('-d', '--date', type=str, help='Date in YYYYMMDD format')
args=parser.parse_args()

print("Start Crawling")
crawling.crawl(args.option, args.date)
