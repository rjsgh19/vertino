# Harness Automation Factory

LangGraph 기반 **Spec-driven 자율 소프트웨어 엔지니어링 공장**입니다.

어떤 프로젝트든 **PRD(제품 요구사항 정의서) 마크다운 문서** 하나만 작성해서 이 공장에 넣으면, 
해당 시스템을 처음부터 생성하고 검증할 수 있는 코드 뼈대, 에이전트 가이드, YAML 명세서, 테스트 스캐폴드를 100% 자동 생성해 줍니다.

---

## ✨ 주요 기능

1. **PRD 기반 원클릭 공장 세팅**
   - 도메인 특화 PRD(Markdown)를 LLM이 100% 동적 파싱하여 프로젝트 규격을 추출합니다.
   - 추출된 규격을 바탕으로 도메인 명세서(YAML), 워크플로 명세서(YAML), 에이전트 가이드(MD), 단위 테스트 스캐폴드(Python)를 자동 생성합니다.
2. **3대 실속형 공장 에이전트 (Planner / Engineer / Reviewer)**
   - 생성된 명세서를 바탕으로 **코드 변경 계획 수립 → 코드 작성(패치) → 샌드박스 품질 판정** 파이프라인을 원자적으로 수행합니다.
3. **Spec-driven Drift Detection (명세 기반 오류 탐지)**
   - AST(추상 구문 트리)를 추출하여 생성된 코드가 YAML 명세서와 1:1로 일치하는지 역검증합니다.
4. **Docker 격리 샌드박스**
   - 생성된 코드는 호스트가 아닌 격리된 Docker 컨테이너 내부에서 실행 및 채점되어 100% 보안을 보장합니다.

---

## 📂 디렉토리 구조

```text
.
├── .claude/
│   └── skills/              # PRD 파싱 및 공장 자동화 스크립트 (prd_to_factory.py 등)
├── agent_runtime/           # [공장] 벤더 비종속 추상화 레이어 (memory, specifications)
├── docs/
│   ├── prd/                 # 사용자가 작성할 PRD 마크다운 문서들
│   └── agent_guides/        # 각 에이전트 노드에 주입될 마크다운 지시서 (자동 생성됨)
├── harness_engine/          # [공장] LangGraph 오케스트레이션 코어 (graph, agents, services)
├── infrastructure/          # [공장] Claude / OpenAI 외부 LLM 어댑터
├── my-harness-platform/     # [최종 산출물] 공장이 만들어낸 결과물(src, tests)이 드롭되는 곳
└── storage/                 # 시스템 동작 로그, traces, replays, telemetry 격리 저장소
```

---

## 🚀 빠른 시작 (Quick Start)

### 1. 환경 설정

```bash
# 의존성 설치
pip install -e ".[dev]"
```

최상위 경로에 `.env` 파일을 생성하고 LLM API 키를 입력합니다 (Claude 기반 권장).
```env
ANTHROPIC_API_KEY="sk-ant-..."
# 또는
# OPENAI_API_KEY="sk-..."
```
*(참고: Docker Desktop이 샌드박스 테스트 실행을 위해 로컬에 켜져 있어야 합니다.)*

### 2. PRD 문서로 산출물 자동 생성

준비된 PRD 마크다운 문서를 입력으로 주어 공장 가동을 위한 뼈대를 10여초 만에 생성합니다.
```bash
# 실제 문서 생성
python .claude/skills/prd_to_factory.py --prd docs/prd/my_project_prd.md

# 미리보기 (실제 쓰기 없이 파싱 결과만 확인)
python .claude/skills/prd_to_factory.py --prd docs/prd/my_project_prd.md --dry-run
```

### 3. 하네스 엔진(공장) 가동

산출물 세팅이 완료되면 3대 에이전트 루프를 실행하여 실제 코드를 작성하고 샌드박스에서 검증합니다.
```bash
python -m harness_engine.graph.workflow
```

---

## 📄 PRD 작성 가이드 (템플릿)

이 공장이 코드를 정확히 생성하려면 PRD 파일(`docs/prd/my_project_prd.md`) 내에 **반드시 표 형태**로 다음 내용이 포함되어야 합니다.

- **도메인 함수**: 에이전트들이 호출할 도메인 로직의 시그니처 (이름, 파라미터, 반환형)
- **인바리언트**: 시스템 불변식 (필수 JSON 키, 정규식 등 데이터 검증 기준)
- **워크플로 / 라우팅 규칙**: LangGraph 상태 머신의 노드 흐름
- **에이전트**: 에이전트 역할과 출력 JSON 스키마
- **테스트 요구사항**: TDD를 위한 검증 리스트

