# main.py on_app_start 함수내에 두면 글로벌 스코프가 아니라서 다른 라우터에서 사용 못하고 함수내에서만 사용 가능함
# --> init파일을 하나 만들어서 클래스로 묶은 후 사용 목적
# Creating the engine
# db와 파이썬 프로그램 연결 역할 = 중계자

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine 
from app.config import MONGO_DB_NAME, MONGO_URL # config 변수 가져오기

# client = AsyncIOMotorClient(MONGO_URL)
# engine = AIOEngine(motor_client=client, database=MONGO_DB_NAME)

class MongoDB:
    def __init__(self):
        self.client = None
        self.engine = None
        
    def connect(self):
        self.client = AsyncIOMotorClient(MONGO_URL)
        self.engine = AIOEngine(moter_client=self.client, database=MONGO_DB_NAME)
        print("DB와 성공적으로 연결됨")
       
# 인스턴스 생성
mongodb = MongoDB()