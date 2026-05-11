import logging
from time import perf_counter

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.category import router as category_router
from app.api.routers.task import router as task_router
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()


# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     Base.metadata.create_all(bind=engine)
#     yield

requestCounter = 0

app = FastAPI()
logger = logging.getLogger("middleware")


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_allowed_origin,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.middleware(
    "http"
)  # log_requests выполнится до и после обработки каждого HTTP-запроса
async def log_requests(request: Request, call_next) -> Response:
    global requestCounter
    requestCounter += 1
    ip_address = request.client.host if request.client is not None else "127.0.0.1"

    started_at = perf_counter()

    try:
        response: Response = await call_next(request)  # Работа самого эндпоинта
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    response.headers["X-Request-Number"] = str(requestCounter)
    duration_ms = (perf_counter() - started_at) * 1000
    logger.info(
        "%s %s -> %s (%.2f ms) | %s",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
        ip_address,
    )
    return response


app.include_router(task_router)
app.include_router(category_router)
