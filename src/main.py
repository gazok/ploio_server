from fastapi import FastAPI

from api import users, summary, dbtest

app = FastAPI()
app.include_router(users.router)
app.include_router(summary.router)
app.include_router(dbtest.router)

@app.get("/")
def api_check_handler():
    return {"hello": "world"}
