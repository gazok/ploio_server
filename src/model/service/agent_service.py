from fastapi import FastAPI
from collections import deque
from fastapi import HTTPException, status

app = FastAPI()
from database.orm import Module
from model.domain.packet import PacketList, PacketItem
from model.domain.pod import PodList, PodItem
from model.domain.notice import NoticeList, NoticeItem

packet_data = PacketList(data=[])
pod_data = PodList(pods=[])
notice_data = NoticeList(data=[])

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
                    id = pod_id,
                    name = pod["Name"],
                    name_space = pod["Namespace"],
                    ip = (pod["Network"])[0],
                    danger_degree="Trace",
                    danger_message="Trace symbol/mark"
                )
            )
        return pod_data

    def save_log_data(self, log_list: dict):
        # pod_sample = {
        #     "pods": [
        #         {
        #             "id": "pod-123",
        #             "name": "nginx-7d9f4df5b8-abc12",
        #             "name_space": "default",
        #             "ip": "192.168.1.10",
        #             "danger_degree": "Trace",
        #             "danger_message": "Trace symbol/mark"
        #         },
        #         {
        #             "id": "pod-456",
        #             "name": "redis-6a78bde9c1-xyz34",
        #             "name_space": "app-namespace",
        #             "ip": "172.16.0.8",
        #             "danger_degree": "Trace",
        #             "danger_message": "Trace symbol/mark"
        #         },
        #         {
        #             "id": "pod-789",
        #             "name": "mysql-2e8cfb1a3d-pqr56",
        #             "name_space": "database",
        #             "ip": "1.1.1.1",
        #             "danger_degree": "Trace",
        #             "danger_message": "Trace symbol/mark"
        #         }
        #     ]
        # }
        # packet_sample = {
        #     "data": [
        #         {
        #             "packet_id": "pod-123",
        #             "src_pod": "default:front-end3",
        #             "dst_pod": "default:api-server",
        #             "timestamp": "12341234",
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
                        for packet in packet_data.data:
                            notice_data.data.append(
                                NoticeItem(
                                    packet_id=packet_id,
                                    src_pod=packet["src_pod"],
                                    dst_pod=packet["dst_pod"],
                                    timestamp=packet["timestamp"],
                                    data_len=packet["data_len"],
                                    danger_degree=code,
                                    danger_message=log_entry.get("Message", ""),
                                )
                            )
        for log_pod in notice_data.data:
            for saved_pod in pod_data.pods:
                if log_pod.packet_id == saved_pod["id"]:
                    saved_pod["danger_degree"] = log_pod.danger_degree
                    saved_pod["danger_message"] = log_pod.danger_message
        return notice_data

    
    def save_module_data(self, module_data: dict) -> Module:
        try:
            # module_data에 'id', 'name', 'description'가 있다고 가정합니다.
            module = Module(
                id=module_data['id'],
                name=module_data['name'],
                description=module_data['description']
            )
            self.create_module(module)
            return module
        except Exception as e:
            # 에러를 출력하는 대신 로그에 기록하는 것이 좋습니다.
            print("모듈 데이터 저장 중 오류:", e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="모듈 데이터 저장 중 오류 발생")


    def convert_json_to_modules(self, json_data):
        modules = []
        for module_data in json_data.get("modules", []):
            module = Module(
                id=module_data.get("GUID"),
                name=module_data.get("Name"),
                description=module_data.get("Description")
            )
            modules.append(module)
        return modules