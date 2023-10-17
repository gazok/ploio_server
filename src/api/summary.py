from fastapi import APIRouter,Depends
from service.summary import AgentService
import json

from service.summary import parsed_data

router = APIRouter(prefix="/summary")


# 프론트 테스트를 위한 임시 api
@router.get("/tmp")
def get_agent_tmp_data():
    # sample3.bin을 갖고 테스트한 내용 반환
    # 아래 파일을 agent.json으로 바꾸면 초기 테스트용 파일을 볼 수 있음
    with open("tmp/parsed_data.json", "r") as json_file:
        data = json.load(json_file)
    return data


@router.get("/security")
def get_security_data():
     # service에서 초기화해주는 agent data buffer
    return parsed_data


@router.get("/operation")
def get_operation_data():
     # service에서 초기화해주는 agent data buffer
    return parsed_data