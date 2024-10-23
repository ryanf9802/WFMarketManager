import pywmapi as wm
import logging
import json
from util.WFMQueue import WFMQueue
from util.models.Items import DeleteOrderID

item_name_to_id = {item["item_name"].lower(): item["id"] for item in json.load(open("util/ref/all_items.json"))["payload"]["items"]}
item_id_to_name = {x:y for y, x in zip(item_name_to_id.keys(), item_name_to_id.values())}

item_name_to_url = {item["item_name"].lower(): item["url_name"] for item in json.load(open("util/ref/all_items.json"))["payload"]["items"]}
item_url_to_name = {x:y for y, x in zip(item_name_to_url.keys(), item_name_to_url.values())}

item_id_to_url = {item_name_to_id[item_name]: item_name_to_url[item_name] for item_name in item_name_to_id}
item_url_to_id = {x:y for y, x in zip(item_id_to_url.keys(), item_id_to_url.values())}

logger = logging.getLogger(__name__)

def calculate_sell_price(item_url: str):
    return 10000 # temporary placeholder

def place_sell_order(*, item_url: str, rank=None, platinum: int, quantity: int, visible=True):
    wq = WFMQueue.get_instance()
    new_item = wm.orders.OrderNewItem(
        item_id=item_name_to_id[item_url_to_name[item_url]],
        order_type=wm.common.OrderType.sell,
        platinum=platinum,
        rank=rank,
        quantity=quantity,
        visible=visible,
    )
    wq.add(new_item)
    #logger.info(f"Placing sell order for {quantity}x {item_url} at {platinum} platinum each {visible=}")

def delete_order(order_id):
    wq = WFMQueue.get_instance()
    wq.add(DeleteOrderID(order_id))

def get_sell_orders():
    wq = WFMQueue.get_instance()
    session = wq.session
    buy_orders, sell_orders = wm.orders.get_current_orders(session)
    logger.info(f'Received {len(sell_orders)} sell orders')
    return sell_orders
