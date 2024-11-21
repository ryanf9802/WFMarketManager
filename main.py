import pywmapi as wm
import logging
import util.syndicate_specific as syn
from util.WFMQueue import WFMQueue
import asyncio
from dotenv import load_dotenv
import os
import sys
from util.util import get_sell_orders

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
    os.system('cls')

    username = os.environ.get("EMAIL")
    password = os.environ.get("PASSWORD")

    print(f"{username} {password}")

    logger.info(f"Starting session as user {username}")
    session = wm.auth.signin(username, password)

    wq = WFMQueue(session)
    await wq.start()

    while True:
        print(f"{len(get_sell_orders())} Sell Orders\n")
        userin = input("[0] Remove Current Syndicate Orders\n[1] Add Syndicate Orders\n[2] Refresh Orders\n[3] Quit\n")
        match userin:
            case "0":
                syn.remove_syndicate_orders(ask_to_confirm=False)
            case "1":
                syn.add_syndicate_orders()
            case "2":
                syn.remove_syndicate_orders(ask_to_confirm=False)
                syn.add_syndicate_orders()
            case "3":
                await wq.stop()
                os.system('cls')
                sys.exit(0)
            case _:
                print("Invalid Input")
                input("Enter to continue")
        while not WFMQueue.queue_is_empty():
            await asyncio.sleep(1)
        os.system('cls')

if __name__ == "__main__":
    asyncio.run(main())
