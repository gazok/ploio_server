from fastapi import APIRouter

router = APIRouter(prefix="/summary")


@router.get("/security")
def get_security_data():
    return "hello sec"


@router.get("/operation")
def get_operation_data():
    return "hello ops"