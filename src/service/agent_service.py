from fastapi import FastAPI
import requests

from collections import deque

app = FastAPI()


packet_data = deque(maxlen=100)
pod_data = deque(maxlen=100)
log_data = deque(maxlen=100)

malicious_pod = deque(maxlen=100)


class Agent_service:
    def __init__(self):
        pass

    def save_packet_data(self):
        response = requests.get(f"{agent_url}")
        for packet_id, packet_info in response.json().items():
            if "Raw" in packet_info:
                del packet_info["Raw"]
        return response.json()

    def save_pod_date(self):
        response = requests.get(f"{agent_url}")
        return response.content

    def save_log_data(self):
        response = requests.get(f"{agent_url}")
        malicious_packet = deque
        malicious_packet.extend(
            log["Refs"][0]["Identifier"]
            for log_id, log in response.items()
            if log.get("Code", 0) >= 2
        )
        for packet in malicious_packet:
            packet_id = packet["packet-id"]

            # 예시 JSON 데이터에서 해당 패킷의 정보 가져오기
            if packet_id in packet_data:
                packet_info = packet_data[packet_id]

                # packet-id에 해당하는 패킷의 Source와 Destination 가져오기
                malicious_pod.append(packet_info["Source"])
                malicious_pod.append(packet_info["Destination"])

        return response.content
