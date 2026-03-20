from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from root import PUBLIC_DIR
import os


docs_router = APIRouter(prefix='/docs')

@docs_router.get('/{file}')
async def get_docs(file: str):
    path = PUBLIC_DIR / 'docs' / f'{file}.html'
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(status_code=404, detail='File not found')