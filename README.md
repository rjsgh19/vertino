# Harness Automation Factory

LangGraph 기반 **Spec-driven 자율 소프트웨어 엔지니어링 공장**.

## 핵심 설계 원칙

1. **3대 실속형 에이전트**: Planner / Engineer / Reviewer (합의 노드 제거, 책임 명확화).
2. **State Hell 방지**: traceback은 `storage/traces/` 외부 파일로, State에는 경로만.
3. **Docker 격리 샌드박스**: 생성된 코드는 절대로 호스트에서 실행되지 않는다.
4. **Spec-driven Drift Detection**: AST 추출 → YAML 명세 역검증.
5. **Prompt Contract 검증**: Pydantic 스키마로 마크다운 가이드 위변조 차단.
6. **구간 기반 패치**: `# BEGIN GENERATED` ~ `# END GENERATED`만 덮어씀 — 인간 수정 영역 보호.
7. **디터미니스틱 리플레이**: `temperature=0` 강제 + 스냅샷 저장.

## Quick Start

```bash
pip install -e ".[dev]"
python -m harness_engine.graph.workflow
```

자세한 명령은 `CLAUDE.md` 참조.


------------------------------------------------------
# 🏭 AI 하네스 자동화 공장 플랫폼 (Enterprise AI Software Factory)

본 플랫폼은 **[BIM 기반 인프라 SOC 설계 최적화 서폿 멀티에이전트]**의 핵심 도메인과 비즈니스 로직을 인간의 개입 없이 자율적으로 생성, 검증, 자가 치유(Self-healing)하여 완벽한 클린 아키텍처 산출물을 찍어내는 AI-native 소프트웨어 공장 시스템입니다.


## 🚀 1. 공장 가동 전 필수 문서 작성 가이드라인

공장 엔진(`harness_engine/`)을 가동하여 제품을 생산하기 전, AI 에이전트 연합이 인지해야 할 **최상위 기획 명세, 전역/개별 가이드라인(Spec), 그리고 채점 시험지(TDD)**를 아래 규격에 맞춰 선행 작성해야 합니다.

### 🏛️ 규칙 0. 최상위 프로젝트 마스터 기획 명세 (`agent_runtime/specifications/domain/project_master_spec.yaml`)
공장이 최종적으로 찍어내야 할 **제품의 본질(Revit API, Dynamo 워크플로우 연동 구조)**을 정의하는 전역 기획서입니다. 에이전트들이 분산 오케스트레이션을 시작하는 뿌리 컨텍스트가 됩니다.

