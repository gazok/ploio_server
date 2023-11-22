from fastapi import APIRouter

router = APIRouter(prefix="/agents")


@router.post("/packet")
def rcv_packet_data():
    return


@router.post("/pod")
def rcv_pod_data():
    return


@router.post("/log")
def rcv_log_data():
    return
