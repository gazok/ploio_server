from model.service.agent_service import packet_data
from model.service.agent_service import pod_data


class Operation_service:
    def __init__(self):
        pass

    def get_packet_data(self):
        return packet_data

    def get_pod_info(self, pod_namespace, pod_name):
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
        for pod_info in pod_data.pods:
            if pod_info["name_space"] == pod_namespace and pod_info["name"] == pod_name:
                return pod_info
        return None