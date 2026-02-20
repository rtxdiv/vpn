from xui import XUIClient
from mainbot import MainBot
import asyncio
import os
from dotenv import load_dotenv

sub_path = None

async def main():
    load_dotenv()
    sub_host = str(os.getenv('PANEL_SUB_HOST'))
    mainbot = MainBot(str(os.getenv('MAIN_BOT_TOKEN')), str(os.getenv('PANEL_HOST')) + '/' + str(os.getenv('PANEL_PATH')), str(os.getenv('PANEL_LOGIN')), str(os.getenv('PANEL_PASSWORD')), sub_host)
    await mainbot.run()


if __name__ == "__main__":
    asyncio.run(main())