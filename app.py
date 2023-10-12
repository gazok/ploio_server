import requests
import csv
from fastapi import FastAPI
from sqlalchemy.orm import Session
from models import Item, Base
from db import EngineConn
from typing import Union

app = FastAPI()

agent_ip = "54.253.191.26"
agent_port = "80"

url = f"http://{agent_ip}:{agent_port}/"

# 데이터베이스 연결 설정
db_conn = EngineConn()
Base.metadata.create_all(db_conn.engine)

# @app.get("/")
# def read_root():
#     return {"Hello": "Ploio"}
    
# 라우트: 데이터 가져오기
@app.get("/items/{item_id}")
def read_item(item_id: int):
    # 데이터베이스 연결과 세션 생성
    db = db_conn.get_session()
    
    # 데이터베이스에서 아이템 검색
    db_item = db.query(Item).filter(Item.id == item_id).first()
    
    # 데이터베이스 세션 종료
    db.close()
    
    # 아이템을 딕셔너리 형태로 반환
    if db_item:
        return db_item.to_dict()
    else:
        return {"error": "Item not found"}

@app.get("/")
def get_csv():
    while(True):
        try:
            # GET req
            response = requests.get(f"https://naver.com")
            # response = requests.get(f"https://{agent_ip}:{agent_port}/")

            # response
            if response.status_code == 200:
                csv_data = response.text

                # save csv
                with open("data.csv", "w") as csv_file:
                    csv_file.write(csv_data)
                # print(csv_data)
                return {"message": "CSV data saving success"}
            else:
                return {"error": "failure."}

        except Exception as e:
            return {"error": str(e)}