* **경로:** `agent_runtime/specifications/domain/project_master_spec.yaml`
* **소스코드:**
```yaml
metadata:
  project_name: "BIM 기반 인프라 SOC 설계 최적화 서폿 멀티에이전트"
  version: "1.0.0"
  target_environment:
    BIM_software: "Autodesk Revit 2026"
    automation_tool: "Dynamo Sandbox / Revit Dynamo"
    language: "Python 3.10+ (IronPython/CPython Adapter)"

project_overview:
  summary: >
    설계자가 레빗(Revit) 및 다이나모(Dynamo)를 통해 추출한 SOC 시설물 및 인프라의 
    지하/지상 배치 데이터(BIM, GIS)를 입력받아, 기후 변화 대응 및 인프라 간섭 규칙을 
    자동으로 연산하고 최적의 대안 배치를 추천 및 채점해 주는 서포트 에이전트 시스템.

core_workflows:
  step_1_ingestion:
    source: "Dynamo Export (JSON / CSV)"
    process: "다이나모 스크립트가 레빗 모델의 형상 정보, 좌표, 패밀리 파라미터를 추출하여 공장 입력단으로 전송"
  step_2_orchestration:
    source: "harness_engine"
    process: "Planner 에이전트가 요구사항을 분석하고, Engineer가 검증 코드를 돌리며, Reviewer가 클린 아키텍처 규격을 감사함"
  step_3_verification:
    source: "Docker Sandbox (pytest)"
    process: "BIM 데이터 구조가 사양 명세(domain_spec.yaml) 및 물리적 간섭 한계치를 통과하는지 TDD 채점 가동"
  step_4_export:
    target: "Dynamo Ingestion Loop"
    process: "최종 최적화된 배치 좌표 및 조정된 파라미터 델타 값을 JSON 매니페스트로 출력하여 다이나모를 통해 레빗 모델에 자동 반영(Reverse Feedback)"

system_agents_definition:
  planner:
    responsibility: "다이나모에서 넘어온 레빗 데이터 구조 및 설계 제약 조건을 분석하여 최적화 시나리오 수립"
  engineer:
    responsibility: "BIM 형상 데이터 간의 물리적 간섭(Interference) 및 기후 복원력 알고리즘 계산 모듈 구현"
  reviewer:
    responsibility: "생성된 최적화 로직이 레빗 파라미터 갱신 규격 및 클린 아키텍처 내부 정책을 준수하는지 최종 검수"

global_constraints:
  - "레빗 API 및 다이나모 노드 구조와의 데이터 호환성을 위해 모든 입출력 인터페이스는 표준화된 JSON 계약(api_contract.yaml)을 따른다."
  - "도메인 레이어는 레빗 프레임워크 종속성 없이 순수 기하학/수학 연산으로만 작동되어야 한다."

```

### 📜 규칙 1. 전역 공통 가이드라인 규격 (`docs/agent_guides/0_global_manifesto.md`)

모든 에이전트(Planner, Engineer, Reviewer)가 코드를 생성하고 검수할 때 공통으로 탑재해야 하는 코딩 표준과 컨벤션 규칙입니다. `prompt_loader.py`가 모든 에이전트 노드의 기본 컨텍스트로 자동 주입합니다.

* **경로:** `docs/agent_guides/0_global_manifesto.md`
* **소스코드:**

```markdown
## ROLE
너는 하네스 공장 플랫폼에 소속된 전문 AI 소프트웨어 엔지니어링 에이전트 연합이다.

## GLOBAL_CONSTRAINTS
- **코딩 표준:** 생성하는 모든 파이썬 코드는 Python Type Hinting을 100% 준수해야 한다.
- **예외 처리:** 예외 발생 가능성이 있는 모든 I/O 및 연산 구간에는 명확한 try-except 블록과 Pydantic validation을 내재화해라.
- **주석 배제:** 코드 자체로 설명이 되는 클린 코드를 지향하며, 불필요한 한글/영어 주석을 코드 내에 남기지 마라.

```

### 📄 규칙 2. 개별 에이전트 지시서 규격 (`docs/agent_guides/1~3_*.md`)

`prompt_loader.py`가 안전 구역 검증(Allowlist Contract Validation)을 수행할 수 있도록, 반드시 아래 4개 헤더 구조(## ROLE, ## CONSTRAINTS, ## OUTPUT_FORMAT, ## EXAMPLES)를 칼같이 엄수해야 합니다.

특히 헛소리를 차단하기 위해 **EXAMPLES 섹션에는 추상적인 설명 대신 실제 다이나모 JSON 구조와 에이전트가 출력해야 할 이스케이프 문자(`\n`) 포함 JSON 정답본을 Few-shot 예제로 강제 바인딩**합니다.

#### ① `docs/agent_guides/1_agent_planner.md`

```markdown
## ROLE
너는 다이나모에서 넘어온 레빗 데이터 구조 및 설계 제약 조건을 분석하여 최적화 시나리오를 수립하는 Planner 에이전트다.

## CONSTRAINTS
- 주어지는 `project_master_spec.yaml`의 핵심 워크플로우에 위배되는 설계를 제안하지 마라.
- 실패 로그가 주어지면 에러가 발생한 지점만 정밀 타격하여 보정(Partial Patch)하도록 명령을 설계해라.

## OUTPUT_FORMAT
설명이나 주석, 마크다운 백틱(```)을 전면 배제하고, 반드시 아래 구조를 만족하는 **유효한 순수 JSON 객체 하나**만 출력해라.
{
  "target_file_path": "str",
  "patch_code": "str"
}