<details>
<summary>💡 PRD 예시 템플릿 보기 (클릭하여 펼치기)</summary>

```markdown
# 프로젝트명: Example Project

## 도메인
example_domain

## 도메인 함수
| 함수명 | 파라미터 | 반환 | docstring 필수 |
|--------|----------|------|:--------------:|
| generate_layout | state: dict, user_instruction: str | dict | ✓ |
| score_compliance | layout: dict, regulations: dict | dict | ✓ |

## 인바리언트
| ID | 설명 | 검증방법 | 값 |
|----|------|----------|----|
| INV-EX-001 | Payload JSON은 version, elements 키 필수 | required_keys | version, elements |

## 워크플로 단계
| 단계 | 노드 | 실패 시 |
|------|------|---------|
| input_generation | parse_instruction, generate_layout | - |
| audit | score_compliance | generate_layout |

## 라우팅 규칙
| 조건 | 다음 | 페이로드 |
|------|------|----------|
| any_auditor_fail | generate_layout | merged_feedback |

## 에이전트
| 이름 | 역할 요약 | 금지 행위 | 출력 키 |
|------|-----------|-----------|---------|
| generate_layout | 유일한 Layout 생성자 | 법규 수치 직접 계산 금지 | layout, self_check |
| score_compliance | 법규 이격 채점관 | state 직접 수정 금지 | verdict, violations |

## 테스트 요구사항
| 유형 | 파일명 | 검증 내용 |
|------|--------|-----------|
| unit | test_layout_schema.py | Layout JSON 스키마 반영 확인 |
```
</details>

---

## 🛠️ 코드 수정 및 유지보수 (Drift Detection & Patching)

이 공장은 코드를 처음부터 덮어쓰는(Overwrite) 방식이 아니라, 기존 코드를 읽고 **변경이 필요한 부분만 찾아 외과 수술하듯 패치(Patch)**합니다.
따라서 에이전트를 추가/삭제하거나 역할을 수정하고 싶을 때, 코드를 직접 건드리는 대신 **PRD 명세서만 수정하고 공장을 다시 가동하는 것**을 권장합니다.

1. **Drift Detection (차이 탐지)**: 공장을 가동하면 `Reviewer` 에이전트가 현재 작성된 파이썬 코드의 AST(추상 구문 트리)를 분석합니다. 이를 새로 업데이트된 YAML 명세서와 비교하여 누락되거나 변경된 '차이(Drift)'를 정확히 찾아냅니다.
2. **Planner의 패치 계획**: `Planner`는 이 차이점 보고서를 분석하여, 파일 전체가 아닌 '어느 파일의 몇 번째 줄을 수정할지' 국소적인 변경 계획을 세웁니다.
3. **안전한 구간 기반 패치**: `Engineer` 에이전트는 코드 내의 `# BEGIN GENERATED` 와 `# END GENERATED` 특수 마커 사이의 구역만 타겟팅하여 코드를 수정합니다.

> 💡 **수동으로 코드를 짤 때 주의사항**
> 사용자가 생성 마커(`BEGIN/END GENERATED`) **바깥 공간**에 작성한 커스텀 로직은 공장이 절대 건드리지 않으며 100% 안전하게 보호됩니다. 반대로 마커 안쪽 코드를 임의로 수정하면, 다음 공장 가동 시 명세서(YAML)를 기준으로 덮어씌워지므로 주의하세요.

---

## ⚙️ 아키텍처 및 역할 구분

이 저장소는 어플리케이션을 직접 서비스하는 것이 아니라, **어플리케이션을 만들어내는 공장**입니다.

### 공장(Factory) vs 애플리케이션 에이전트
| 구분 | 에이전트 | 역할 |
|------|----------|------|
| **공장** (이 저장소) | Planner | YAML 명세 + 실패 로그 → 변경 **계획** JSON |
| | Engineer | 계획 → `my-harness-platform/` **코드 패치** (안전한 구간 기반 패치) |
| | Reviewer | drift + sandbox + spec → **PASS/FAIL** 판단 |
| **애플리케이션** (생성 대상 예시) | Supervisor | 라우팅·취합·재설계 루프 (PRD에 따라 동적 구성) |
| | Task Agent | 도메인별 실제 작업 수행자 (PRD에 따라 동적 구성) |
| | Evaluator | 작업 결과물 검증/채점자 (수정 권한 없음) |

> 공장은 대상 시스템의 코드와 에이전트 가이드 마크다운을 찍어내고, 그렇게 생성된 대상(애플리케이션) 에이전트들은 도메인에 특화된 데이터 구조(JSON)를 주고받으며 자신들의 목적을 달성하게 됩니다.
