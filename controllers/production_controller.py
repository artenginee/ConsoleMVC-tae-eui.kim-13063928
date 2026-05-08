import math
from collections import deque

from interfaces.i_production_controller import IProductionController
from models.production_job import JobStatus, ProductionJob


class ProductionController(IProductionController):

    def __init__(self):
        self._queue: deque[ProductionJob] = deque()
        self._current: ProductionJob | None = None
        self._counter = 1
        self._queue_order = 1

    def enqueue(self, order_id: str, sample_id: str, planned_quantity: int,
                yield_rate: float, avg_production_time: float) -> ProductionJob:
        # 실 생산량 = ceil(부족분 / (수율 × 0.9)), 시간 → 분 변환
        job = ProductionJob(
            job_id=f"J{self._counter:04d}",
            order_id=order_id,
            sample_id=sample_id,
            planned_quantity=planned_quantity,
            actual_quantity=0,
            total_time_min=avg_production_time * 60 * planned_quantity,
            queue_order=self._queue_order,
            status=JobStatus.WAITING,
        )
        self._counter += 1
        self._queue_order += 1
        self._queue.append(job)
        self._try_start_next()
        return job

    def find_in_progress(self) -> ProductionJob | None:
        return self._current

    def find_waiting_queue(self) -> list[ProductionJob]:
        return list(self._queue)

    def update_status(self, job_id: str, status: JobStatus) -> bool:
        job = self._find_job(job_id)
        if not job:
            return False
        job.status = status
        if status == JobStatus.COMPLETED and self._current and self._current.job_id == job_id:
            self._current = None
            self._try_start_next()
        return True

    def _try_start_next(self):
        if self._current is None and self._queue:
            self._current = self._queue.popleft()
            self._current.status = JobStatus.IN_PROGRESS

    def _find_job(self, job_id: str) -> ProductionJob | None:
        if self._current and self._current.job_id == job_id:
            return self._current
        return next((j for j in self._queue if j.job_id == job_id), None)
