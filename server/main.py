from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse

from src.utils.admin import create_default_admin
from src.routers.admin import admin_router
from src.routers.file_upload import file_upload_router
from src.routers.dashboard import dashboard_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_default_admin()
        yield
    except Exception as e:
        raise RuntimeError("Startup failed") from e


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(admin_router)
app.include_router(file_upload_router)
app.include_router(dashboard_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "statusCode": exc.status_code,
            "detail": exc.detail,
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "statusCode": 422,
            "detail": "Validation failed",
        },
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "statusCode": 500,
            "detail": "Internal Server Error",
        },
    )


@app.get("/root/health")
async def root():
    return {"status": "ok", "message": "Application running..."}


