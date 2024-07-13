import asyncio
from util.WFMQueue import WFMQueue

async def main():
    queue = WFMQueue()
    queue.add('item1')
    queue.add('item2')

    queue.start()

    queue.add('item3')
    queue.add('item4')

    # Stop the queue after a delay
    await asyncio.sleep(2)
    await queue.stop()

asyncio.run(main())
