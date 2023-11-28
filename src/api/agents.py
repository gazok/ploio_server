from fastapi import APIRouter
from http import HTTPStatus

from model.domain.pod import PodList
from model.service.agent_service import Agent_service

router = APIRouter(prefix="/agents")

agent_service = Agent_service()


@router.post("/packet")
def rcv_packet_data(packet_list: dict):
    agent_service.save_packet_data(packet_list)
    return HTTPStatus.OK


@router.post("/pod")
def rcv_pod_data(pod_data: dict):
    agent_service.save_pod_data(pod_data)
    return HTTPStatus.OK


@router.post("/log")
def rcv_log_data(log_data: dict):
    agent_service.save_log_data(log_data)
    return HTTPStatus.OK
