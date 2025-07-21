import os
from dotenv import load_dotenv

load_dotenv()

ROOT = os.path.dirname(__file__)
ROOTDATA = os.path.join(ROOT, 'datas')
LOSTURL = 'https://www.lost112.go.kr'
STARTPAGE = 1
START_YMD = '20250118'
ALLDATA = 'all.json'

# AWS S3 설정
S3_ACCESS_KEY = os.getenv("access-key")
S3_SECRET_KEY = os.getenv("secret-key")
S3_BUCKET_NAME = os.getenv("bucket-name")
S3_REGION = os.getenv("region")

# Redis 설정
REDIS_HOST = os.getenv("host")
REDIS_PORT = int(os.getenv("port", 6379))
REDIS_STREAM = os.getenv("stream")
REDIS_PASSWORD = os.getenv("password")