## EXAMPLES
- **실제 Input 데이터 셋 (다이나모 추출 데이터):**
  ```json
  {
    "revit_family": "SOC_Drainage_Pipe",
    "coordinates": {"X": 1500.5, "Y": 2400.0, "Z": -500.0},
    "parameters": {"diameter_mm": 300, "slope_ratio": 0.02}
  }

```

* **너가 출력해야 하는 실제 무결점 JSON 정답 코드:**
```json
{
  "target_file_path": "my-harness-platform/src/domain/design_assistant.py",
  "patch_code": "class DesignScorer:\n    def __init__(self, policy_provider):\n        self.policy = policy_provider\n\n    def calculate_score(self, project_data: dict) -> float:\n        if 'imports' in project_data and 'fastapi' in project_data['imports']:\n            return 50.0\n        return 100.0"
}

```



```

### ⚙️ 규칙 3. 세부 사양 및 아키텍처 금지 정책 (`agent_runtime/specifications/`)
에이전트들의 물리적 이탈과 의존성 오염을 기술적으로 차단하는 디테일 설계 명세입니다.

* **도메인 채점 규칙 명세 (`specifications/domain_spec.yaml`):**
```yaml
metadata:
  spec_name: "design_support_scoring_rules"
  version: "1.0.0"

architecture_metrics:
  dependency_inversion:
    weight: 0.4
    metric_formula: "Score = 100 * (1 - (prohibited_imports_count / total_imports_count))"
  coupling_index:
    weight: 0.3
    max_allowed_classes_per_module: 10
    penalty_per_excess_class: 5

critical_policies:
  min_pass_score: 70
  enforce_hexagonal: true

```

* **인터페이스 및 API 계약서 (`specifications/api_contract.yaml`):**

```yaml
metadata:
  contract_name: "design_assistant_api_contract"
  version: "1.0.0"

endpoints:
  - path: "/api/v1/design/evaluate"
    method: "POST"
    request_body:
      project_name: "str"
      source_files: "List[dict]"
    responses:
      200:
        status: "str"
        total_score: "float"
        violated_rules: "List[str]"

```

* **아키텍처 의존성 금지 정책 (`specifications/architecture_policy.yaml`):**

```yaml
layer_policies:
  domain:
    allowed_imports:
      - "typing"
      - "math"
      - "pydantic"
    prohibited_imports:
      - "fastapi"
      - "sqlalchemy"
      - "requests"
      - "os"
      - "subprocess"
  use_cases:
    allowed_imports:
      - "domain"
    prohibited_imports:
      - "fastapi"
      - "sqlalchemy"

```

### 🧪 규칙 4. 선행 TDD 테스트 하네스 규격 (`my-harness-platform/tests/`)

AI 공장이 샌드박스 내부에서 초록불(Green)을 획득하기 위해 통과해야 할 채점 시험지입니다. AI가 코드를 짜기 전에 미리 리포지토리에 생성해 둡니다.

* **인프라 모킹 하네스 드라이버 (`tests/harnesses/api_harness.py`):**

```python
import pytest

class FakeArchitecturePolicyHarness:
    def __init__(self):
        self.prohibited_tokens = ["os.system", "subprocess.Popen", "eval"]

    def fetch_banned_imports_by_layer(self, layer_name: str) -> list:
        if layer_name == "domain":
            return ["fastapi", "sqlalchemy", "requests"]
        return []

@pytest.fixture
def policy_harness():
    return FakeArchitecturePolicyHarness()

```

* **자율 채점용 유닛 테스트 (`tests/unit/test_design_assistant.py`):**

```python
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

