from fastapi import APIRouter

from model.domain.Items import PacketList, PodList, LogList
from model.service.agent_service import Agent_service

router = APIRouter(prefix="/agents")

agent_service = Agent_service()


@router.post("/packet")
def rcv_packet_data(packet_list: PacketList):
    agent_service.save_packet_data(packet_list)
    return "success"


@router.post("/pod")
def rcv_pod_data(pod_data: PodList):
    agent_service.save_pod_data(pod_data)
    return


@router.post("/log")
def rcv_log_data(log_data: LogList):
    agent_service.save_log_data(log_data)
    return
