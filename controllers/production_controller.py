from collections import deque
from models.production_job import ProductionJob


class ProductionController:

    def __init__(self):
        self._queue: deque[ProductionJob] = deque()
        self._current: ProductionJob | None = None

    def enqueue(self, order_id: str, sample_id: str, shortfall: int,
                yield_rate: float, avg_production_time: float) -> ProductionJob:
        pass

    def get_current(self) -> ProductionJob | None:
        pass

    def get_queued(self) -> list[ProductionJob]:
        pass

    def complete_current(self) -> ProductionJob | None:
        pass
