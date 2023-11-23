from fastapi import FastAPI

from collections import deque

app = FastAPI()

from model.domain.packet import PacketList, PacketItem
from model.domain.pod import PodList, PodItem
from model.domain.log import LogList

packet_data = PacketList(data=[])
pod_data = PodList(pods=[])
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
                    src_pod=self.get_pod_info(packet["Source"]),
                    dst_pod=self.get_pod_info(packet["Destination"]),
                    timestamp=packet["Timestamp"],
                    data_len=packet["Size"],
                )
            )
        print(packet_data)
        return packet_data

    def get_pod_info(self, target_pod_id: str):
        # 테스트용
        # pod_data = {
        #     "pods": [
        #         {
        #             "id": "pod-123",
        #             "name": "pod_name",
        #             "name_space": "namespace",
        #             "ip": "ip.ip.ip.ip",
        #             "danger_degree": "Information",
        #             "message": "Partial service may be dead or attacked; or mannual health-check is recommended",
        #         },
        #         {
        #             "id": "pod-456",
        #             "name": "pod_name",
        #             "name_space": "namespace",
        #             "ip": "ip.ip.ip.ip",
        #             "danger_degree": "Fail",
        #             "message": "Partial service was dead or attacked; or should be checked mannually",
        #         },
        #     ]
        # }

        for pod in pod_data["pods"]:
            if pod["id"] == target_pod_id:
                return f"{pod['name']}:{pod['name_space']}"
        else:
            return f"Pod ID '{target_pod_id}' not found."

    def save_pod_data(self, pod_dict: dict):
        for pod_id, pod in pod_dict.items():
            pod_data.pods.append(
                PodItem(
                    id=pod_id,
                    name=pod["Name"],
                    name_space=pod["Namespace"],
                    ip=(pod["Network"])[0],
                    danger_degree="danger_degree",
                    message="message",
                )
            )
        return pod_data

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
