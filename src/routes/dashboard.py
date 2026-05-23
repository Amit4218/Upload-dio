from fastapi.routing import APIRouter

dashboard_router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@dashboard_router.get("/")
def get_metadata():
    pass
