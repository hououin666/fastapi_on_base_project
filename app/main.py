from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, APIRouter
from api import router as api_router
from core.config import settings
from core.models.db_helper import db_helper

main_app = FastAPI()
main_app.include_router(api_router)


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield
    db_helper.dispose()


@main_app.get("/")
async def root():
    return {"message": "Hello World"}


@main_app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == '__main__':
    uvicorn.run('main:main_app', reload=True, host=settings.run.host, port=settings.run.port)

