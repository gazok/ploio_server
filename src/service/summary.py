from fastapi import FastAPI
import asyncio
import json
import requests
import struct

app = FastAPI()

agent_ip = "54.253.191.26"
agent_port = "8080"

parsed_data = []


@app.on_event("startup")
async def startup_event():
    # fetching process를 fastapi 서버가 올라가는 동시에 실행
    asyncio.create_task(fetching_process())


async def fetching_process():
    # 반복적으로 req를 보내고, reply를 파싱해서 공유변수 parsed_data에 저장
    while True:
        agent_service = AgentService(agent_ip, agent_port)
        response_content = agent_service.send_http_get_request()
        data = agent_service.parse_data(response_content)
        print(data)
        parsed_data = data # 리스트에 임시 저장. 근데 일정량이 차면 비워줘야 하는데 어떻게?


class AgentService:
    # agent에 접근할 때 쓰일 서비스 클래스
    def __init__(self, agent_ip, agent_port):
        self.agent_url = f"http://{agent_ip}:{agent_port}"

    # 지정 ip와 port로 http req를 보냄 (비동기)
    # 그런데 실제로는 모든 노드를 찾아서 보내야하는데 이걸 어떻게 구현할 것인가
    async def send_http_get_request(self):
        response = requests.get(f"{self.agent_url}")
        return response.content

    # fetching process에서 쓰는 멤버함수.
    # req로 받아온 reply data를 파싱하는 로직
    def parse_data(self, bitstream):
        signature, version, count_of_log = struct.unpack('4s4si', bitstream)
        # JSON 데이터 생성
        # count만큼 52byte 데이터를 추가적으로 파싱해야 함
        data = {
            "signature": signature.decode('utf-8'),  # 바이트를 문자열로 디코딩
            "version": version.decode('utf-8'),  # 바이트를 문자열로 디코딩
            "count_of_log": count_of_log
        }
        with open("tmp/parsed_data", 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return data
