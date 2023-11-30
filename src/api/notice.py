from fastapi import APIRouter

from model.service.agent_service import notice_data

router = APIRouter()


@router.get("/notice")
def get_notice_data():
    return notice_data