# AI 공장이 자동 생성하여 드롭할 클래스를 선행 import
from domain.design_assistant import DesignScorer

def test_calculate_score_with_perfect_clean_architecture(policy_harness):
    scorer = DesignScorer(policy_provider=policy_harness)
    perfect_code = {
        "layer": "domain",
        "imports": ["typing", "math", "pydantic"],
        "class_count": 4
    }
    final_score = scorer.calculate_score(perfect_code)
    assert final_score == 100

def test_calculate_score_with_architecture_violation(policy_harness):
    scorer = DesignScorer(policy_provider=policy_harness)
    violated_code = {
        "layer": "domain",
        "imports": ["typing", "fastapi"], # 규칙 위반
        "class_count": 3
    }
    final_score = scorer.calculate_score(violated_code)
    assert final_score < 70

```

---

## 🏃‍♂️ 2. 공장 가동 실전 작업 절차 (Step-by-Step)

모든 기획서, 가이드라인, 시험지 파일 세팅이 완료되었다면 아래 절차에 의거하여 공장을 가동합니다.

### Step 1. 가상 샌드박스 환경 확인 및 패키지 설치

노트북에 백그라운드로 **Docker**가 구동 중인지 확인한 후, 루트 경로에서 의존성 라이브러리를 빌드합니다.

```bash
pip install langgraph pydantic docker pyyaml opentelemetry-api

```

### Step 2. 최상위 클로드 절대 규칙 확인 (`.clauderules`)

루트 폴더에 위치한 `.clauderules` 스펙을 점검합니다. 이 파일은 Claude CLI가 켜지자마자 컨텍스트 유실을 막기 위해 자동으로 흡수하는 철칙입니다.

```text
- 모든 코드는 수동 전체 덮어쓰기를 금지하며, # BEGIN GENERATED와 # END GENERATED 마커 기반 패치를 수행해라.
- 인간이 수동 수정한 구역(# @generated 마커가 유실된 곳) 발견 시 즉시 OverwriteError를 발생시켜라.
- 코드 빌드 후에는 커스텀 스킬 `run_harness_tests`를 실행하여 Docker 샌드박스 내부 검증을 수행해라.

```

### Step 3. 클로드 CLI(Claude Code) 가동

VS Code 터미널 창을 열고 에이전트 오케스트레이션 인터페이스를 구동합니다.

```bash
claude

```

### Step 4. 자율 생산 마스터 명령 하달

클로드 CLI 창에 아래 명령어를 그대로 복사해서 던지고 관제를 시작합니다.

> 💬 **"공장 관리 스킬을 실행해서 `agent_runtime/specifications/domain/project_master_spec.yaml` 마스터 기획서와 파싱된 가이드라인들을 기반으로 3대 에이전트 루프를 기동해 줘. `my-harness-platform/tests/` 시험지를 완벽히 패스할 때까지 자가 치유(Self-healing)를 돌려서 `my-harness-platform/src/` 하위에 최종 검증된 레빗/다이나모 최적화 코드를 드롭해라."**

### Step 5. 관제 및 수동 개입 (HITL 휴먼 거버넌스)

* **성공 시:** 에이전트가 Docker 격리 채점을 모두 패스하면 상단에 `# @generated` 마커와 해시값이 찍힌 고품질 소스코드가 레이어별(`domain/`, `use_cases/` 등)로 분할 결합되어 깔끔하게 드롭됩니다.
* **보안 위반 또는 실패 시:** 만약 코드 내 악성 구문 감지(`SECURITY_VIOLATION`), 명세 설계 이탈(`SPEC_DRIFT`), 또는 3회 리트라이 초과 에러가 발생하면 공장은 `interrupt()`를 발생시키고 가동을 일시 정지합니다. 이때 터미널 창에 조언 및 피드백 입력을 주어 디버깅 방향을 가이드해주면 공장이 다시 돌아갑니다.