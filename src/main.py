from fastapi import FastAPI
import asyncio
from api import user, summary, dbtest
from service.summary import agent_ip, agent_port, AgentService

app = FastAPI()
app.include_router(user.router)
app.include_router(summary.router)
# app.include_router(dbtest.router)

@app.get("/")
def api_check_handler():
    return {"hello": "world"}

@app.on_event("startup")
async def startup_event():
    agent_service = AgentService(agent_ip, agent_port)
    asyncio.create_task(agent_service.send_http_get_request())
