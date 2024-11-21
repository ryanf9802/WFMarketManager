import pywmapi as wm
import logging
import util.syndicate_specific as syn
from util.WFMQueue import WFMQueue
import asyncio
from dotenv import load_dotenv
import os
import sys
from util.util import get_sell_orders

async def main():
  username = os.environ.get("EMAIL")
  password = os.environ.get("PASSWORD")

  session = wm.auth.signin(username, password)
  stats = wm.statistics.get_statistic("vampire_leech").closed_48h

  sum = 0
  for i in stats:
    sum += i.volume
  print(sum)

if __name__ == '__main__':
  load_dotenv()
  asyncio.run(main())