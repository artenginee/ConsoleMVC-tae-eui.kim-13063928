import math
from collections import deque

from interfaces.i_production_controller import IProductionController
from models.production_job import ProductionJob


class ProductionController(IProductionController):

    def __init__(self):
        self._queue: deque[ProductionJob] = deque()
        self._current: ProductionJob | None = None
        self._counter = 1

    def enqueue(self, order_id: str, sample_id: str, shortfall: int,
                yield_rate: float, avg_production_time: float) -> ProductionJob:
        actual_qty = math.ceil(shortfall / (yield_rate * 0.9))
        job = ProductionJob(
            job_id=f"J{self._counter:04d}",
            order_id=order_id,
            sample_id=sample_id,
            shortfall=shortfall,
            actual_production_qty=actual_qty,
            total_production_time=avg_production_time * actual_qty,
        )
        self._counter += 1
        self._queue.append(job)
        self._try_start_next()
        return job

    def get_current(self) -> ProductionJob | None:
        return self._current

    def get_queued(self) -> list[ProductionJob]:
        return list(self._queue)

    def complete_current(self) -> ProductionJob | None:
        if not self._current:
            return None
        completed = self._current
        completed.produced_qty = completed.actual_production_qty
        completed.is_in_progress = False
        self._current = None
        self._try_start_next()
        return completed

    def _try_start_next(self):
        if self._current is None and self._queue:
            self._current = self._queue.popleft()
            self._current.is_in_progress = True
