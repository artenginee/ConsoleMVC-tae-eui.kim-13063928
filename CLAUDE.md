# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 실행

```bash
python main.py
```

표준 라이브러리만 사용하므로 별도 패키지 설치 불필요. Python 3.10+ 필수 (`match` 문 사용).

## 테스트

```bash
# 모델 테스트 (현재 전체 통과)
python -m unittest tests.test_models -v

# 컨트롤러 계약 테스트 (인터페이스 구현 확인은 통과 / 나머지는 POC-2 구현 후 통과)
python -m unittest tests.test_controllers -v

# 전체 실행
python -m unittest discover tests -v
```

## 프로젝트 개요

반도체 주문/생산 관리 콘솔 애플리케이션. 총 4개의 POC로 구성되며 이 저장소는 **POC-1 (MVC 스켈레톤)** 구현체다.

- POC-2: 데이터 영속성 (파일/JSON/DB)
- POC-3: 데이터 모니터링 도구
- POC-4: 더미 데이터 생성 도구

## 아키텍처

레이어 간 의존 방향: `View → Interface ← Controller → Model`

```
interfaces/    ← 레이어 연결 계약 (ABC)
  ISampleController
  IOrderController
  IProductionController

models/        ← 순수 데이터 클래스 (@dataclass), 로직 없음
controllers/   ← ISampleController 등 구현, 현재 pass 스텁
views/         ← 인터페이스 타입으로 Controller 참조, print/input만 담당
```

`main.py`에서 구체 Controller를 생성해 View에 주입한다. View는 인터페이스 타입(`ISampleController` 등)을 참조하므로 POC-2에서 구현체를 교체해도 View 수정이 없다.

## 주문 상태 흐름

```
RESERVED → (승인) → PRODUCING → CONFIRMED → RELEASE
         → (거절) → REJECTED
         → (재고 충분 시 승인) → CONFIRMED → RELEASE
```

## POC-2 확장 가이드

1. 각 Controller의 `pass` 메서드에 구현을 채운다.
2. `self._samples` / `self._orders` / `self._queue` 를 Repository 객체로 교체한다.
3. `tests/test_controllers.py` 의 계약 테스트가 전체 통과하면 완료.
