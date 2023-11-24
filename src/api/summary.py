from fastapi import APIRouter, Depends
from model.service.operation_service import Operation_service
import json
from pathlib import Path

router = APIRouter(prefix="/summary")

operation_service = Operation_service()


@router.get("/tmp/{filename}")
def get_agent_tmp_data(filename: str):
    file_path = Path("tmp") / f"{filename}.json"

    # 샘플 데이터 반환 (log_data.json, pod_data.json, traffic_data.json)
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


@router.get("/operation")
def get_operation_data():
    return operation_service.get_packet_data()


@router.get("/operation/{pod_namespace}/{pod_name}")
def get_pod_data(pod_namespace: str, pod_name: str):
    return operation_service.get_pod_info(pod_namespace, pod_name)


@router.get("/operation/{edgeId}")
def get_log_data():
    return operation_service.get_packet_data()
