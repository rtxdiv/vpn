from mainbot import MainBot
import asyncio
import os
from dotenv import load_dotenv

sub_path = None

async def main():
    load_dotenv()
    mainbot = MainBot()
    await mainbot.run()


if __name__ == "__main__":
    asyncio.run(main())