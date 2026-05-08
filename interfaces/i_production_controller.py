from abc import ABC, abstractmethod
from models.production_job import ProductionJob


class IProductionController(ABC):

    @abstractmethod
    def enqueue(self, order_id: str, sample_id: str, shortfall: int,
                yield_rate: float, avg_production_time: float) -> ProductionJob: ...

    @abstractmethod
    def get_current(self) -> ProductionJob | None: ...

    @abstractmethod
    def get_queued(self) -> list[ProductionJob]: ...

    @abstractmethod
    def complete_current(self) -> ProductionJob | None: ...
