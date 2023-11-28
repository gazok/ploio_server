from fastapi import APIRouter

router = APIRouter()
from model.service.operation_service import Operation_service

operation_service = Operation_service()


@router.get("/management")
def get_module_data():
    return operation_service.get_module_data()

@router.post("/management")
def update_module_status():
    return operation_service.update_module_status()