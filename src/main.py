from bot import MainBot
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from auth import Validation, auth_guard
import os
import uvicorn
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR.parent / 'public'

app = FastAPI()

app.mount('/public', StaticFiles(directory=PUBLIC_DIR, html=True), name='public')
validation = Validation(os.environ['MAIN_BOT_TOKEN'])

@app.get('/')
async def get_root():
    return FileResponse(PUBLIC_DIR / 'index.html')

@app.get('/user')
@auth_guard(validation)
async def get_user(request: Request):
    return {
        'name': request.state.telegram_user.get('first_name')
    }


async def main():
    mainbot = MainBot(os.environ['MAIN_BOT_TOKEN'])
    
    config = uvicorn.Config(app, host='0.0.0.0', port=8443)
    server = uvicorn.Server(config)
    
    await asyncio.gather(
        server.serve(),
        asyncio.create_task(mainbot.run()),
        return_exceptions=True
    )

if __name__ == '__main__':
    asyncio.run(main())