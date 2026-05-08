from datetime import datetime

from interfaces.i_order_controller import IOrderController
from models.order import Order
from models.order_status import OrderStatus


class OrderController(IOrderController):

    def __init__(self):
        self._orders: list[Order] = []
        self._counter = 1

    def create(self, sample_id: str, customer_name: str, quantity: int) -> Order:
        order = Order(
            order_id=f"O{self._counter:04d}",
            sample_id=sample_id,
            customer_name=customer_name,
            quantity=quantity,
            status=OrderStatus.RESERVED,
            created_at=datetime.now(),
        )
        self._orders.append(order)
        self._counter += 1
        return order

    def find_all(self) -> list[Order]:
        return list(self._orders)

    def find_by_id(self, order_id: str) -> Order | None:
        return next((o for o in self._orders if o.order_id == order_id), None)

    def find_by_status(self, status: OrderStatus) -> list[Order]:
        return [o for o in self._orders if o.status == status]

    def update_status(self, order_id: str, new_status: OrderStatus) -> bool:
        order = self.find_by_id(order_id)
        if not order:
            return False
        order.status = new_status
        return True
