import requests
import json
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('output.log'),
        logging.StreamHandler()
    ]
)

with open("token.json") as f:
    token = json.load(f)

market = requests.Session()
market.headers.update({
    "content-type": "application/json",
    "accept": "application/json",
    "platform": "pc",
    "language": "en"
})

market.base_url = "https://api.warframe.market/v1"

# Create a client instance for authorized requests
nkn1396 = requests.Session()
nkn1396.headers.update({
    "content-type": "application/json",
    "accept": "application/json",
    "platform": "pc",
    "language": "en",
    "authorization": f"JWT {token}"
})
nkn1396.base_url = "https://api.warframe.market/v1"

def post_order(item_id: str, platinum: int, quantity: int, rank: int, visible: bool=True):
    order_data = {
        "order_type": "sell",
        "item_id": item_id,
        "platinum": platinum,
        "quantity": quantity,
        "visible": visible,
        "rank": rank
    }
    try:
        response = nkn1396.post(f"{nkn1396.base_url}/profile/orders", json=order_data)
        response.raise_for_status()
        print("SUCCESS!")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def main():
    post_order()

if __name__ == '__main__':
    main()

