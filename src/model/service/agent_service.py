from fastapi import FastAPI

from collections import deque

app = FastAPI()

from model.domain.packet import PacketList, PacketItem
from model.domain.pod import PodList
from model.domain.log import LogList

packet_data = PacketList(data=[])
pod_data = deque(maxlen=100)
log_data = deque(maxlen=100)

malicious_pod = deque(maxlen=100)


class Agent_service:
    def __init__(self):
        pass

    def save_packet_data(self, packet_dict: dict):
        for packet_id, packet in packet_dict.items():
            # "Raw" 필드를 제외한 값들을 추출하여 새로운 딕셔너리에 추가
            packet_data.data.append(
                PacketItem(
                    src_pod=packet["Source"],
                    dst_pod=packet["Destination"],
                    timestamp=packet["Timestamp"],
                    data_len=packet["Size"],
                )
            )
        return packet_data

    def save_pod_data(self, pod_list: PodList):
        pod_data.append(pod_list)

    def save_log_data(self, log_list: LogList):
        malicious_packet = deque
        malicious_packet.extend(
            log["Refs"][0]["Identifier"]
            for log_id, log in log_list.items()
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

        return None
