from datetime import datetime
from typing import Dict, List, Optional
from models.order import Order
from models.order_status import OrderStatus


class OrderController:
    """주문 생성 및 상태 관리"""

    def __init__(self):
        self._orders: List[Order] = []
        self._counter = 1

    # ── CRUD ──────────────────────────────────────────────────────────

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

    def get_all(self) -> List[Order]:
        return list(self._orders)

    def get_by_id(self, order_id: str) -> Optional[Order]:
        return next((o for o in self._orders if o.order_id == order_id), None)

    def get_by_status(self, status: OrderStatus) -> List[Order]:
        return [o for o in self._orders if o.status == status]

    def update_status(self, order_id: str, new_status: OrderStatus) -> bool:
        order = self.get_by_id(order_id)
        if not order:
            return False
        order.status = new_status
        return True

    # ── 집계 ──────────────────────────────────────────────────────────

    def count_by_status(self) -> Dict[OrderStatus, int]:
        return {
            s: len(self.get_by_status(s))
            for s in OrderStatus
            if s != OrderStatus.REJECTED
        }
