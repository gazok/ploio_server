from fastapi import FastAPI
from api import user, summary, dbtest
from fastapi.middleware.cors import CORSMiddleware

from service.summary import agent_ip, agent_port, AgentService, fetching_process

import requests
import asyncio

app = FastAPI()
app.include_router(user.router)
app.include_router(summary.router)
# app.include_router(dbtest.router)
origins = [
    "http://localhost/",
    "http://localhost:3000/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)

@app.get("/")
def api_check_handler():
    return {"hello": "world"}


@app.on_event("startup")
async def startup_event():
    # fetching process를 fastapi 서버가 올라가는 동시에 실행
    asyncio.create_task(fetching_process())