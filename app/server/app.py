from fastapi import FastAPI

from server.routes.user import router as UserRouter

app = FastAPI()

app.include_router(UserRouter, tags=['user'], prefix='/user')

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}