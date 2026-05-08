from models.order import Order
from models.order_status import OrderStatus


class OrderController:

    def __init__(self):
        self._orders: list[Order] = []

    def create(self, sample_id: str, customer_name: str, quantity: int) -> Order:
        pass

    def get_all(self) -> list[Order]:
        pass

    def get_by_id(self, order_id: str) -> Order | None:
        pass

    def get_by_status(self, status: OrderStatus) -> list[Order]:
        pass

    def update_status(self, order_id: str, new_status: OrderStatus) -> bool:
        pass
