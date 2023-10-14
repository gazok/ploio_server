from fastapi import APIRouter,Depends
from service.summary import AgentService
import json

router = APIRouter(prefix="/summary")


# 프론트 테스트를 위한 임시 api
@router.get("/tmp")
def get_agent_tmp_data():
    with open("/tmp/agent.json", "r") as json_file:
        data = json.load(json_file)
    return data



@router.get("/security")
def get_security_data():
    agent_service: AgentService = Depends(),
    return "hello sec"


@router.get("/operation")
def get_operation_data():
    return "hello ops"