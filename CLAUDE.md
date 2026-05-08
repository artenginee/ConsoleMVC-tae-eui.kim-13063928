# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 실행

```bash
python main.py
```

표준 라이브러리만 사용하므로 별도 패키지 설치 불필요. Python 3.10+ 필수 (`match` 문 사용).

## 프로젝트 개요

반도체 주문/생산 관리 콘솔 애플리케이션. 총 4개의 POC로 구성되며 이 저장소는 **POC-1 (MVC 스켈레톤)** 구현체다.

- POC-2: 데이터 영속성 (파일/JSON/DB)
- POC-3: 데이터 모니터링 도구
- POC-4: 더미 데이터 생성 도구

## MVC 아키텍처

세 레이어는 단방향으로만 의존한다: `View → Controller → Model`

**Model** (`models/`) — 순수 데이터 클래스(`@dataclass`). 로직 없음.
- `OrderStatus` Enum: `RESERVED → PRODUCING / CONFIRMED → RELEASE` (거절 시 `REJECTED`)
- `Sample`: 시료 (avg_production_time, yield_rate, inventory 보유)
- `Order`: 주문 (sample_id 참조, status 필드로 상태 추적)
- `ProductionJob`: 생산 작업 (shortfall, actual_production_qty, total_production_time)

**Controller** (`controllers/`) — 비즈니스 로직 + in-memory 저장소. View를 import하지 않는다.
- `SampleController`: 시료 CRUD, 재고 증감(`add_inventory` / `deduct_inventory`)
- `OrderController`: 주문 생성·상태 변경, 상태별 조회
- `ProductionController`: FIFO 큐(`deque`), `enqueue` 시 자동으로 첫 작업 시작

**View** (`views/`) — `print` / `input` 담당. 비즈니스 판단 없이 Controller만 호출.
- `MainView`: 역할 선택(생산담당자 / 주문담당자)
- `ProductionView`: 생산담당자 전체 화면 (시료 관리, 승인/거절, 생산 라인)
- `OrderView`: 주문담당자 전체 화면 (주문 예약, 모니터링, 출고)

`main.py`에서 세 Controller를 생성한 뒤 생성자 주입으로 View에 전달한다.

## 핵심 비즈니스 규칙

**주문 승인 분기** (`ProductionView._approve_order`):
- 재고 충분(`inventory >= quantity`) → 재고 차감 후 즉시 `CONFIRMED`
- 재고 부족 → `shortfall = quantity - inventory` 계산, `ProductionController.enqueue` 호출 후 `PRODUCING`

**실 생산량 공식** (`ProductionController.enqueue`):
```
actual_qty = ceil(shortfall / (yield_rate × 0.9))
total_time = avg_production_time × actual_qty
```

**생산 완료 시 재고 반영** (`ProductionView._complete_job`):
```
good_units = int(actual_production_qty × yield_rate)
inventory += good_units      # 양품 입고
inventory -= order.quantity  # 주문 수량 출고
order.status = CONFIRMED
```

## 데이터 ID 규칙

| 엔티티 | 형식 | 예시 |
|---|---|---|
| Sample | `S{counter:03d}` | `S001` |
| Order | `O{counter:04d}` | `O0001` |
| ProductionJob | `J{counter:04d}` | `J0001` |

## POC-2 확장 시 유의사항

영속성 레이어를 추가할 때 Controller의 in-memory 리스트(`self._samples`, `self._orders`, `self._queue`)를 Repository 객체로 교체하면 된다. View와 비즈니스 로직은 변경 불필요.
