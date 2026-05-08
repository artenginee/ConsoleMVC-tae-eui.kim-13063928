# 반도체 주문/생산 관리 시스템 — POC-1 MVC Skeleton

---

## POC 구성

| POC | 내용 | 상태 |
|-----|------|------|
| **POC-1** | MVC 스켈레톤 — 패키지 구조 및 역할 분리 | ✅ 현재 |
| POC-2 | 데이터 영속성 — 파일 / JSON / DB | 예정 |
| POC-3 | 데이터 모니터링 도구 | 예정 |
| POC-4 | 더미 데이터 생성 도구 | 예정 |

---

## 실행 / 테스트

```bash
python main.py                              # 애플리케이션 실행 (Python 3.10+)

pip install -r requirements-dev.txt        # 테스트 의존성 설치
pytest tests/test_models.py -v             # 모델 테스트 (현재 전체 통과)
pytest tests/test_controllers.py -v        # 컨트롤러 계약 테스트 (POC-2 이후 통과)
pytest -v                                  # 전체 실행
```

---

## MVC 패키지 구조

```
ConsoleMVC/
├── models/          Model   — 순수 데이터 클래스, 로직 없음
├── interfaces/      (공통)  — 컨트롤러 계약 정의 (ABC)
├── controllers/     Controller — 인터페이스 구현체, 현재 pass 스텁
├── views/           View    — 콘솔 입출력, 인터페이스 타입으로 컨트롤러 참조
└── tests/           계약 테스트 (모델) + 구현 명세 (컨트롤러)
```

---

## 레이어 역할 분리

### Model
- `@dataclass` 로 정의된 순수 데이터 구조
- 로직·의존성 없음, 다른 레이어를 import하지 않음
- `Sample` / `Order` / `ProductionJob` / `OrderStatus`

### Interface
- `abc.ABC` + `@abstractmethod` 로 Controller 계약 정의
- View가 구체 클래스 대신 인터페이스를 참조함으로써 구현체 교체 가능
- `ISampleController` / `IOrderController` / `IProductionController`

### Controller
- 인터페이스를 상속하여 메서드 시그니처 보장
- 비즈니스 로직은 POC-2에서 구현 (`pass` 스텁 상태)
- View를 import하지 않음 — 단방향 의존성 준수

### View
- `print` / `input` 만 담당, 판단 로직 없음
- 생성자에서 인터페이스 타입으로 Controller를 주입받음
- `MainView` → `ProductionView` (생산담당자) / `OrderView` (주문담당자)

---

## 의존 방향

```
View  →  Interface  ←  Controller  →  Model
```

`main.py` 에서 구체 Controller를 생성해 View에 주입 (생성자 주입).  
POC-2에서 Controller 구현체를 교체해도 View · Interface · Model 은 수정 불필요.

---

## 테스트 전략

| 파일 | 대상 | 현재 상태 |
|------|------|-----------|
| `tests/test_models.py` | Model 데이터 구조 검증 | ✅ 전체 통과 |
| `tests/test_controllers.py` | 인터페이스 구현 확인 | ✅ 통과 |
| `tests/test_controllers.py` | Controller 동작 계약 명세 | ⏳ POC-2 구현 후 통과 |
