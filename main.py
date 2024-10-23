import pywmapi as wm
import logging
import util.syndicate_specific as syn
from util.WFMQueue import WFMQueue
from util.StatusModel import StatusModel
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

# Clear log file
open("output.log", "w").close()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            "output.log",
        ),
    ],
)
logger = logging.getLogger(__name__)


async def main():
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")

    logger.info(f"Starting session as user {username}")
    session = wm.auth.signin(username, password)

    wq = WFMQueue(session)
    await wq.start()

    syn.remove_syndicate_orders(ask_to_confirm=False)
    syn.add_syndicate_orders()

    await wq.stop()


if __name__ == "__main__":
    asyncio.run(main())
