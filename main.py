from fastapi import FastAPI
from config.db import Base, engine, get_db
from settings.env_provider import SECRET_KEY
from src.routes.dashboard import dashboard_router
from src.routes.image_upload import image_upload_router
from src.routes.auth import auth_router
from models.admin import Admin, create_admin
from models.bucket_config import BucketConfig, Images
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(title="Image Uploader API")
Base.metadata.create_all(bind=engine)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


app.include_router(dashboard_router)
app.include_router(image_upload_router)
app.include_router(auth_router)


@app.on_event("startup")
def startup_event():
    try:
        db = next(get_db())
        msg = create_admin(db)
        print(msg)
    except Exception as e:
        raise RuntimeError("Startup failed", e)


@app.get("/root/health")
def root():
    return {"status": "ok", "message": "Application running..."}
