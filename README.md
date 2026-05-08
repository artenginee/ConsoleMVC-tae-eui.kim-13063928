# 반도체 주문/생산 관리 시스템

콘솔 기반 반도체 시료 주문 및 생산 관리 애플리케이션 (Python MVC)

---

## POC 구성

| POC | 내용 | 상태 |
|-----|------|------|
| **POC-1** | MVC 스켈레톤 — 패키지 구조 및 역할 분리 | ✅ 현재 |
| POC-2 | 데이터 영속성 — 파일 / JSON / DB | 예정 |
| POC-3 | 데이터 모니터링 도구 | 예정 |
| POC-4 | 더미 데이터 생성 도구 | 예정 |

---

## 실행

```bash
python main.py        # Python 3.10+, 외부 패키지 불필요
```

테스트:

```bash
python -m unittest discover tests -v
```

---

## 아키텍처

의존 방향: `View → Interface ← Controller → Model`

```
ConsoleMVC/
├── models/          데이터 클래스 (@dataclass), 로직 없음
├── interfaces/      컨트롤러 계약 정의 (ABC)
├── controllers/     인터페이스 구현체, 현재 pass 스텁
├── views/           콘솔 UI, 인터페이스 타입으로 컨트롤러 참조
└── tests/           모델 테스트(통과) + 컨트롤러 계약 테스트(POC-2 이후 통과)
```

View는 인터페이스 타입만 참조하므로 POC-2에서 Controller 구현체를 교체해도 View 수정이 없다.

---

## 도메인 모델

**시료 (Sample)** — 생산 대상 반도체 시료

| 필드 | 설명 |
|------|------|
| `sample_id` | 자동 부여 식별자 (`S001`, `S002`, …) |
| `name` | 시료명 (예: DRAM-16G, NAND-256G) |
| `avg_production_time` | 평균 생산시간 (시간/개) |
| `yield_rate` | 수율 (0.0 ~ 1.0) |
| `inventory` | 현재 재고 수량 |

**주문 (Order)** — 고객 주문 단위

| 필드 | 설명 |
|------|------|
| `order_id` | 자동 부여 식별자 (`O0001`, …) |
| `sample_id` | 주문 시료 참조 |
| `customer_name` | 고객명 |
| `quantity` | 주문 수량 |
| `status` | 주문 상태 (아래 흐름 참고) |

**주문 상태 흐름**

```
주문 접수
    └─ RESERVED
          ├─ 거절 → REJECTED
          ├─ 승인 (재고 충분) → CONFIRMED → RELEASE
          └─ 승인 (재고 부족) → PRODUCING → CONFIRMED → RELEASE
```

---

## 역할별 기능

### 생산담당자
- **시료 관리** — 등록 / 목록 조회 / 검색 / 수정 / 삭제
- **주문 승인·거절** — RESERVED 목록 확인 후 승인 또는 거절
- **생산 라인** — 현재 생산 현황, 대기 큐(FIFO) 확인, 생산 완료 처리

### 주문담당자
- **시료 주문** — 시료 ID / 고객명 / 수량 입력 → RESERVED 상태로 접수
- **모니터링** — 상태별 주문 현황, 시료별 재고 현황 (여유 / 부족 / 고갈)
- **출고 처리** — CONFIRMED 주문을 RELEASE로 전환

---

## POC-2 확장 방법

Controller의 `pass` 메서드에 구현을 채우고, 내부 리스트(`_samples`, `_orders`, `_queue`)를 Repository 객체로 교체한다. `tests/test_controllers.py`의 계약 테스트가 전체 통과하면 완료.
