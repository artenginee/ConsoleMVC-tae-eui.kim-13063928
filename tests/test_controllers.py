"""
Controller 계약 테스트 — POC-2 인터페이스 명세 기준
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
from models.production_job import JobStatus, ProductionJob
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


# ── 인터페이스 구현 확인 ────────────────────────────────────────────────

def test_sample_controller_implements_interface():
    assert isinstance(SampleController(), ISampleController)

def test_order_controller_implements_interface():
    assert isinstance(OrderController(), IOrderController)

def test_production_controller_implements_interface():
    assert isinstance(ProductionController(), IProductionController)


# ── SampleController ───────────────────────────────────────────────────

def test_sample_create_returns_sample(sample_ctrl):
    result = sample_ctrl.create("NAND-256G", 1.5, 0.88, 100)
    assert isinstance(result, Sample)
    assert result.name == "NAND-256G"
    assert result.stock == 100

def test_sample_find_all(sample_ctrl):
    sample_ctrl.create("DRAM-8G", 2.0, 0.90, 0)
    assert len(sample_ctrl.find_all()) == 1

def test_sample_find_by_id_found(sample_ctrl):
    s = sample_ctrl.create("DRAM-16G", 2.5, 0.85, 50)
    assert sample_ctrl.find_by_id(s.sample_id).name == "DRAM-16G"

def test_sample_find_by_id_not_found(sample_ctrl):
    assert sample_ctrl.find_by_id("S999") is None

def test_sample_find_by_name(sample_ctrl):
    sample_ctrl.create("NAND-128G", 1.0, 0.80, 0)
    sample_ctrl.create("DRAM-16G", 2.5, 0.85, 0)
    results = sample_ctrl.find_by_name("NAND")
    assert len(results) == 1
    assert results[0].name == "NAND-128G"

def test_sample_update_success(sample_ctrl):
    s = sample_ctrl.create("DRAM-8G", 2.0, 0.90, 0)
    assert sample_ctrl.update(s.sample_id, "DRAM-8G-v2", 1.8, 0.92) is True
    assert sample_ctrl.find_by_id(s.sample_id).name == "DRAM-8G-v2"

def test_sample_update_unknown_id(sample_ctrl):
    assert sample_ctrl.update("S999", "X", 1.0, 0.9) is False

def test_sample_delete_success(sample_ctrl):
    s = sample_ctrl.create("NAND-512G", 3.0, 0.75, 0)
    assert sample_ctrl.delete(s.sample_id) is True
    assert sample_ctrl.find_by_id(s.sample_id) is None

def test_sample_delete_unknown_id(sample_ctrl):
    assert sample_ctrl.delete("S999") is False

def test_sample_update_stock_increase(sample_ctrl):
    s = sample_ctrl.create("DRAM-32G", 3.0, 0.80, 0)
    assert sample_ctrl.update_stock(s.sample_id, 50) is True
    assert sample_ctrl.find_by_id(s.sample_id).stock == 50

def test_sample_update_stock_decrease(sample_ctrl):
    s = sample_ctrl.create("DRAM-64G", 4.0, 0.78, 100)
    assert sample_ctrl.update_stock(s.sample_id, -30) is True
    assert sample_ctrl.find_by_id(s.sample_id).stock == 70

def test_sample_update_stock_insufficient(sample_ctrl):
    s = sample_ctrl.create("DRAM-64G", 4.0, 0.78, 10)
    assert sample_ctrl.update_stock(s.sample_id, -50) is False
    assert sample_ctrl.find_by_id(s.sample_id).stock == 10


# ── OrderController ────────────────────────────────────────────────────

def test_order_create_returns_order(order_ctrl):
    o = order_ctrl.create("S001", "삼성전자", 200)
    assert isinstance(o, Order)
    assert o.status == OrderStatus.RESERVED
    assert o.quantity == 200

def test_order_find_all(order_ctrl):
    order_ctrl.create("S001", "고객A", 100)
    assert len(order_ctrl.find_all()) == 1

def test_order_find_by_id_found(order_ctrl):
    o = order_ctrl.create("S001", "고객A", 100)
    assert order_ctrl.find_by_id(o.order_id) is not None

def test_order_find_by_id_not_found(order_ctrl):
    assert order_ctrl.find_by_id("O9999") is None

def test_order_find_by_status(order_ctrl):
    order_ctrl.create("S001", "고객A", 100)
    order_ctrl.create("S002", "고객B", 200)
    assert len(order_ctrl.find_by_status(OrderStatus.RESERVED)) == 2
    assert len(order_ctrl.find_by_status(OrderStatus.CONFIRMED)) == 0

def test_order_update_status_success(order_ctrl):
    o = order_ctrl.create("S001", "고객A", 100)
    assert order_ctrl.update_status(o.order_id, OrderStatus.CONFIRMED) is True
    assert order_ctrl.find_by_id(o.order_id).status == OrderStatus.CONFIRMED

def test_order_update_status_unknown_id(order_ctrl):
    assert order_ctrl.update_status("O9999", OrderStatus.CONFIRMED) is False


# ── ProductionController ───────────────────────────────────────────────

def test_prod_enqueue_returns_job(prod_ctrl):
    job = prod_ctrl.enqueue("O0001", "S001", 13, 0.85, 2.5)
    assert isinstance(job, ProductionJob)
    assert job.planned_quantity == 13

def test_prod_first_enqueue_auto_starts(prod_ctrl):
    prod_ctrl.enqueue("O0001", "S001", 13, 0.85, 2.5)
    assert prod_ctrl.find_in_progress() is not None
    assert prod_ctrl.find_in_progress().status == JobStatus.IN_PROGRESS

def test_prod_second_job_waits(prod_ctrl):
    prod_ctrl.enqueue("O0001", "S001", 13, 0.85, 2.5)
    prod_ctrl.enqueue("O0002", "S001", 5, 0.85, 2.5)
    assert len(prod_ctrl.find_waiting_queue()) == 1
    assert prod_ctrl.find_waiting_queue()[0].status == JobStatus.WAITING

def test_prod_find_waiting_queue_empty(prod_ctrl):
    assert prod_ctrl.find_waiting_queue() == []

def test_prod_update_status_completed(prod_ctrl):
    job = prod_ctrl.enqueue("O0001", "S001", 13, 0.85, 2.5)
    assert prod_ctrl.update_status(job.job_id, JobStatus.COMPLETED) is True
    assert prod_ctrl.find_in_progress() is None

def test_prod_complete_starts_next(prod_ctrl):
    job1 = prod_ctrl.enqueue("O0001", "S001", 13, 0.85, 2.5)
    prod_ctrl.enqueue("O0002", "S001", 5, 0.85, 2.5)
    prod_ctrl.update_status(job1.job_id, JobStatus.COMPLETED)
    assert prod_ctrl.find_in_progress() is not None
    assert len(prod_ctrl.find_waiting_queue()) == 0

def test_prod_update_status_unknown_id(prod_ctrl):
    assert prod_ctrl.update_status("J9999", JobStatus.COMPLETED) is False
