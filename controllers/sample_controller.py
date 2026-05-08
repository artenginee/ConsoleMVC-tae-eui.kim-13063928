from interfaces.i_sample_controller import ISampleController
from models.sample import Sample


class SampleController(ISampleController):

    def __init__(self):
        self._samples: list[Sample] = []
        self._counter = 1

    def create(self, name: str, avg_production_time: float,
               yield_rate: float, initial_stock: int = 0) -> Sample:
        sample = Sample(
            sample_id=f"S{self._counter:03d}",
            name=name,
            avg_production_time=avg_production_time,
            yield_rate=yield_rate,
            stock=initial_stock,
        )
        self._samples.append(sample)
        self._counter += 1
        return sample

    def find_all(self) -> list[Sample]:
        return list(self._samples)

    def find_by_id(self, sample_id: str) -> Sample | None:
        return next((s for s in self._samples if s.sample_id == sample_id), None)

    def find_by_name(self, keyword: str) -> list[Sample]:
        return [s for s in self._samples if keyword.lower() in s.name.lower()]

    def update(self, sample_id: str, name: str,
               avg_production_time: float, yield_rate: float) -> bool:
        sample = self.find_by_id(sample_id)
        if not sample:
            return False
        sample.name = name
        sample.avg_production_time = avg_production_time
        sample.yield_rate = yield_rate
        return True

    def delete(self, sample_id: str) -> bool:
        sample = self.find_by_id(sample_id)
        if not sample:
            return False
        self._samples.remove(sample)
        return True

    def update_stock(self, sample_id: str, delta: int) -> bool:
        """delta 양수: 재고 증가 / 음수: 재고 차감"""
        sample = self.find_by_id(sample_id)
        if not sample:
            return False
        if sample.stock + delta < 0:
            return False
        sample.stock += delta
        return True
