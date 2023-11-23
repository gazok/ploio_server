from fastapi import APIRouter
from http import HTTPStatus

from model.domain.packet import PacketItem
from model.domain.pod import PodList
from model.domain.log import LogList
from model.service.agent_service import Agent_service

router = APIRouter(prefix="/agents")

agent_service = Agent_service()


@router.post("/packet")
def rcv_packet_data(packet_list: dict):
    return agent_service.save_packet_data(packet_list)


@router.post("/pod")
def rcv_pod_data(pod_data: PodList):
    agent_service.save_pod_data(pod_data)
    return HTTPStatus.OK


@router.post("/log")
def rcv_log_data(log_data: LogList):
    agent_service.save_log_data(log_data)
    return HTTPStatus.OK
