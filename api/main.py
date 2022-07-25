#!/usr/bin/env python3
import fastapi_healthcheck as healthcheck
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi import Header
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import PlainTextResponse

from api.core.settings import get_logger
from api.core.utils import valid_token
from api.db.base import *  # noqa
from api.db.session import SessionLocal, engine
from api.endpoints import users, detections

Base.metadata.create_all(bind=engine)

app = FastAPI()
logger = get_logger('main')


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


async def get_token_header(x_token: str = Header(...)):
    """
        Function that is used to validate the token in the case that it requires it
    """
    token = valid_token(x_token)
    if x_token != token:
        raise HTTPException(status_code=401, detail="X-Token header invalid")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    message = 'Request Validation Error: '
    logger.error(f'{message} exc {str(exc.detail)}')
    return PlainTextResponse(f'{message} {str(exc.detail)}', status_code=400)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    message = 'Request Validation Error: '
    logger.error(f'{message} exc {str(exc.detail)}')
    return PlainTextResponse(f'{message} exc {str(exc.detail)}', status_code=400)


class WorkerChecker(healthcheck.base.Base):
    async def check(self):
        status = False
        # code that checks health
        time_passed_for_check = 1.0
        return {
            "name": self.name,
            "status": status,
            "optional": self.optional,
            "time": time_passed_for_check
        }


healthcheck.add_health_route(app, name="FastApi", checkers=[
    healthcheck.redis.Checker(),
    WorkerChecker(name="Worker Checker")
])


app.include_router(
    users.router
)

app.include_router(
    detections.router,
    prefix="/detections",
    tags=["detections"],
    dependencies=[Depends(get_token_header)], # in case any token is used
    responses={404: {"description": "Not found"}},
)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, timeout_keep_alive=0)
