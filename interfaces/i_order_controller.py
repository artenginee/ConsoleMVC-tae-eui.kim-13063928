from abc import ABC, abstractmethod
from models.order import Order
from models.order_status import OrderStatus


class IOrderController(ABC):

    @abstractmethod
    def create(self, sample_id: str, customer_name: str, quantity: int) -> Order: ...

    @abstractmethod
    def get_all(self) -> list[Order]: ...

    @abstractmethod
    def get_by_id(self, order_id: str) -> Order | None: ...

    @abstractmethod
    def get_by_status(self, status: OrderStatus) -> list[Order]: ...

    @abstractmethod
    def update_status(self, order_id: str, new_status: OrderStatus) -> bool: ...
