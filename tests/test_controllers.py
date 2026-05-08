"""
Controller 계약 테스트
----------------------
현재 컨트롤러 메서드는 pass 스텁이므로 아래 테스트는 실패한다.
POC-2에서 구현을 채운 뒤 전체가 통과해야 한다.
"""
import pytest

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


# ── Fixtures ───────────────────────────────────────────────────────────

@pytest.fixture
def sample_ctrl():
    return SampleController()

@pytest.fixture
def order_ctrl():
    return OrderController()

@pytest.fixture
def prod_ctrl():
    return ProductionController()


# ── 인터페이스 구현 확인 (현재도 통과) ────────────────────────────────

def test_sample_controller_implements_interface():
    assert isinstance(SampleController(), ISampleController)

def test_order_controller_implements_interface():
    assert isinstance(OrderController(), IOrderController)

def test_production_controller_implements_interface():
    assert isinstance(ProductionController(), IProductionController)


# ── SampleController 계약 ──────────────────────────────────────────────

def test_sample_add_returns_sample(sample_ctrl):
    result = sample_ctrl.add("NAND-256G", 1.5, 0.88, 100)
    assert isinstance(result, Sample)
    assert result.name == "NAND-256G"
    assert result.inventory == 100

def test_sample_get_all_returns_list(sample_ctrl):
    sample_ctrl.add("DRAM-8G", 2.0, 0.90, 0)
    assert isinstance(sample_ctrl.get_all(), list)
    assert len(sample_ctrl.get_all()) == 1

def test_sample_get_by_id_found(sample_ctrl):
    s = sample_ctrl.add("DRAM-16G", 2.5, 0.85, 50)
    found = sample_ctrl.get_by_id(s.sample_id)
    assert found is not None
    assert found.name == "DRAM-16G"

def test_sample_get_by_id_not_found(sample_ctrl):
    assert sample_ctrl.get_by_id("S999") is None

def test_sample_search_by_name(sample_ctrl):
    sample_ctrl.add("NAND-128G", 1.0, 0.80, 0)
    sample_ctrl.add("DRAM-16G", 2.5, 0.85, 0)
    results = sample_ctrl.search_by_name("NAND")
    assert len(results) == 1
    assert results[0].name == "NAND-128G"

def test_sample_update_success(sample_ctrl):
    s = sample_ctrl.add("DRAM-8G", 2.0, 0.90, 0)
    assert sample_ctrl.update(s.sample_id, "DRAM-8G-v2", 1.8, 0.92) is True
    assert sample_ctrl.get_by_id(s.sample_id).name == "DRAM-8G-v2"

def test_sample_update_unknown_id(sample_ctrl):
    assert sample_ctrl.update("S999", "X", 1.0, 0.9) is False

def test_sample_delete_success(sample_ctrl):
    s = sample_ctrl.add("NAND-512G", 3.0, 0.75, 0)
    assert sample_ctrl.delete(s.sample_id) is True
    assert sample_ctrl.get_by_id(s.sample_id) is None

def test_sample_delete_unknown_id(sample_ctrl):
    assert sample_ctrl.delete("S999") is False

def test_sample_add_inventory(sample_ctrl):
    s = sample_ctrl.add("DRAM-32G", 3.0, 0.80, 0)
    assert sample_ctrl.add_inventory(s.sample_id, 50) is True
    assert sample_ctrl.get_by_id(s.sample_id).inventory == 50

def test_sample_deduct_inventory_success(sample_ctrl):
    s = sample_ctrl.add("DRAM-64G", 4.0, 0.78, 100)
    assert sample_ctrl.deduct_inventory(s.sample_id, 30) is True
    assert sample_ctrl.get_by_id(s.sample_id).inventory == 70

def test_sample_deduct_inventory_insufficient(sample_ctrl):
    s = sample_ctrl.add("DRAM-64G", 4.0, 0.78, 10)
    assert sample_ctrl.deduct_inventory(s.sample_id, 50) is False
    assert sample_ctrl.get_by_id(s.sample_id).inventory == 10


# ── OrderController 계약 ───────────────────────────────────────────────

def test_order_create_returns_order(order_ctrl):
    o = order_ctrl.create("S001", "삼성전자", 200)
    assert isinstance(o, Order)
    assert o.status == OrderStatus.RESERVED
    assert o.quantity == 200

def test_order_get_all_returns_list(order_ctrl):
    order_ctrl.create("S001", "고객A", 100)
    assert isinstance(order_ctrl.get_all(), list)
    assert len(order_ctrl.get_all()) == 1

def test_order_get_by_id_found(order_ctrl):
    o = order_ctrl.create("S001", "고객A", 100)
    assert order_ctrl.get_by_id(o.order_id) is not None

def test_order_get_by_id_not_found(order_ctrl):
    assert order_ctrl.get_by_id("O9999") is None

def test_order_get_by_status(order_ctrl):
    order_ctrl.create("S001", "고객A", 100)
    order_ctrl.create("S002", "고객B", 200)
    assert len(order_ctrl.get_by_status(OrderStatus.RESERVED)) == 2
    assert len(order_ctrl.get_by_status(OrderStatus.CONFIRMED)) == 0

def test_order_update_status_success(order_ctrl):
    o = order_ctrl.create("S001", "고객A", 100)
    assert order_ctrl.update_status(o.order_id, OrderStatus.CONFIRMED) is True
    assert order_ctrl.get_by_id(o.order_id).status == OrderStatus.CONFIRMED

def test_order_update_status_unknown_id(order_ctrl):
    assert order_ctrl.update_status("O9999", OrderStatus.CONFIRMED) is False


# ── ProductionController 계약 ──────────────────────────────────────────

def test_prod_enqueue_returns_job(prod_ctrl):
    job = prod_ctrl.enqueue("O0001", "S001", 10, 0.85, 2.5)
    assert isinstance(job, ProductionJob)
    assert job.shortfall == 10

def test_prod_first_enqueue_auto_starts(prod_ctrl):
    prod_ctrl.enqueue("O0001", "S001", 10, 0.85, 2.5)
    assert prod_ctrl.get_current() is not None

def test_prod_second_job_waits_in_queue(prod_ctrl):
    prod_ctrl.enqueue("O0001", "S001", 10, 0.85, 2.5)
    prod_ctrl.enqueue("O0002", "S001", 5, 0.85, 2.5)
    assert len(prod_ctrl.get_queued()) == 1

def test_prod_get_queued_returns_list(prod_ctrl):
    assert isinstance(prod_ctrl.get_queued(), list)

def test_prod_complete_returns_job(prod_ctrl):
    prod_ctrl.enqueue("O0001", "S001", 10, 0.85, 2.5)
    assert isinstance(prod_ctrl.complete_current(), ProductionJob)

def test_prod_complete_starts_next(prod_ctrl):
    prod_ctrl.enqueue("O0001", "S001", 10, 0.85, 2.5)
    prod_ctrl.enqueue("O0002", "S001", 5, 0.85, 2.5)
    prod_ctrl.complete_current()
    assert prod_ctrl.get_current() is not None
    assert len(prod_ctrl.get_queued()) == 0

def test_prod_complete_with_no_job(prod_ctrl):
    assert prod_ctrl.complete_current() is None
