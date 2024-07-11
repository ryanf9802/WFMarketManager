import pywmapi as wm
import logging
import util.syndicate_specific as syn
from util.WFMQueue import WFMQueue

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


def main():
    session = wm.auth.signin('ryanf9802@gmail.com', 'Coppernotice0101')
    wq = WFMQueue()
    wq.start()
    syn.refresh_syndicate_orders(session, ask_to_confirm_removal=False)

if __name__ == "__main__":
    main()
