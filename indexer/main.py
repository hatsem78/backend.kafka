#!/usr/bin/env python3
import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
import fastapi_healthcheck as healthcheck
from uvicorn.middleware.debug import PlainTextResponse

from core.settings import get_logger
from core.utils import valid_token
from db.base_class import Base
from db.session import engine
from endpoints import items

Base.metadata.create_all(bind=engine)

app = FastAPI()
logger = get_logger('main')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    items.router,
    prefix="/items",
    tags=["items"],
    #dependencies=[Depends(get_token_header)], # in case any token is used
    responses={404: {"description": "Not found"}},
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8007, timeout_keep_alive=0)
