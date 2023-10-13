import requests
import csv
import asyncio
import json

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

buffer = []
@app.get("/")
def read_root():
    return {"Hello": "Ploio"}
    
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

@app.get("/summary/security")
def return_traffic_log():
    with open("./agent_data_buffer.json", "r") as json_file:
        data = json.load(json_file)
    return data

async def get_pkt_from_agent():
    while True:
        try:
            # GET req
            response = requests.get(f"https://naver.com")
            # response = requests.get(f"https://{agent_ip}:{agent_port}/")

            # response
            if response.status_code == 200:
                csv_data = response.text
                
                # save csv
                with open("./data.csv", 'r') as csv_data:
                    csv_reader = csv.DictReader(csv_data)
                    for row in csv_reader:
                    # 필드 이름을 기준으로 데이터 추출
                        data = {
                            'src_ip': (row['src_ip']),
                            'src_port': int(row['src_port']),
                            'dst_ip': row['dst_ip'],
                            'dst_port': int(row['dst_port']),
                            'data_len': int(row['data_len']),
                            'protocol': row['protocol'],
                        }
                        buffer.append(data)
                with open("agent_data_buffer.json", 'w') as json_file:
                    json.dump(buffer, json_file, indent=4)

                print({"message": "CSV data saving success"})
            else:
                print({"error": "failure."})
        except Exception as e:
            print({"error": str(e)})
        await asyncio.sleep(1)

# def csv_to_json(csv_data):
#     csv_lines = csv_data.strip().split('\n')
#     csv_reader = csv.reader(csv_lines)
#     json_data = []

#     for row in csv_reader:
#         record = {
#             'src_ip': row[0],
#             'dst_ip': row[1],
#             'http_header': row[2]
#         }
#         json_data.append(record)

#     return json.dumps(json_data)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(get_pkt_from_agent())

