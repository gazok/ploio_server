from fastapi import FastAPI
import asyncio
import json
import requests
import struct

from collections import deque

app = FastAPI()

# 나중에 노드 순회해야함
agent_ip = "54.253.191.26"
agent_port = "8080"

parsed_data = deque(maxlen=100)  # 데이터를 저장할 큐, 최대 크기를 10으로 설정

async def fetching_process():
    # 반복적으로 req를 보내고, reply를 파싱해서 공유변수 parsed_data에 저장
    while True:
        agent_service = AgentService(agent_ip, agent_port)
        response_content = await agent_service.send_http_get_request()
        data = agent_service.parse_data(response_content)

        # 아래 문단은 테스트용
        # with open("tmp/sample3.bin","rb") as file:
            # bitstream = file.read()
        # data = agent_service.parse_data(bitstream)
        
        # 공유변수 parsed_data. `api/summary`에서 접근 가능
        parsed_data.append(data)

        # 텀 두기
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
        signature, version, count_of_log = struct.unpack('>4s4si', bitstream[:12])

        # add header info into temp buffer
        log_data["signature"] = signature.decode('utf-8')
        log_data["version"] = (int.from_bytes(version, byteorder='little'))
        log_data["count_of_log"] = count_of_log

        offset = 12  # header size

        # insert logs into temp buffer by the count
        for i in range(count_of_log):
            data = {}
            # parse agent data
            unix_epoch, l2_protocol, l3_protocol, l7_protocol, sip, dip, sport, dport, size = struct.unpack('>qHBB16s16sHHi', bitstream[offset:offset+52])

            # assign data after Ipv4 / Ipv6 check
            data["src_ip"] = self.check_ip(l2_protocol, sip)
            data["src_port"] = sport
            
            # assign data after Ipv4 / Ipv6 check
            data["dst_ip"] = self.check_ip(l2_protocol, dip)
            data["dst_port"] = dport
            data["data_len"] = size
        
            data["protocol"] = self.check_protocol(l3_protocol)
            data["timestamp"] = unix_epoch

            # add into temp buffer
            log_data["data"].append(data)

            offset += 52  # 다음 로그 항목으로 이동
        # insert temp buffer into log buffer
        with open("tmp/parsed_data.json", 'w') as json_file:
            json.dump(log_data, json_file, indent=4)

        return log_data
    
    def check_protocol(self,protocol):
        # check protocol type
        if protocol == 6:
            protocol_type = 'TCP'
        elif protocol == 17:
            protocol_type = 'UDP'
        return protocol_type

    def check_ip(self, ip_type, ip_hex):
        # Ipv4
        if ip_type == 1:
            bytes_list = [ip_hex[i:i+4] for i in range(0, len(ip_hex), 4)]
            ip_address = '.'.join([str(byte) for byte in bytes_list[0]])
            return ip_address
        # 그외
        # else:
