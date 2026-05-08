from interfaces.i_sample_controller import ISampleController
from models.sample import Sample


class SampleController(ISampleController):

    def __init__(self):
        self._samples: list[Sample] = []

    def add(self, name: str, avg_production_time: float,
            yield_rate: float, initial_inventory: int = 0) -> Sample:
        pass

    def get_all(self) -> list[Sample]:
        pass

    def get_by_id(self, sample_id: str) -> Sample | None:
        pass

    def search_by_name(self, keyword: str) -> list[Sample]:
        pass

    def update(self, sample_id: str, name: str,
               avg_production_time: float, yield_rate: float) -> bool:
        pass

    def delete(self, sample_id: str) -> bool:
        pass

    def add_inventory(self, sample_id: str, qty: int) -> bool:
        pass

    def deduct_inventory(self, sample_id: str, qty: int) -> bool:
        pass
