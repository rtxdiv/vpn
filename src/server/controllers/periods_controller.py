from fastapi import APIRouter
from fastapi.responses import FileResponse
from root import PUBLIC_DIR


periods_router = APIRouter(prefix='/periods')

@periods_router.get('/')
async def get_root():
    return FileResponse(PUBLIC_DIR / 'periods.html')