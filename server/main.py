from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

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


@app.get("/root/health")
async def root():
    return {"status": "ok", "message": "Application running..."}


