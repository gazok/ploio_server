from service.operation_service import packet_data
from service.operation_service import pod_data
from service.operation_service import log_data
from service.operation_service import malicious_pod


class Operation_service:
    def __init__(self):
        pass

    def get_packet_data():
        return packet_data

    def get_pod_info(pod_data, pod_namespace, pod_name):
        for pod_id, pod_info in pod_data.items():
            if pod_info["Namespace"] == pod_namespace and pod_info["Name"] == pod_name:
                return self.generate_pod_format(pod_info, self.is_malicious_pod(pod_id))
        return None

    def is_malicious_pod(pod_id):
        return pod_id in malicious_pod

    def generate_pod_format(pod_info, is_malicious: bool):
        if is_malicious:
            danger_degree = "malicous"
        else:
            danger_degree = "secure"

        return {
            "pod_info": {
                "name": pod_info["Name"],
                "name_space": pod_info["Namespace"],
                "ip": {pod_info["Network"][0]},
                "danger_degree": danger_degree,
            }
        }
