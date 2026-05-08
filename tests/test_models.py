from datetime import datetime

import pytest

from models.order import Order
from models.order_status import OrderStatus
from models.production_job import JobStatus, ProductionJob
from models.sample import Sample


# ── OrderStatus ────────────────────────────────────────────────────────

def test_order_status_has_five_values():
    assert {s.value for s in OrderStatus} == {
        "RESERVED", "REJECTED", "PRODUCING", "CONFIRMED", "RELEASE"
    }


# ── JobStatus ──────────────────────────────────────────────────────────

def test_job_status_has_three_values():
    assert {s.value for s in JobStatus} == {"WAITING", "IN_PROGRESS", "COMPLETED"}


# ── Sample ─────────────────────────────────────────────────────────────

def test_sample_fields_assigned():
    s = Sample("S001", "DRAM-16G", 2.5, 0.85)
    assert s.sample_id == "S001"
    assert s.name == "DRAM-16G"
    assert s.avg_production_time == pytest.approx(2.5)
    assert s.yield_rate == pytest.approx(0.85)

def test_sample_stock_default_zero():
    assert Sample("S001", "NAND-256G", 1.5, 0.90).stock == 0

def test_sample_stock_set():
    assert Sample("S001", "NAND-256G", 1.5, 0.90, 200).stock == 200


# ── Order ──────────────────────────────────────────────────────────────

def test_order_default_status_reserved():
    assert Order("O0001", "S001", "삼성전자", 100).status == OrderStatus.RESERVED

def test_order_created_at_is_datetime():
    assert isinstance(Order("O0001", "S001", "고객A", 100).created_at, datetime)

def test_order_status_mutable():
    o = Order("O0001", "S001", "고객A", 50)
    o.status = OrderStatus.CONFIRMED
    assert o.status == OrderStatus.CONFIRMED

def test_order_fields_assigned():
    o = Order("O0001", "S001", "삼성전자", 100)
    assert o.order_id == "O0001"
    assert o.customer_name == "삼성전자"
    assert o.quantity == 100


# ── ProductionJob ──────────────────────────────────────────────────────

def test_production_job_fields_assigned():
    j = ProductionJob("J0001", "O0001", "S001", planned_quantity=13,
                      actual_quantity=0, total_time_min=195.0)
    assert j.job_id == "J0001"
    assert j.planned_quantity == 13
    assert j.actual_quantity == 0
    assert j.total_time_min == pytest.approx(195.0)

def test_production_job_default_status_waiting():
    j = ProductionJob("J0001", "O0001", "S001", 13, 0, 195.0)
    assert j.status == JobStatus.WAITING

def test_production_job_queue_order_default_zero():
    j = ProductionJob("J0001", "O0001", "S001", 13, 0, 195.0)
    assert j.queue_order == 0
