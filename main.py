from utils import crawling
import argparse

parser = argparse.ArgumentParser(description='choose crawl all or update new')
parser.add_argument('-o', '--option', type=str, help='ca for crawl all, un for update new')
args=parser.parse_args()

print("Start Crawling")
crawling.crawl(args.option)
