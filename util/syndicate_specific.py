import pywmapi as wm
import logging
import json
import util.util as util

SYNDICATE_STANDINGS_FILE_PATH = "syndicate_standings.json"

logger = logging.getLogger(__name__)

standings = json.load(open(SYNDICATE_STANDINGS_FILE_PATH))
logger.info('Loaded user syndicate standings')

syndicate_items = json.load(open("util/ref/syndicate_items.json"))
logger.info('Loaded syndicate items')

syndicate_item_ids = []
for syndicate in syndicate_items:
    for index, item in enumerate(syndicate_items[syndicate]):
        syndicate_item_ids.append(util.item_url_to_id[item["url_name"]])
print(syndicate_item_ids)

def remove_syndicate_orders(session):
    sell_orders = util.get_sell_orders(session)
    for order in sell_orders:
        if order.item_id in [syndicate["id"] for syndicate in syndicate_items]:
            wm.orders.remove_order(session, order.id)
            logger.info(f'Removed order for {util.item_id_to_name[order.item_id]}')

