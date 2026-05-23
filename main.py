from fastapi import FastAPI
from config.db import Base, engine
from src.routes.dashboard import dashboard_router
from src.routes.image_upload import image_upload_router


app = FastAPI(title="Image Uploader API")
Base.metadata.create_all(bind=engine)  # create the db and the tables


app.include_router(dashboard_router)
app.include_router(image_upload_router)


@app.get("/root/health")
def root():
    return {"status": "ok", "message": "Application running..."}
