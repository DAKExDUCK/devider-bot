import asyncio
from modules.bot import start_bot
from modules.db import DB
from modules.logger import logger


if __name__ == "__main__":
    while 1:
        try:
            DB.init()
            asyncio.run(start_bot())
        except Exception as exc:
            logger.error(str(exc), exc_info=True)