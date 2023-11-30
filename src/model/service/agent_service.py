from fastapi import FastAPI
from collections import deque
from fastapi import HTTPException, status
from database.connection import Module
from model.domain.packet import PacketList, PacketItem
from model.domain.pod import PodList, PodItem

app = FastAPI()

packet_data = PacketList(data=[])
pod_data = PodList(pods=[])

malicious_pod = deque(maxlen=100)


class Agent_service:
    def __init__(self):
        pass

    def save_packet_data(self, packet_dict: dict):
        for packet_id, packet in packet_dict.items():
            # "Raw" 필드를 제외한 값들을 추출하여 새로운 딕셔너리에 추가
            packet_data.data.append(
                PacketItem(
                    packet_id=packet_id,
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
        #             "name": "pod_name123",
        #             "name_space": "namespace23",
        #             "ip": "ip.ip.ip.ip1",
        #             "danger_degree": "Information",
        #             "message": "Partial service may be dead or attacked; or mannual health-check is recommended",
        #         },
        #         {
        #             "id": "pod-002",
        #             "name": "pod_name456",
        #             "name_space": "namespace456",
        #             "ip": "ip.ip.ip.ip2",
        #             "danger_degree": "Fail",
        #             "message": "Partial service was dead or attacked; or should be checked mannually",
        #         },
        #         {
        #             "id": "pod-001",
        #             "name": "pod_name890",
        #             "name_space": "namespace890",
        #             "ip": "ip.ip.ip.ip3",
        #             "danger_degree": "?",
        #             "message": "Partial servicasdfsdshould be checked mannually",
        #         },
        #     ]
        # }

        for pod in pod_data.pods:
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
                    danger_degree="Trace",
                    danger_message="Trace symbol/mark",
                )
            )
        return pod_data

    def save_module_data(self, module_data: dict) -> Module:
        try:
            # module_data에 'id', 'name', 'description'가 있다고 가정합니다.
            module = Module(
                id=module_data["id"],
                name=module_data["name"],
                description=module_data["description"],
            )
            self.create_module(module)
            return module
        except Exception as e:
            # 에러를 출력하는 대신 로그에 기록하는 것이 좋습니다.
            print("모듈 데이터 저장 중 오류:", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="모듈 데이터 저장 중 오류 발생",
            )
