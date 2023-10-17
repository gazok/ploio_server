from fastapi import FastAPI
import asyncio
import json
import requests
import struct
import sys

from collections import deque

app = FastAPI()

agent_ip = "54.253.191.26"
agent_port = "8080"

parsed_data = deque(maxlen=100)  # 데이터를 저장할 큐, 최대 크기를 10으로 설정

async def fetching_process():
    print('helee')
    # 반복적으로 req를 보내고, reply를 파싱해서 공유변수 parsed_data에 저장
    while True:
        print('while')
        agent_service = AgentService(agent_ip, agent_port)
        # response_content = await agent_service.send_http_get_request()
        print("here")
        # data = agent_service.parse_data(response_content)
        with open("tmp/sample.bin","rb") as file:
            bitstream = file.read()
        data = agent_service.parse_data(bitstream)
        # print(data)
        parsed_data.append(data) # 리스트에 임시 저장. 근데 일정량이 차면 비워줘야 하는데 어떻게?
        await asyncio.sleep(2)


class AgentService:
    # agent에 접근할 때 쓰일 서비스 클래스
    def __init__(self, agent_ip, agent_port):
        self.agent_url = f"http://{agent_ip}:{agent_port}"

    # 지정 ip와 port로 http req를 보냄 (비동기)
    # 그런데 실제로는 모든 노드를 찾아서 보내야하는데 이걸 어떻게 구현할 것인가
    async def send_http_get_request(self):
        response = await requests.get(f"{self.agent_url}")
        return response.content

    # fetching process에서 쓰는 멤버함수.
    # req로 받아온 reply data를 파싱하는 로직
    def parse_data(self, bitstream):

        log_data = {
            "data": []
        }
        signature, version, count_of_log = struct.unpack('4s4si', bitstream[:12])


        print(bitstream[:12])
        log_data["signature"] = signature.decode('utf-8')  # 바이트를 문자열로 디코딩
        log_data["version"] = version.decode('utf-8')  # 바이트를 문자열로 디코딩
        log_data["count_of_log"] = count_of_log
        print(sys.getsizeof(signature))
        print(sys.getsizeof(version))
        print(sys.getsizeof(count_of_log))
        print("sig : ", signature)
        print("ver : " , version)
        print("cnt : " , count_of_log)
        print(log_data)
        offset = 12  # 이미 읽은 바이트 수

        for i in range(count_of_log):
            data = {}
            unix_epoch, protocol, sip, dip, sport, dport, size = struct.unpack('qi16s16shhi', bitstream[offset:offset+52])
            
            data["unix_epoch"] = unix_epoch
            data["protocol"] = protocol
            data["sip"] = sip.decode('utf-8')
            data["dip"] = dip.decode('utf-8')
            data["sport"] = sport
            data["dport"] = dport
            data["size"] = size

            log_data["data"].append(data)
            print(data)
            offset += 52  # 다음 로그 항목으로 이동

        with open("tmp/parsed_data.json", 'w') as json_file:
            json.dump(log_data, json_file, indent=4)

        return data
