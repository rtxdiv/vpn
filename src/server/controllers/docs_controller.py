from fastapi import APIRouter
from fastapi.responses import FileResponse
from root import PUBLIC_DIR


docs_router = APIRouter(prefix='/docs')

@docs_router.get('/{file}')
async def get_docs(file: str):
    return FileResponse(PUBLIC_DIR / 'docs' / f'{file}.html')