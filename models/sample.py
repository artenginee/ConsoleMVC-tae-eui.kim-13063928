from dataclasses import dataclass, field


@dataclass
class Sample:
    sample_id: str
    name: str
    avg_production_time: float  # 단위: 시간/개
    yield_rate: float           # 수율 0.0 ~ 1.0
    stock: int = 0              # 재고 수량 (POC-2: stock)
