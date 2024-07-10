import pywmapi as wm
import logging
import util.syndicate_specific as syn
import util.util as util

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('output.log', mode='w'),
    ]
)
logger = logging.getLogger(__name__)

session = wm.auth.signin('ryanf9802@gmail.com', 'Coppernotice0101')

def main():
    syn.refresh_syndicate_orders(session, ask_to_confirm_removal=False)

if __name__ == "__main__":
    main()
