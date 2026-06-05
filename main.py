from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager

from src.utils.settings import settings
from src.routers.dashboard.router import dashboard_router
from src.routers.image_upload.router import image_upload_router
from src.routers.admin.router import admin_router, create_admin
from models.fastapi_settings import create_default_settings, ApplicationSettings

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_admin()
        await create_default_settings()
        yield
    except Exception as e:
        raise RuntimeError("Startup failed") from e


app = FastAPI(**ApplicationSettings().model_dump(), lifespan=lifespan)

template = Jinja2Templates(directory="templates")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


app.include_router(dashboard_router)
app.include_router(image_upload_router)
app.include_router(admin_router)


@app.get("/root/health")
async def root():
    return {"status": "ok", "message": "Application running..."}


@app.get("/")
async def home(req: Request):
    return template.TemplateResponse(request=req, name="pages/login.html")