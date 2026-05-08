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

레이어 간 의존 방향: `View → Controller → Model`

**Model** (`models/`) — 순수 데이터 클래스(`@dataclass`). 로직 없음.
- `OrderStatus` Enum: `RESERVED → PRODUCING / CONFIRMED → RELEASE` (거절 시 `REJECTED`)
- `Sample`: 시료 (avg_production_time, yield_rate, inventory)
- `Order`: 주문 (sample_id 참조, status 필드로 상태 추적)
- `ProductionJob`: 생산 작업 (shortfall, actual_production_qty, total_production_time)

**Controller** (`controllers/`) — 메서드 시그니처만 정의된 스켈레톤. 구현부는 `pass`. View를 import하지 않는다.
- `SampleController`: 시료 CRUD + 재고 증감 인터페이스
- `OrderController`: 주문 생성·상태 변경·상태별 조회 인터페이스
- `ProductionController`: 생산 큐(`deque`) 등록·조회·완료 인터페이스

**View** (`views/`) — `print` / `input` 담당. Controller 메서드를 호출하는 것 외에 판단 로직 없음.
- `MainView`: 역할 선택 (생산담당자 / 주문담당자)
- `ProductionView`: 생산담당자 전체 화면 (시료 관리, 승인/거절, 생산 라인)
- `OrderView`: 주문담당자 전체 화면 (주문 예약, 모니터링, 출고)

`main.py`에서 세 Controller를 생성한 뒤 생성자 주입으로 View에 전달한다.

## POC-2 확장 가이드

Controller의 `pass` 메서드에 구현을 채우고, `self._samples` / `self._orders` / `self._queue` 를 Repository 객체로 교체하면 된다. View와 Model은 변경 불필요.
