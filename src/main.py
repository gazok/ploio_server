from fastapi import FastAPI
from api import user, summary, agents, notice, management
from fastapi.middleware.cors import CORSMiddleware

from database.connection import engine, Base

app = FastAPI()
app.include_router(user.router)
app.include_router(summary.router)
app.include_router(agents.router)
app.include_router(notice.router)
app.include_router(management.router)
origins = ["http://localhost/", "http://localhost:3000/"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)
Base.metadata.create_all(bind=engine)


@app.get("/")
def api_check_handler():
    return {"hello": "world"}
