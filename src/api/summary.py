from fastapi import APIRouter, Depends
from service.summary import AgentService
import json

from service.summary import parsed_data
from service.summary import packet_data
from service.summary import pod_data
from service.summary import log_data

from service.summary import malicious_pod

router = APIRouter(prefix="/summary")


# 프론트 테스트를 위한 임시 api
@router.get("/tmp/{filename}")
def get_agent_tmp_data(filename: str):
    # 샘플 데이터 반환 (log_data.json, pod_data.json, traffic_data.json)
    with open("tmp/{filename}.json", "r") as json_file:
        data = json.load(json_file)
    return data


@router.get("/security")
def get_packet_data():
    return packet_data


@router.get("/security/{podNamespace}/{podName}")
def get_pod_data(podNamespace: str, podName: str):
    return find_pod_info(pod_data, podNamespace, podName)


def find_pod_info(pod_data, podNamespace, podName):
    for pod_id, pod_info in pod_data.items():
        if pod_info["Namespace"] == podNamespace and pod_info["Name"] == podName:
            return generate_pod_format(pod_info, is_malicious_pod(pod_id))
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


@router.get("/security/{edgeId}")
def get_log_data():
    result = []

    for log_id, log_info in log_data.items():
        for ref in log_info["Refs"]:
            if ref["Source"] == "Packet":
                packet_id = ref["Identifier"]

                if packet_id in packet_data:
                    packet_info = packet_data[packet_id]
                    src_pod = packet_info["Source"]
                    dst_pod = packet_info["Destination"]

                    if src_pod in packet_data and dst_pod in packet_data:
                        src_pod_info = packet_data[src_pod]
                        dst_pod_info = packet_data[dst_pod]

                        src_pod_name_namespace = (
                            f"{src_pod_info['Name']}:{src_pod_info['Namespace']}"
                        )
                        dst_pod_name_namespace = (
                            f"{dst_pod_info['Name']}:{dst_pod_info['Namespace']}"
                        )

                        data_len = int(packet_info["Size"])

                        result.append(
                            {
                                "data": {
                                    "src_pod": src_pod_name_namespace,
                                    "dst_pod": dst_pod_name_namespace,
                                    "data_len": data_len,
                                }
                            }
                        )

    return result


@router.get("/operation")
def get_operation_data():
    # service에서 초기화해주는 agent data buffer
    return parsed_data


# @router.get("/security")
# def get_security_data():
#     # service에서 초기화해주는 agent data buffer
#     return parsed_data
