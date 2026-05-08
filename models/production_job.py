from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class JobStatus(Enum):
    WAITING     = "WAITING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED   = "COMPLETED"


@dataclass
class ProductionJob:
    job_id: str
    order_id: str
    sample_id: str
    planned_quantity: int           # 실 생산량 목표
    actual_quantity: int            # 실제 생산된 양품 수량
    total_time_min: float           # 총 생산시간 (분)
    queue_order: int = 0            # FIFO 순번
    status: JobStatus = JobStatus.WAITING
    enqueued_at: datetime = field(default_factory=datetime.now)
