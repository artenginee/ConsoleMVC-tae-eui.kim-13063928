from datetime import datetime

import pytest

from models.order import Order
from models.order_status import OrderStatus
from models.production_job import ProductionJob
from models.sample import Sample


# ── OrderStatus ────────────────────────────────────────────────────────

def test_order_status_has_five_values():
    assert {s.value for s in OrderStatus} == {
        "RESERVED", "REJECTED", "PRODUCING", "CONFIRMED", "RELEASE"
    }


# ── Sample ─────────────────────────────────────────────────────────────

def test_sample_fields_assigned():
    s = Sample("S001", "DRAM-16G", 2.5, 0.85)
    assert s.sample_id == "S001"
    assert s.name == "DRAM-16G"
    assert s.avg_production_time == pytest.approx(2.5)
    assert s.yield_rate == pytest.approx(0.85)

def test_sample_inventory_default_zero():
    assert Sample("S001", "NAND-256G", 1.5, 0.90).inventory == 0

def test_sample_inventory_set():
    assert Sample("S001", "NAND-256G", 1.5, 0.90, 200).inventory == 200


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
    j = ProductionJob("J0001", "O0001", "S001", 10, 13, 32.5)
    assert j.job_id == "J0001"
    assert j.shortfall == 10
    assert j.actual_production_qty == 13
    assert j.total_production_time == pytest.approx(32.5)

def test_production_job_produced_qty_default_zero():
    assert ProductionJob("J0001", "O0001", "S001", 10, 13, 32.5).produced_qty == 0

def test_production_job_is_in_progress_default_false():
    assert not ProductionJob("J0001", "O0001", "S001", 10, 13, 32.5).is_in_progress
