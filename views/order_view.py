from interfaces.i_order_controller import IOrderController
from interfaces.i_sample_controller import ISampleController
from models.order_status import OrderStatus


class OrderView:
    """주문담당자 화면: 시료 주문 / 모니터링 / 출고 처리"""

    def __init__(self, sample_ctrl: ISampleController, order_ctrl: IOrderController):
        self._sc = sample_ctrl
        self._oc = order_ctrl

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

    def _order_menu(self):
        while True:
            print("\n[ 시료 주문 ]")
            print("1. 주문 예약")
            print("2. 시료 목록 보기")
            print("0. 뒤로")
            choice = input("선택: ").strip()

            if   choice == "1": self._oc.create(input("시료 ID: "), input("고객명: "), int(input("수량: ")))
            elif choice == "2": self._sc.find_all()
            elif choice == "0": break

    def _monitoring_menu(self):
        while True:
            print("\n[ 모니터링 ]")
            print("1. 주문량 확인 (상태별)")
            print("2. 재고량 확인 (시료별)")
            print("0. 뒤로")
            choice = input("선택: ").strip()

            if   choice == "1":
                for status in [OrderStatus.RESERVED, OrderStatus.PRODUCING,
                               OrderStatus.CONFIRMED, OrderStatus.RELEASE]:
                    self._oc.find_by_status(status)
            elif choice == "2": self._sc.find_all()
            elif choice == "0": break

    def _release_menu(self):
        while True:
            print("\n[ 출고 처리 ]")
            print("1. 출고 대기 목록 (CONFIRMED)")
            print("2. 출고 실행")
            print("0. 뒤로")
            choice = input("선택: ").strip()

            if   choice == "1": self._oc.find_by_status(OrderStatus.CONFIRMED)
            elif choice == "2": self._oc.update_status(input("주문 ID: "), OrderStatus.RELEASE)
            elif choice == "0": break
