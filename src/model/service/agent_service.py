from fastapi import FastAPI

from collections import deque

app = FastAPI()

from model.domain.packet import PacketList, PacketItem
from model.domain.pod import PodList, PodItem
from model.domain.log import LogList, LogItem

packet_data = PacketList(data=[])
pod_data = PodList(pods=[])
log_data = LogList(logs=[])

malicious_pod = deque(maxlen=100)


class Agent_service:
    def __init__(self):
        pass

    def save_packet_data(self, packet_dict: dict):
        for packet_id, packet in packet_dict.items():
            # "Raw" 필드를 제외한 값들을 추출하여 새로운 딕셔너리에 추가
            packet_data.data.append(
                PacketItem(
                    packet_id=self.get_pod_info(packet_id),
                    src_pod=self.get_pod_info(packet["Source"]),
                    dst_pod=self.get_pod_info(packet["Destination"]),
                    timestamp=packet["Timestamp"],
                    data_len=packet["Size"],
                )
            )
        return packet_data

    def get_pod_info(self, target_pod_id: str):
        # # 테스트용
        # test_pod_data = {
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
                    pod_id,
                    pod["Name"],
                    pod["Namespace"],
                    (pod["Network"])[0],
                    "danger_degree",
                    "message",
                )
            )
        return pod_data

    def save_log_data(self, log_list: dict):
        # packet_sample = {
        #     "data": [
        #         {
        #             "packet_id": "PCKT-001",
        #             "src_pod": "default:front-end3",
        #             "dst_pod": "default:api-server",
        #             "timestamp": 12341234,
        #             "data_len": 1024,
        #         }
        #     ]
        # }
        for log_id, log_entry in log_list.items():
            code = log_entry.get("Code")
            if code in ["Warning", "Fail", "Critical"]:
                for ref in log_entry.get("Refs", []):
                    if ref.get("Source") == "Packet":
                        packet_id = ref.get("Identifier")
                        for packet in packet_data["data"]:
                            if packet["packet_id"] == packet_id:
                                log_data.logs.append(
                                    LogItem(
                                        packet_id=packet_id,
                                        src_pod=packet["src_pod"],
                                        dst_pod=packet["dst_pod"],
                                        timestamp=packet["timestamp"],
                                        data_len=packet["data_len"],
                                        danger_degree=code,
                                        danger_message=log_entry.get("Message", ""),
                                    )
                                )
        return log_data
