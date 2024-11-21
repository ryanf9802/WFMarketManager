import asyncio
from collections import deque
import pywmapi as wm
from util.models.Items import DeleteOrderID
from util.StatusModel import StatusModel
import logging
import sys

logger = logging.getLogger(__name__)


class WFMQueue:
    _instance = None

    @staticmethod
    def get_instance():
        if WFMQueue._instance is None:
            logger.debug("Returning new WFMQueue instance")
            WFMQueue._instance = WFMQueue()
        else:
            logger.debug("Returning existing WFMQueue instance")
        return WFMQueue._instance

    @staticmethod
    def size():
        return WFMQueue.get_instance().get_queue_size()
    
    @staticmethod
    def queue_is_empty() -> bool:
        return WFMQueue.size() == 0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(WFMQueue, cls).__new__(cls)
        return cls._instance

    def __init__(self, session):
        if not hasattr(self, "initialized"):
            self.session = session
            self.queue = deque()
            self.lock = asyncio.Lock()
            self.rate_limit = 3  # 3 API calls per second
            self.interval = 1 / self.rate_limit  # Time interval between calls
            self.running = False
            self.worker_task = None
            self.initialized = True
            self.status_model = StatusModel.get_instance()

    def get_queue_size(self):
        return len(self.queue)

    async def display_queue_size(self):
        while self.running:
            sys.stdout.write(f"\r{self.status_model.status_message}")
            sys.stdout.flush()
            await asyncio.sleep(1)

    async def process_item(self, item):

        logger.debug(
            f"Processing item: {item} with {len(self.queue)} items remaining in queue"
        )
        try:
            match type(item):
                case wm.orders.models.OrderNewItem:
                    wm.orders.add_order(self.session, item)
                case DeleteOrderID:
                    wm.orders.delete_order(self.session, item.order_id)
            logger.debug(f"Finished processing item: {item}")
        except Exception as e:
            logger.error(f"Error processing {item=}: {e}")
            # Continue the loop even if an error occurs
            return

    async def worker(self):
        logger.debug("Worker loop started")
        while self.running:
            async with self.lock:
                if len(self.queue) == 0:
                    logger.debug("Queue is empty, waiting for new items...")
                    
                    StatusModel.set_status_message(f"Queue size: {self.size()}")
                    StatusModel.display()

                    await asyncio.sleep(self.interval)
                    logger.debug(f"Worker sleep for {self.interval} seconds")
                    continue
                item = self.queue.popleft()

            StatusModel.set_status_message(f"Queue size: {self.size()}")
            StatusModel.display()

            start_time = asyncio.get_event_loop().time()
            await self.process_item(item)
            end_time = asyncio.get_event_loop().time()
            logger.info(f"Processed item {item} in time: {end_time - start_time}")
            logger.debug(f"Worker sleep for {self.interval} seconds")
        logger.debug("Worker loop has ended")

    def add(self, item):
        logger.debug(f"Adding item to queue: {item}")
        self.queue.append(item)
        logger.debug(f"Queue size after adding: {self.size()}")
        
    async def start(self):
        logger.debug("Starting WFMQueue")
        self.running = True
        self.worker_task = asyncio.create_task(self.worker())

    async def stop(self):
        logger.debug("Stopping WFMQueue")
        self.running = False

        if self.worker_task:
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                pass

        loop = asyncio.get_event_loop()
        loop.stop()
