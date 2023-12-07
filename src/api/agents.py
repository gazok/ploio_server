from fastapi import APIRouter, Depends
from http import HTTPStatus
from sqlalchemy.orm import Session
from model.service.agent_service import Agent_service
from database.repository import PloioRepository
from database.connection import get_ploio_db, Module
from fastapi import HTTPException


router = APIRouter(prefix="/agents")

agent_service = Agent_service()
ploio_repository = PloioRepository(session=Depends(get_ploio_db))


@router.post("/packet")
def rcv_packet_data(packet_list: dict):
    agent_service.save_packet_data(packet_list)
    return HTTPStatus.OK


@router.post("/pod")
def rcv_pod_data(pod_data: dict):
    agent_service.save_pod_data(pod_data)
    return HTTPStatus.OK


@router.post("/log")
def rcv_log_data(log_data: dict, db: Session = Depends(get_ploio_db)):
    try:
        notices = ploio_repository.create_notice(log_data, db=db)
        return {
            "status": HTTPStatus.OK,
            "notices": notices,
            "message": "log 데이터가 성공적으로 저장되었습니다",
        }
    except HTTPException as e:
        return {"code": e.status_code, "message": e.args[0]}


@router.post("/activation")
def return_module_status(request: dict, db: Session = Depends(get_ploio_db)):
    try:
        guid = request["guid"]
        module = db.query(Module).filter(Module.guid == guid).first()
        return {
            "guid": module.guid,
            "status": module.status
        }
    except HTTPException as e:
        return {"code": e.status_code, "message": e.args[0]}
