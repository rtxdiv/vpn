from fastapi import APIRouter
from root import PUBLIC_DIR


docs_router = APIRouter(prefix='/docs')

@docs_router.get('/{document}')
async def get_docs(document: str):
    return { document }