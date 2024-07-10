import pywmapi as wm
import logging
import util
from ref.ref import updateRefs, syndicate_items

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('output.log', mode='w'),
    ]
)

logger = logging.getLogger(__name__)

session = wm.auth.signin('ryanf9802@gmail.com', 'Coppernotice0101')

standing = {
    "steel_meridian": 0,
    "cephalon_suda": 0,
    "perrin_sequence": 0,
    "red_veil": 0,
    "new_loka": 0,
    "arbiters_of_hexis": 0,
}

def main():
    updateRefs()
    print(util.get_sell_orders(session))

if __name__ == "__main__":
    main()
