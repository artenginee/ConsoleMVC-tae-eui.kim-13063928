from abc import ABC, abstractmethod
from models.sample import Sample


class ISampleController(ABC):

    @abstractmethod
    def add(self, name: str, avg_production_time: float,
            yield_rate: float, initial_inventory: int = 0) -> Sample: ...

    @abstractmethod
    def get_all(self) -> list[Sample]: ...

    @abstractmethod
    def get_by_id(self, sample_id: str) -> Sample | None: ...

    @abstractmethod
    def search_by_name(self, keyword: str) -> list[Sample]: ...

    @abstractmethod
    def update(self, sample_id: str, name: str,
               avg_production_time: float, yield_rate: float) -> bool: ...

    @abstractmethod
    def delete(self, sample_id: str) -> bool: ...

    @abstractmethod
    def add_inventory(self, sample_id: str, qty: int) -> bool: ...

    @abstractmethod
    def deduct_inventory(self, sample_id: str, qty: int) -> bool: ...
