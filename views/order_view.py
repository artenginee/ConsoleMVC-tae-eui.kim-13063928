from controllers.order_controller import OrderController
from controllers.sample_controller import SampleController
from models.order_status import OrderStatus


class OrderView:
    """주문담당자 화면: 시료 주문 / 모니터링 / 출고 처리"""

    def __init__(self, sample_ctrl: SampleController, order_ctrl: OrderController):
        self._sc = sample_ctrl
        self._oc = order_ctrl

    # ── 메뉴 ──────────────────────────────────────────────────────────

    def show(self):
        while True:
            print("\n----- 주문담당자 메뉴 -----")
            print("1. 시료 주문")
            print("2. 모니터링")
            print("3. 출고 처리")
            print("0. 뒤로")
            choice = input("선택: ").strip()

            if   choice == "1": self._order_menu()
            elif choice == "2": self._monitoring_menu()
            elif choice == "3": self._release_menu()
            elif choice == "0": break
            else: print("[오류] 잘못된 선택입니다.")

    # ── 1. 시료 주문 ───────────────────────────────────────────────────

    def _order_menu(self):
        while True:
            print("\n[ 시료 주문 ]")
            print("1. 주문 예약")
            print("2. 시료 목록 보기")
            print("0. 뒤로")
            choice = input("선택: ").strip()

            if   choice == "1": self._reserve_order()
            elif choice == "2": self._list_samples()
            elif choice == "0": break

    def _list_samples(self):
        samples = self._sc.get_all()
        print(f"\n  {'ID':<8} {'시료명':<16} {'재고':>8}")
        print("  " + "-" * 34)
        for s in samples:
            print(f"  {s.sample_id:<8} {s.name:<16} {s.inventory:>8,}개")

    def _reserve_order(self):
        self._list_samples()
        sid      = input("  시료 ID: ").strip()
        sample   = self._sc.get_by_id(sid)
        if not sample:
            print("  [오류] 시료를 찾을 수 없습니다.")
            return
        customer = input("  고객명: ").strip()
        qty      = int(input("  주문 수량 (개): "))

        order = self._oc.create(sid, customer, qty)
        print(f"  → 주문 접수 완료 | {order.order_id}  상태: RESERVED")

    # ── 2. 모니터링 ────────────────────────────────────────────────────

    def _monitoring_menu(self):
        while True:
            print("\n[ 모니터링 ]")
            print("1. 주문량 확인 (상태별)")
            print("2. 재고량 확인 (시료별)")
            print("0. 뒤로")
            choice = input("선택: ").strip()

            if   choice == "1": self._show_order_status()
            elif choice == "2": self._show_inventory_status()
            elif choice == "0": break

    def _show_order_status(self):
        active = [OrderStatus.RESERVED, OrderStatus.PRODUCING,
                  OrderStatus.CONFIRMED, OrderStatus.RELEASE]
        print()
        for status in active:
            orders = self._oc.get_by_status(status)
            print(f"  {status.value:<12}: {len(orders)}건")
            for o in orders:
                print(f"      {o.order_id}  고객: {o.customer_name}  수량: {o.quantity:,}개")

    def _show_inventory_status(self):
        samples    = self._sc.get_all()
        all_orders = self._oc.get_all()
        pending    = {OrderStatus.RESERVED, OrderStatus.PRODUCING}

        print(f"\n  {'시료명':<16} {'재고':>8} {'잠재수요':>10} {'상태':>6}")
        print("  " + "-" * 44)
        for s in samples:
            demand = sum(o.quantity for o in all_orders
                         if o.sample_id == s.sample_id and o.status in pending)
            if   s.inventory == 0:       label = "고갈"
            elif s.inventory < demand:   label = "부족"
            else:                        label = "여유"
            print(f"  {s.name:<16} {s.inventory:>8,} {demand:>10,} {label:>6}")

    # ── 3. 출고 처리 ───────────────────────────────────────────────────

    def _release_menu(self):
        while True:
            print("\n[ 출고 처리 ]")
            print("1. 출고 대기 목록 (CONFIRMED)")
            print("2. 출고 실행")
            print("0. 뒤로")
            choice = input("선택: ").strip()

            if   choice == "1": self._list_confirmed()
            elif choice == "2": self._process_release()
            elif choice == "0": break

    def _list_confirmed(self):
        orders = self._oc.get_by_status(OrderStatus.CONFIRMED)
        print(f"\n  출고 대기: {len(orders)}건")
        for o in orders:
            sample = self._sc.get_by_id(o.sample_id)
            print(f"    {o.order_id}  {sample.name if sample else '-'}  "
                  f"{o.customer_name}  {o.quantity:,}개")

    def _process_release(self):
        self._list_confirmed()
        oid   = input("  출고할 주문 ID: ").strip()
        order = self._oc.get_by_id(oid)
        if not order or order.status != OrderStatus.CONFIRMED:
            print("  [오류] 유효한 CONFIRMED 주문이 아닙니다.")
            return
        self._oc.update_status(oid, OrderStatus.RELEASE)
        print(f"  → {oid} 출고 완료: CONFIRMED → RELEASE")
