import pywmapi as wm
import logging
import json
import util.util as util

SYNDICATE_STANDINGS_FILE_PATH = "syndicate_standings.json"

logger = logging.getLogger(__name__)

standings = json.load(open(SYNDICATE_STANDINGS_FILE_PATH))
logger.info("Loaded user syndicate standings")

syndicates = json.load(open("util/ref/syndicates.json"))

syndicate_item_ids = []
for syndicate in syndicates:
    for item in syndicates[syndicate]["items"]:
        syndicate_item_ids.append(util.item_url_to_id[item["url_name"]])
    for mod in syndicates[syndicate]["mods"]:
        syndicate_item_ids.append(util.item_url_to_id[mod["url_name"]])
syndicate_item_ids = list(set(syndicate_item_ids))
logger.info(f"Generated list of {len(syndicate_item_ids)} syndicate item/mod IDs")

def refresh_syndicate_orders(ask_to_confirm=True):
    logger.info("Refreshing syndicate orders")
    remove_syndicate_orders(ask_to_confirm=ask_to_confirm)
    add_syndicate_orders()
    logger.info("Finished refreshing syndicate orders")


def add_syndicate_orders():
    logger.info("Adding available syndicate orders")
    valid_syndicate_standings = {
        syndicate: standings[syndicate]
        for syndicate in standings
        if standings[syndicate] > 20000
    }
    logger.info(f"User valid syndicates: {valid_syndicate_standings}")
    for syndicate in valid_syndicate_standings.keys():
        for itemobj in syndicates[syndicate]["items"]:
            if itemobj["required_standing"] == 0:
                logger.debug(
                    f'Skipping {itemobj["url_name"]} due to no standing requirement'
                )
                continue
            if itemobj["required_standing"] < standings[syndicate]:
                url_name = itemobj["url_name"]
                platinum = util.calculate_sell_price(url_name)
                if determine_worth_sell(platinum, itemobj["required_standing"]):
                    quantity = standings[syndicate] // itemobj["required_standing"]
                    util.place_sell_order(
                        item_url=url_name, platinum=platinum, quantity=quantity
                    )
                else:
                    logger.info(f"Skipping {url_name} due to low sell value")
        for modobj in syndicates[syndicate]["mods"]:
            if modobj["required_standing"] == 0:
                logger.debug(
                    f'Skipping {modobj["url_name"]} due to no standing requirement'
                )
                continue
            if modobj["required_standing"] < standings[syndicate]:
                url_name = modobj["url_name"]
                platinum = util.calculate_sell_price(url_name)
                if determine_worth_sell(platinum, modobj["required_standing"]):
                    quantity = standings[syndicate] // modobj["required_standing"]
                    util.place_sell_order(
                        item_url=url_name, platinum=platinum, rank=0, quantity=quantity
                    )
                else:
                    logger.info(f"Skipping {url_name} due to low sell value")

def determine_worth_sell(sellprice: int, standing: int):
    # Modify this value for the filter (higher number = more forgiveness)
    if standing // sellprice > 2700:
        return False
    return True


def remove_syndicate_orders(*, ask_to_confirm=True):
    logger.info("Removing syndicate orders")
    sell_orders = util.get_sell_orders()
    order_ids_to_remove = []
    for order in sell_orders:
        if order.item.id in syndicate_item_ids:
            order_ids_to_remove.append(order.id)
    logger.info(f"Found {len(order_ids_to_remove)} sell orders to remove")
    logger.debug(f"Order IDs to remove: {order_ids_to_remove}")
    if ask_to_confirm:
        choice = input(
            f"Preparing to remove {len(order_ids_to_remove)} sell orders. Continue? (y/n): "
        )
        while True:
            match choice:
                case "y" | "Y":
                    break
                case "n" | "N":
                    return
                case _:
                    choice = input('Invalid input. Please enter "y" or "n": ')
    logger.info(f"Initiating deletion of {len(order_ids_to_remove)} sell orders")
    for order_id in order_ids_to_remove:
        util.delete_order(order_id)
