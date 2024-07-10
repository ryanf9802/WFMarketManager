import pywmapi as wm
import logging
import json
import util.util as util

SYNDICATE_STANDINGS_FILE_PATH = "syndicate_standings.json"

logger = logging.getLogger(__name__)

standings = json.load(open(SYNDICATE_STANDINGS_FILE_PATH))
logger.info('Loaded user syndicate standings')

syndicates = json.load(open("util/ref/syndicates.json"))
# get number of syndicate items
num_syndicate_items = 0
for syndicate in syndicates:
    num_syndicate_items += len(syndicates[syndicate])
logger.info(f'Loaded syndicate items')

syndicate_item_ids = []
for syndicate in syndicates:
    for index, item in enumerate(syndicates[syndicate]):
        syndicate_item_ids.append(util.item_url_to_id[item["url_name"]])
logger.info(f'Generated list of {len(syndicate_item_ids)} syndicate item IDs')

def refresh_syndicate_orders(session, ask_to_confirm_removal=True):
    logger.info('Refreshing syndicate orders')
    remove_syndicate_orders(session, ask_to_confirm=ask_to_confirm_removal)
    add_syndicate_orders(session)
    logger.info('Finished refreshing syndicate orders')

def add_syndicate_orders(session):
    logger.info('Adding available syndicate orders')
    valid_syndicate_standings = {syndicate:standings[syndicate] for syndicate in standings if standings[syndicate] > 20000}
    logger.info(f'User valid syndicates: {valid_syndicate_standings}')
    created_orders = []
    for syndicate in valid_syndicate_standings.keys():
        for itemobj in syndicates[syndicate]:
            if itemobj['required_standing'] == 0:
                logger.debug(f'Skipping {itemobj["url_name"]} due to no standing requirement')
                continue
            if itemobj['required_standing'] < standings[syndicate]:
                url_name = itemobj['url_name']
                platinum = util.calculate_sell_price(session, url_name)
                quantity = standings[syndicate] // itemobj['required_standing']
                created_orders.append(util.place_sell_order(session, 
                                      item_url=url_name, 
                                      platinum=platinum, 
                                      quantity=quantity))
    logger.info(f'Added {len(created_orders)} orders')
    logger.debug(f'Order IDs: {[order.id for order in created_orders]}')

def remove_syndicate_orders(session, *, ask_to_confirm=True):
    sell_orders = util.get_sell_orders(session)
    order_ids_to_remove = []
    for order in sell_orders:
        if order.item.id in syndicate_item_ids:
            order_ids_to_remove.append(order.id)
    logger.info(f'Found {len(order_ids_to_remove)} sell orders to remove')
    logger.debug(f'Order IDs to remove: {order_ids_to_remove}')
    if ask_to_confirm:
        choice = input(f'Preparing to remove {len(order_ids_to_remove)} sell orders. Continue? (y/n): ')
        while True:
            match choice:
                case 'y' | 'Y':
                    break
                case 'n' | 'N':
                    return
                case _:
                    choice = input('Invalid input. Please enter "y" or "n": ')
    for order_id in order_ids_to_remove:
        wm.orders.delete_order(session, order_id)
    logger.info(f'Successfully deleted {len(order_ids_to_remove)} orders')
