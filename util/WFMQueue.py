import asyncio
from collections import deque
import pywmapi as wm
from util.models.Items import DeleteOrderID
import logging

logger = logging.getLogger(__name__)

class WFMQueue:
    _instance = None

    @staticmethod
    def get_instance():
        if WFMQueue._instance is None:
            logger.debug('Returning new WFMQueue instance')
            WFMQueue._instance = WFMQueue()
        else:
            logger.debug('Returning existing WFMQueue instance')
        return WFMQueue._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(WFMQueue, cls).__new__(cls)
        return cls._instance

    def __init__(self, session):
        if not hasattr(self, 'initialized'):
            self.session = session
            self.queue = deque()
            self.lock = asyncio.Lock()
            self.rate_limit = 3  # 3 API calls per second
            self.interval = 1 / self.rate_limit  # Time interval between calls
            self.running = False
            self.worker_task = None
            self.initialized = True

    async def process_item(self, item):
        logger.debug(f'Processing item: {item} with {len(self.queue)} items remaining in queue')
        try:
            match type(item):
                case wm.orders.models.OrderNewItem:
                    wm.orders.add_order(self.session, item)
                case DeleteOrderID:
                    wm.orders.delete_order(self.session, item.order_id)
            logger.debug(f'Finished processing item: {item}')
        except Exception as e:
            logger.error(f'Error processing {item=}: {e}')
            # Continue the loop even if an error occurs
            return

    async def worker(self):
        logger.debug('Worker loop started')
        while self.running:
            async with self.lock:
                if len(self.queue) == 0:
                    logger.debug('Queue is empty, waiting for new items...')
                    await asyncio.sleep(self.interval)
                    continue
                item = self.queue.popleft()
            await self.process_item(item)
            logger.debug(f'Processed item: {item}')
            await asyncio.sleep(self.interval)
            logger.debug('Worker loop is still running')
        logger.debug('Worker loop has ended')

    def add(self, item):
        logger.debug(f'Adding item to queue: {item}')
        self.queue.append(item)
        logger.debug(f'Queue size after adding: {self.size()}')

    def size(self):
        return len(self.queue)

    async def start(self):
        logger.debug('Starting WFMQueue')
        self.running = True
        self.worker_task = asyncio.create_task(self.worker())

    async def stop(self):
        logger.debug('Stopping WFMQueue')
        self.running = False
        if self.worker_task:
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                pass
        loop = asyncio.get_event_loop()
        loop.stop()
