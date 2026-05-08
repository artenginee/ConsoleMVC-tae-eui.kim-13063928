from interfaces.i_order_controller import IOrderController
from interfaces.i_production_controller import IProductionController
from interfaces.i_sample_controller import ISampleController
from views.order_view import OrderView
from views.production_view import ProductionView


class MainView:
    """역할 선택 메인 메뉴"""

    def __init__(self, sample_ctrl: ISampleController,
                 order_ctrl: IOrderController,
                 prod_ctrl: IProductionController):
        self._prod_view  = ProductionView(sample_ctrl, order_ctrl, prod_ctrl)
        self._order_view = OrderView(sample_ctrl, order_ctrl)

    def run(self):
        while True:
            print("\n===== 반도체 주문/생산 관리 시스템 =====")
            print("1. 생산담당자")
            print("2. 주문담당자")
            print("0. 종료")
            choice = input("선택: ").strip()

            if   choice == "1": self._prod_view.show()
            elif choice == "2": self._order_view.show()
            elif choice == "0": break
            else: print("[오류] 잘못된 선택입니다.")
