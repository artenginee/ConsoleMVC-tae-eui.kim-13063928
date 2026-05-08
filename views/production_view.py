from controllers.order_controller import OrderController
from controllers.production_controller import ProductionController
from controllers.sample_controller import SampleController
from models.order_status import OrderStatus


class ProductionView:
    """생산담당자 화면: 시료 관리 / 주문 승인·거절 / 생산 라인"""

    def __init__(self, sample_ctrl: SampleController,
                 order_ctrl: OrderController,
                 prod_ctrl: ProductionController):
        self._sc = sample_ctrl
        self._oc = order_ctrl
        self._pc = prod_ctrl

    # ── 메뉴 ──────────────────────────────────────────────────────────

    def show(self):
        while True:
            print("\n----- 생산담당자 메뉴 -----")
            print("1. 시료 관리")
            print("2. 주문 승인 / 거절")
            print("3. 생산 라인 확인")
            print("0. 뒤로")
            choice = input("선택: ").strip()

            if   choice == "1": self._sample_menu()
            elif choice == "2": self._approval_menu()
            elif choice == "3": self._production_menu()
            elif choice == "0": break
            else: print("[오류] 잘못된 선택입니다.")

    # ── 1. 시료 관리 ───────────────────────────────────────────────────

    def _sample_menu(self):
        while True:
            print("\n[ 시료 관리 ]")
            print("1. 시료 등록")
            print("2. 시료 목록 조회")
            print("3. 시료 검색")
            print("4. 시료 수정")
            print("5. 시료 삭제")
            print("0. 뒤로")
            choice = input("선택: ").strip()

            if   choice == "1": self._register_sample()
            elif choice == "2": self._list_samples()
            elif choice == "3": self._search_sample()
            elif choice == "4": self._update_sample()
            elif choice == "5": self._delete_sample()
            elif choice == "0": break

    def _register_sample(self):
        print("\n[시료 등록]  예) NAND-256G / 생산시간 2.5h / 수율 0.87 / 초기재고 100")
        name     = input("  시료명: ").strip()
        avg_time = float(input("  평균 생산시간 (h/개): "))
        yield_r  = float(input("  수율 (0.0~1.0): "))
        init_inv = int(input("  초기 재고 수량 (개): "))

        s = self._sc.add(name, avg_time, yield_r, init_inv)
        print(f"  → 등록 완료 | ID: {s.sample_id}  이름: {s.name}")

    def _list_samples(self):
        print("\n[시료 목록]")
        samples = self._sc.get_all()
        if not samples:
            print("  등록된 시료가 없습니다.")
            return
        print(f"  {'ID':<8} {'이름':<16} {'생산시간':>10} {'수율':>8} {'재고':>8}")
        print("  " + "-" * 54)
        for s in samples:
            print(f"  {s.sample_id:<8} {s.name:<16} {s.avg_production_time:>9.1f}h "
                  f"{s.yield_rate:>7.0%} {s.inventory:>8,}")

    def _search_sample(self):
        keyword = input("  검색어 (이름): ").strip()
        results = self._sc.search_by_name(keyword)
        print(f"  검색 결과: {len(results)}건")
        for s in results:
            print(f"    {s.sample_id}  {s.name}  재고 {s.inventory:,}개")

    def _update_sample(self):
        self._list_samples()
        sid  = input("  수정할 시료 ID: ").strip()
        s    = self._sc.get_by_id(sid)
        if not s:
            print("  [오류] 시료를 찾을 수 없습니다.")
            return
        name     = input(f"  새 이름 (현재: {s.name}, Enter=유지): ").strip() or s.name
        avg_time = input(f"  새 생산시간 (현재: {s.avg_production_time}, Enter=유지): ").strip()
        yield_r  = input(f"  새 수율 (현재: {s.yield_rate}, Enter=유지): ").strip()
        self._sc.update(sid, name,
                        float(avg_time) if avg_time else s.avg_production_time,
                        float(yield_r)  if yield_r  else s.yield_rate)
        print("  → 수정 완료")

    def _delete_sample(self):
        self._list_samples()
        sid = input("  삭제할 시료 ID: ").strip()
        if self._sc.delete(sid):
            print("  → 삭제 완료")
        else:
            print("  [오류] 시료를 찾을 수 없습니다.")

    # ── 2. 주문 승인 / 거절 ────────────────────────────────────────────

    def _approval_menu(self):
        while True:
            print("\n[ 주문 승인 / 거절 ]")
            print("1. 접수 주문 목록 (RESERVED)")
            print("2. 주문 승인")
            print("3. 주문 거절")
            print("0. 뒤로")
            choice = input("선택: ").strip()

            if   choice == "1": self._list_reserved()
            elif choice == "2": self._approve_order()
            elif choice == "3": self._reject_order()
            elif choice == "0": break

    def _list_reserved(self):
        orders = self._oc.get_by_status(OrderStatus.RESERVED)
        print(f"\n  RESERVED 주문: {len(orders)}건")
        for o in orders:
            print(f"    {o.order_id}  시료: {o.sample_id}  "
                  f"고객: {o.customer_name}  수량: {o.quantity:,}개")

    def _approve_order(self):
        self._list_reserved()
        oid   = input("  승인할 주문 ID: ").strip()
        order = self._oc.get_by_id(oid)
        if not order or order.status != OrderStatus.RESERVED:
            print("  [오류] 유효한 RESERVED 주문이 아닙니다.")
            return

        sample = self._sc.get_by_id(order.sample_id)

        if sample.inventory >= order.quantity:
            # 재고 충분 → 즉시 CONFIRMED
            self._sc.deduct_inventory(sample.sample_id, order.quantity)
            self._oc.update_status(oid, OrderStatus.CONFIRMED)
            print(f"  → 재고 충분. 즉시 CONFIRMED  (잔여재고: {sample.inventory:,}개)")
        else:
            # 재고 부족 → 생산 등록 + PRODUCING
            shortfall = order.quantity - sample.inventory
            job = self._pc.enqueue(oid, sample.sample_id, shortfall,
                                   sample.yield_rate, sample.avg_production_time)
            self._oc.update_status(oid, OrderStatus.PRODUCING)
            print(f"  → 재고 부족(부족분 {shortfall:,}개). 생산 등록 → PRODUCING")
            print(f"     작업ID: {job.job_id}  실생산량: {job.actual_production_qty:,}개  "
                  f"예상시간: {job.total_production_time:.1f}h")

    def _reject_order(self):
        self._list_reserved()
        oid = input("  거절할 주문 ID: ").strip()
        if self._oc.update_status(oid, OrderStatus.REJECTED):
            print(f"  → {oid} REJECTED 처리 완료")
        else:
            print("  [오류] 주문을 찾을 수 없습니다.")

    # ── 3. 생산 라인 ───────────────────────────────────────────────────

    def _production_menu(self):
        while True:
            print("\n[ 생산 라인 ]")
            print("1. 현재 생산 현황")
            print("2. 대기 큐 확인")
            print("3. 생산 완료 처리")
            print("0. 뒤로")
            choice = input("선택: ").strip()

            if   choice == "1": self._show_current_job()
            elif choice == "2": self._show_queue()
            elif choice == "3": self._complete_job()
            elif choice == "0": break

    def _show_current_job(self):
        job = self._pc.get_current()
        if not job:
            print("  현재 생산 중인 작업 없음")
            return
        order  = self._oc.get_by_id(job.order_id)
        sample = self._sc.get_by_id(job.sample_id)
        print(f"\n  [생산중] {job.job_id}")
        print(f"    시료: {sample.name if sample else job.sample_id}")
        print(f"    주문: {job.order_id}  고객: {order.customer_name if order else '-'}")
        print(f"    부족분: {job.shortfall:,}개  실생산량: {job.actual_production_qty:,}개  "
              f"예상시간: {job.total_production_time:.1f}h")

    def _show_queue(self):
        queue = self._pc.get_queued()
        print(f"\n  대기 중인 작업: {len(queue)}건")
        for i, job in enumerate(queue, 1):
            print(f"    {i}. {job.job_id}  주문: {job.order_id}  "
                  f"실생산량: {job.actual_production_qty:,}개")

    def _complete_job(self):
        job = self._pc.get_current()
        if not job:
            print("  현재 생산 중인 작업 없음")
            return
        sample = self._sc.get_by_id(job.sample_id)
        order  = self._oc.get_by_id(job.order_id)

        completed  = self._pc.complete_current()
        good_units = int(completed.actual_production_qty * sample.yield_rate)
        self._sc.add_inventory(sample.sample_id, good_units)
        self._sc.deduct_inventory(sample.sample_id, order.quantity)
        self._oc.update_status(job.order_id, OrderStatus.CONFIRMED)

        print(f"  → 생산 완료  양품입고: {good_units:,}개  "
              f"주문 {job.order_id}: PRODUCING → CONFIRMED")
