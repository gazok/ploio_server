from fastapi import APIRouter, Depends
from http import HTTPStatus
from sqlalchemy.orm import Session
from model.service.agent_service import Agent_service
from database.repository import PloioRepository
from database.connection import get_ploio_db
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
        return e


@router.post("/module")
def rcv_module_data(module_data: dict, db: Session = Depends(get_ploio_db)):
    try:
        modules = ploio_repository.create_modules(module_data, db=db)
        return {
            "status": HTTPStatus.OK,
            "modules": modules,
            "message": "모듈 데이터가 성공적으로 저장되었습니다",
        }
    except HTTPException as e:
        return e
