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

            if   choice == "1": self._sc.add(None, None, None)
            elif choice == "2": self._sc.get_all()
            elif choice == "3": self._sc.search_by_name(input("검색어: "))
            elif choice == "4": self._sc.update(None, None, None, None)
            elif choice == "5": self._sc.delete(input("시료 ID: "))
            elif choice == "0": break

    # ── 2. 주문 승인 / 거절 ────────────────────────────────────────────

    def _approval_menu(self):
        while True:
            print("\n[ 주문 승인 / 거절 ]")
            print("1. 접수 주문 목록 (RESERVED)")
            print("2. 주문 승인")
            print("3. 주문 거절")
            print("0. 뒤로")
            choice = input("선택: ").strip()

            if   choice == "1": self._oc.get_by_status(OrderStatus.RESERVED)
            elif choice == "2": self._oc.update_status(input("주문 ID: "), OrderStatus.CONFIRMED)
            elif choice == "3": self._oc.update_status(input("주문 ID: "), OrderStatus.REJECTED)
            elif choice == "0": break

    # ── 3. 생산 라인 ───────────────────────────────────────────────────

    def _production_menu(self):
        while True:
            print("\n[ 생산 라인 ]")
            print("1. 현재 생산 현황")
            print("2. 대기 큐 확인")
            print("3. 생산 완료 처리")
            print("0. 뒤로")
            choice = input("선택: ").strip()

            if   choice == "1": self._pc.get_current()
            elif choice == "2": self._pc.get_queued()
            elif choice == "3": self._pc.complete_current()
            elif choice == "0": break
