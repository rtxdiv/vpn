from bot import MainBot
from xui import XUIClient
import asyncio
from fastapi import FastAPI, Request, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from auth import Validation, create_auth_guard
import os
import uvicorn
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR.parent / 'public'

app = FastAPI()
xui = XUIClient()
xui.login()

app.mount('/public', StaticFiles(directory=PUBLIC_DIR, html=True), name='public')
validation = Validation(os.environ['MAIN_BOT_TOKEN'])
auth_guard = create_auth_guard(validation)

@app.get('/')
async def get_root():
    return FileResponse(PUBLIC_DIR / 'index.html')

@app.get('/user')
async def get_user(request: Request, _=Depends(auth_guard)):
    user = await xui.get_by_tgid(request.state.telegram_user['id'])
    return user
    


async def main():
    mainbot = MainBot(os.environ['MAIN_BOT_TOKEN'])
    
    config = uvicorn.Config(app, host='0.0.0.0', port=8443)
    server = uvicorn.Server(config)
    await xui.login()
    
    await asyncio.gather(
        server.serve(),
        # asyncio.create_task(mainbot.run()),
        return_exceptions=True
    )

if __name__ == '__main__':
    asyncio.run(main())