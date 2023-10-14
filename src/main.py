from fastapi import FastAPI

from api import user, summary, dbtest

app = FastAPI()
app.include_router(user.router)
app.include_router(summary.router)
app.include_router(dbtest.router)

@app.get("/")
def api_check_handler():
    return {"hello": "world"}
