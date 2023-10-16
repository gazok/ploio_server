import json

import requests
import struct

agent_ip = "54.253.191.26"
agent_port = "8080"


class AgentService:
    def __init__(self, agent_ip, agent_port):
        self.agent_url = f"http://{agent_ip}:{agent_port}"

    async def send_http_get_request(self):
        response = requests.get(f"{self.agent_url}")
        return response.content

    def parse_data(self, bitstream):
        signature, version, count_of_log = struct.unpack('4s4si', bitstream)
        # JSON 데이터 생성
        data = {
            "signature": signature.decode('utf-8'),  # 바이트를 문자열로 디코딩
            "version": version.decode('utf-8'),  # 바이트를 문자열로 디코딩
            "count_of_log": count_of_log
        }
        with open("tmp/parsed_data", 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return data
