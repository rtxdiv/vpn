from xui import XUIClient
from mainbot import MainBot
import asyncio
import os
from dotenv import load_dotenv

async def main():
    load_dotenv()
    mainbot = MainBot(str(os.getenv('MAIN_BOT_TOKEN')), str(os.getenv('PANEL_HOST')) + str(os.getenv('PANEL_PATH')), str(os.getenv('PANEL_LOGIN')), str(os.getenv('PANEL_PASSWORD')))
    await mainbot.run()


if __name__ == "__main__":
    asyncio.run(main())