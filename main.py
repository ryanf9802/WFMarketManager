import pywmapi as wm
import logging
import util.syndicate_specific as syn
from util.WFMQueue import WFMQueue
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

# Clear log file
open('output.log', 'w').close()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('output.log',),
    ]
)
logger = logging.getLogger(__name__)


async def main():
    session = wm.auth.signin(os.environ.get("USERNAME"), os.environ.get("PASSWORD"))
    wq = WFMQueue(session)
    asyncio.run(wq.start())

    syn.refresh_syndicate_orders(ask_to_confirm=True)


if __name__ == "__main__":
    asyncio.run(main())
