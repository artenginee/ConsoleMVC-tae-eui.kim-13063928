"""
Controller 계약 테스트
----------------------
현재 컨트롤러 메서드는 pass 스텁이므로 아래 테스트는 실패한다.
POC-2에서 구현을 채운 뒤 전체가 통과해야 한다.
"""
import unittest

from controllers.order_controller import OrderController
from controllers.production_controller import ProductionController
from controllers.sample_controller import SampleController
from interfaces.i_order_controller import IOrderController
from interfaces.i_production_controller import IProductionController
from interfaces.i_sample_controller import ISampleController
from models.order import Order
from models.order_status import OrderStatus
from models.production_job import ProductionJob
from models.sample import Sample


class TestInterfaces(unittest.TestCase):
    """각 컨트롤러가 대응하는 인터페이스를 구현하는지 확인"""

    def test_sample_controller_implements_interface(self):
        self.assertIsInstance(SampleController(), ISampleController)

    def test_order_controller_implements_interface(self):
        self.assertIsInstance(OrderController(), IOrderController)

    def test_production_controller_implements_interface(self):
        self.assertIsInstance(ProductionController(), IProductionController)


class TestSampleController(unittest.TestCase):

    def setUp(self):
        self.ctrl = SampleController()

    def test_add_returns_sample(self):
        result = self.ctrl.add("NAND-256G", 1.5, 0.88, 100)
        self.assertIsInstance(result, Sample)
        self.assertEqual(result.name, "NAND-256G")
        self.assertEqual(result.inventory, 100)

    def test_get_all_returns_list(self):
        self.ctrl.add("DRAM-8G", 2.0, 0.90, 0)
        result = self.ctrl.get_all()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_get_by_id_found(self):
        sample = self.ctrl.add("DRAM-16G", 2.5, 0.85, 50)
        found = self.ctrl.get_by_id(sample.sample_id)
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "DRAM-16G")

    def test_get_by_id_not_found(self):
        self.assertIsNone(self.ctrl.get_by_id("S999"))

    def test_search_by_name(self):
        self.ctrl.add("NAND-128G", 1.0, 0.80, 0)
        self.ctrl.add("DRAM-16G", 2.5, 0.85, 0)
        results = self.ctrl.search_by_name("NAND")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "NAND-128G")

    def test_update_returns_true(self):
        sample = self.ctrl.add("DRAM-8G", 2.0, 0.90, 0)
        ok = self.ctrl.update(sample.sample_id, "DRAM-8G-v2", 1.8, 0.92)
        self.assertTrue(ok)
        self.assertEqual(self.ctrl.get_by_id(sample.sample_id).name, "DRAM-8G-v2")

    def test_update_unknown_id_returns_false(self):
        self.assertFalse(self.ctrl.update("S999", "X", 1.0, 0.9))

    def test_delete_returns_true(self):
        sample = self.ctrl.add("NAND-512G", 3.0, 0.75, 0)
        ok = self.ctrl.delete(sample.sample_id)
        self.assertTrue(ok)
        self.assertIsNone(self.ctrl.get_by_id(sample.sample_id))

    def test_delete_unknown_id_returns_false(self):
        self.assertFalse(self.ctrl.delete("S999"))

    def test_add_inventory(self):
        sample = self.ctrl.add("DRAM-32G", 3.0, 0.80, 0)
        ok = self.ctrl.add_inventory(sample.sample_id, 50)
        self.assertTrue(ok)
        self.assertEqual(self.ctrl.get_by_id(sample.sample_id).inventory, 50)

    def test_deduct_inventory_success(self):
        sample = self.ctrl.add("DRAM-64G", 4.0, 0.78, 100)
        ok = self.ctrl.deduct_inventory(sample.sample_id, 30)
        self.assertTrue(ok)
        self.assertEqual(self.ctrl.get_by_id(sample.sample_id).inventory, 70)

    def test_deduct_inventory_insufficient(self):
        sample = self.ctrl.add("DRAM-64G", 4.0, 0.78, 10)
        ok = self.ctrl.deduct_inventory(sample.sample_id, 50)
        self.assertFalse(ok)
        self.assertEqual(self.ctrl.get_by_id(sample.sample_id).inventory, 10)


class TestOrderController(unittest.TestCase):

    def setUp(self):
        self.ctrl = OrderController()

    def test_create_returns_order(self):
        order = self.ctrl.create("S001", "삼성전자", 200)
        self.assertIsInstance(order, Order)
        self.assertEqual(order.status, OrderStatus.RESERVED)
        self.assertEqual(order.quantity, 200)

    def test_get_all_returns_list(self):
        self.ctrl.create("S001", "고객A", 100)
        result = self.ctrl.get_all()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_get_by_id_found(self):
        order = self.ctrl.create("S001", "고객A", 100)
        self.assertIsNotNone(self.ctrl.get_by_id(order.order_id))

    def test_get_by_id_not_found(self):
        self.assertIsNone(self.ctrl.get_by_id("O9999"))

    def test_get_by_status(self):
        self.ctrl.create("S001", "고객A", 100)
        self.ctrl.create("S002", "고객B", 200)
        self.assertEqual(len(self.ctrl.get_by_status(OrderStatus.RESERVED)), 2)
        self.assertEqual(len(self.ctrl.get_by_status(OrderStatus.CONFIRMED)), 0)

    def test_update_status_success(self):
        order = self.ctrl.create("S001", "고객A", 100)
        ok = self.ctrl.update_status(order.order_id, OrderStatus.CONFIRMED)
        self.assertTrue(ok)
        self.assertEqual(self.ctrl.get_by_id(order.order_id).status, OrderStatus.CONFIRMED)

    def test_update_status_unknown_id_returns_false(self):
        self.assertFalse(self.ctrl.update_status("O9999", OrderStatus.CONFIRMED))


class TestProductionController(unittest.TestCase):

    def setUp(self):
        self.ctrl = ProductionController()

    def test_enqueue_returns_job(self):
        job = self.ctrl.enqueue("O0001", "S001", 10, 0.85, 2.5)
        self.assertIsInstance(job, ProductionJob)
        self.assertEqual(job.shortfall, 10)

    def test_first_enqueue_auto_starts(self):
        self.ctrl.enqueue("O0001", "S001", 10, 0.85, 2.5)
        self.assertIsNotNone(self.ctrl.get_current())

    def test_second_job_waits_in_queue(self):
        self.ctrl.enqueue("O0001", "S001", 10, 0.85, 2.5)
        self.ctrl.enqueue("O0002", "S001", 5, 0.85, 2.5)
        self.assertEqual(len(self.ctrl.get_queued()), 1)

    def test_get_queued_returns_list(self):
        self.assertIsInstance(self.ctrl.get_queued(), list)

    def test_complete_current_returns_job(self):
        self.ctrl.enqueue("O0001", "S001", 10, 0.85, 2.5)
        completed = self.ctrl.complete_current()
        self.assertIsInstance(completed, ProductionJob)

    def test_complete_starts_next_job(self):
        self.ctrl.enqueue("O0001", "S001", 10, 0.85, 2.5)
        self.ctrl.enqueue("O0002", "S001", 5, 0.85, 2.5)
        self.ctrl.complete_current()
        self.assertIsNotNone(self.ctrl.get_current())
        self.assertEqual(len(self.ctrl.get_queued()), 0)

    def test_complete_with_no_job_returns_none(self):
        self.assertIsNone(self.ctrl.complete_current())


if __name__ == "__main__":
    unittest.main()
