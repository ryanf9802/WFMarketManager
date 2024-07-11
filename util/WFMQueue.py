import asyncio
from collections import deque

class WFMQueue:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(WFMQueue, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.queue = deque()
            self.lock = asyncio.Lock()
            self.rate_limit = 3  # 3 API calls per second
            self.interval = 1 / self.rate_limit  # Time interval between calls
            self.initialized = True

    async def process_item(self, item):
        # Implement the actual processing of the item
        pass

    async def worker(self):
        while True:
            async with self.lock:
                if len(self.queue) == 0:
                    await asyncio.sleep(self.interval)
                    continue
                item = self.queue.popleft()
            await self.process_item(item)
            await asyncio.sleep(self.interval)

    def add(self, item):
        self.queue.append(item)

    def size(self):
        return len(self.queue)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.worker())
        loop.run_forever()
