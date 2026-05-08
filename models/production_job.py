from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ProductionJob:
    job_id: str
    order_id: str
    sample_id: str
    shortfall: int              # 부족분
    actual_production_qty: int  # 실 생산량
    total_production_time: float  # 총 생산시간 (시간)
    produced_qty: int = 0
    enqueued_at: datetime = field(default_factory=datetime.now)
    is_in_progress: bool = False
