from fastapi import FastAPI
from fastapi import HTTPException, status
from database.connection import Module
from model.domain.packet import PacketList, PacketItem
from model.domain.pod import PodList, PodItem
from kubernetes import config, client

app = FastAPI()

packet_data = PacketList(packets=[])
pod_data = PodList(pods=[])


class Agent_service:
    def __init__(self):
        pass

    def save_packet_data(self, packet_dict: dict):
        for packet_id, packet in packet_dict.items():
            # "Raw" 필드를 제외한 값들을 추출하여 새로운 딕셔너리에 추가
            packet_data.packets.append(
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
                    type=self.get_pod_type(pod["Name"], pod["Namespace"]),
                    ip=(pod["Network"])[0],
                    danger_degree="Trace",
                    danger_message="Trace symbol/mark",
                )
            )
        return pod_data

    def get_pod_type(self, pod_name: str, pod_namespace: str):
        pod_port = self.get_pod_ports(pod_name, pod_namespace)
        server_port = [53, 9153, 443, 8000, 80, 6379]
        database_port = [27017, 3306]
        if pod_port in server_port:
            return "server"
        if pod_port in database_port:
            return "database"
        return None

    def get_pod_ports(self, pod_name: str, pod_namespace: str):
        config.load_kube_config()
        api_instance = client.CoreV1Api()
        try:
            pod = api_instance.read_namespaced_pod(
                name=pod_name, namespace=pod_namespace
            )
            return pod.spec.containers[0]["ports"][0]["container_port"]

        except Exception as e:
            print(f"Error fetching pod information: {str(e)}")

    def save_module_data(self, module_data: dict) -> Module:
        try:
            module = Module(
                id=module_data["id"],
                name=module_data["name"],
                description=module_data["description"],
            )
            self.create_module(module)
            return module
        except Exception as e:
            print("모듈 데이터 저장 중 오류:", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="모듈 데이터 저장 중 오류 발생",
            )
