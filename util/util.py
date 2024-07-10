import pywmapi as wm
import logging
import json

item_name_to_id = {item["item_name"].lower(): item["id"] for item in json.load(open("util/ref/all_items.json"))["payload"]["items"]}
item_id_to_name = {x:y for y, x in zip(item_name_to_id.keys(), item_name_to_id.values())}

item_name_to_url = {item["item_name"].lower(): item["url_name"] for item in json.load(open("util/ref/all_items.json"))["payload"]["items"]}
item_url_to_name = {x:y for y, x in zip(item_name_to_url.keys(), item_name_to_url.values())}

item_id_to_url = {item_name_to_id[item_name]: item_name_to_url[item_name] for item_name in item_name_to_id}
item_url_to_id = {x:y for y, x in zip(item_id_to_url.keys(), item_id_to_url.values())}

logger = logging.getLogger(__name__)

def place_sell_order(session, *, item_url: str, platinum: int, quantity: int, rank: int=0, visible=True):
    new_item = wm.orders.OrderNewItem(
        item_id=item_name_to_id[item_url_to_name[item_url]],
        order_type=wm.common.OrderType.sell,
        platinum=platinum,
        quantity=quantity,
        rank=rank,
        visible=visible,
    )
    logger.info(f"Placing sell order for {quantity}x {item_url} at {platinum} platinum each")
    return wm.orders.add_order(session, new_item)

def get_sell_orders(session):
    buy_orders, sell_orders = wm.orders.get_current_orders(session)
    logger.info(f'Received {len(sell_orders)} sell orders')
    return sell_orders
