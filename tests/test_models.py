import unittest
from datetime import datetime

from models.order import Order
from models.order_status import OrderStatus
from models.production_job import ProductionJob
from models.sample import Sample


class TestOrderStatus(unittest.TestCase):

    def test_has_five_statuses(self):
        values = {s.value for s in OrderStatus}
        self.assertEqual(values, {"RESERVED", "REJECTED", "PRODUCING", "CONFIRMED", "RELEASE"})


class TestSample(unittest.TestCase):

    def _make(self, **kwargs):
        defaults = dict(sample_id="S001", name="DRAM-16G",
                        avg_production_time=2.5, yield_rate=0.85)
        return Sample(**{**defaults, **kwargs})

    def test_fields_assigned(self):
        s = self._make()
        self.assertEqual(s.sample_id, "S001")
        self.assertEqual(s.name, "DRAM-16G")
        self.assertAlmostEqual(s.avg_production_time, 2.5)
        self.assertAlmostEqual(s.yield_rate, 0.85)

    def test_inventory_default_zero(self):
        self.assertEqual(self._make().inventory, 0)

    def test_inventory_set(self):
        self.assertEqual(self._make(inventory=200).inventory, 200)


class TestOrder(unittest.TestCase):

    def _make(self, **kwargs):
        defaults = dict(order_id="O0001", sample_id="S001",
                        customer_name="삼성전자", quantity=100)
        return Order(**{**defaults, **kwargs})

    def test_default_status_reserved(self):
        self.assertEqual(self._make().status, OrderStatus.RESERVED)

    def test_created_at_is_datetime(self):
        self.assertIsInstance(self._make().created_at, datetime)

    def test_status_mutable(self):
        o = self._make()
        o.status = OrderStatus.CONFIRMED
        self.assertEqual(o.status, OrderStatus.CONFIRMED)

    def test_fields_assigned(self):
        o = self._make()
        self.assertEqual(o.order_id, "O0001")
        self.assertEqual(o.customer_name, "삼성전자")
        self.assertEqual(o.quantity, 100)


class TestProductionJob(unittest.TestCase):

    def _make(self, **kwargs):
        defaults = dict(job_id="J0001", order_id="O0001", sample_id="S001",
                        shortfall=10, actual_production_qty=13,
                        total_production_time=32.5)
        return ProductionJob(**{**defaults, **kwargs})

    def test_fields_assigned(self):
        j = self._make()
        self.assertEqual(j.job_id, "J0001")
        self.assertEqual(j.shortfall, 10)
        self.assertEqual(j.actual_production_qty, 13)
        self.assertAlmostEqual(j.total_production_time, 32.5)

    def test_produced_qty_default_zero(self):
        self.assertEqual(self._make().produced_qty, 0)

    def test_is_in_progress_default_false(self):
        self.assertFalse(self._make().is_in_progress)


if __name__ == "__main__":
    unittest.main()
