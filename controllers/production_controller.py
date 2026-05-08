import math
from collections import deque
from typing import List, Optional
from models.production_job import ProductionJob


class ProductionController:
    """생산 큐(FIFO) 및 현재 생산 작업 관리"""

    def __init__(self):
        self._queue: deque[ProductionJob] = deque()
        self._current: Optional[ProductionJob] = None
        self._counter = 1

    # ── 생산 작업 등록 ─────────────────────────────────────────────────

    def enqueue(self, order_id: str, sample_id: str, shortfall: int,
                yield_rate: float, avg_production_time: float) -> ProductionJob:
        # 실 생산량 = ceil(부족분 / (수율 × 0.9))
        actual_qty = math.ceil(shortfall / (yield_rate * 0.9))
        total_time = avg_production_time * actual_qty

        job = ProductionJob(
            job_id=f"J{self._counter:04d}",
            order_id=order_id,
            sample_id=sample_id,
            shortfall=shortfall,
            actual_production_qty=actual_qty,
            total_production_time=total_time,
        )
        self._counter += 1
        self._queue.append(job)
        self._try_start_next()
        return job

    def _try_start_next(self):
        if self._current is None and self._queue:
            self._current = self._queue.popleft()
            self._current.is_in_progress = True

    # ── 조회 ──────────────────────────────────────────────────────────

    def get_current(self) -> Optional[ProductionJob]:
        return self._current

    def get_queued(self) -> List[ProductionJob]:
        return list(self._queue)

    # ── 생산 완료 처리 ─────────────────────────────────────────────────

    def complete_current(self) -> Optional[ProductionJob]:
        if not self._current:
            return None
        completed = self._current
        completed.produced_qty = completed.actual_production_qty
        completed.is_in_progress = False
        self._current = None
        self._try_start_next()
        return completed
