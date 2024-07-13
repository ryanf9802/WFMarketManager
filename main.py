import pywmapi as wm
import logging
import util.syndicate_specific as syn
from util.WFMQueue import WFMQueue
import asyncio
import util.util as util

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
    session = wm.auth.signin('ryanf9802@gmail.com', 'Coppernotice0101')
    wq = WFMQueue(session)
    wq.start()

    syn.refresh_syndicate_orders(ask_to_confirm=False)


if __name__ == "__main__":
    asyncio.run(main())
