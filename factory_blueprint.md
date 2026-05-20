# 🚀 프로젝트 목표: Spec-driven 기반 실속형 자율 소프트웨어 엔지니어링 플랫폼 구축

너는 전 세계 최고 수준의 에이전트 인프라 아키텍트이자 화이트해커급 보안 엔지니어다. 제시된 모든 보안 격리, 상태 최적화, 위변조 방지 피드백을 반영하되, 과최적화된 에이전트 개수와 중복 스캐너를 걷어내고 가장 실속 있고 날카롭게 움직이는 **[Enterprise-grade AI 소프트웨어 공장]**을 LangGraph 기반으로 구축해라. SWE-agent 및 Aider의 핵심 작동 방식을 차용해라.

## 1. 반영할 초고도화 아키텍처 핵심 논리 (Core Principles)

1. **런타임 추상화 및 결합 제거 (Runtime Abstraction):**
   - 특정 AI Vendor 또는 CLI에 종속되지 않는 구조를 구축해라. Claude, OpenAI 관련 외부 연동 기능은 오직 `infrastructure/adapters/` 하위로 격리하고 오케스트레이션 코어 로직과 철저히 분리해라.
2. **실속형 3대 멀티 에이전트 구조 (Multi-agent Consolidation):**
   - 7개의 과도한 에이전트 분화와 말싸움 루프를 유발하는 합의(Consensus) 노드를 전면 제거한다. 대신 명확한 책임을 가진 3대 에이전트로 압축해라.
     - **Planner Agent:** 기능 설계, 로직 플래닝 및 실패 로그 진단/분석 통합 (`agents/planner.py`)
     - **Engineer Agent:** 최초 무결점 코드 생성 및 자가 치유 패치 수정 통합 (`agents/engineer.py`)
     - **Reviewer Agent:** Spec 준수 검사, 코드 리뷰 및 비판 통합 (`agents/reviewer.py`)
3. **State Hell 방지 및 메모리 격리 (State Optimization):**
   - LangGraph State에 무거운 에러 Traceback 전체를 누적하여 저장하는 행위를 금지한다. State에는 오직 최소한의 메타데이터와 파일 경로만 유지하고, 실제 Trace 로그는 외부 `storage/traces/` 폴더에 물리 파일로 격리 저장해라. State는 `ephemeral`과 `persistent` 관점으로 분리해라.
4. **보안 샌드박스 가상 격리 (Docker Isolation):**
   - 생성된 AI 코드의 검증은 로컬이 아닌, `services/sandbox_runner.py`에서 Rootless Docker 컨테이너(또는 임시 가상 공간 Sandbox)를 생성하여 `pytest`를 구동하도록 작성해라. 강력한 Timeout 제약과 임시 워크스페이스 분리를 통해 로컬 호스트 자원 파괴 및 쉘 탈옥을 원천 차단해라.
5. **명세서 기반 생성 및 이탈 역추적 (Spec-driven & Drift Detection):**
   - [Spec ➡️ Validation ➡️ Planning ➡️ Generation ➡️ Verification ➡️ Repair] 흐름을 강제해라.
   - 코드 생성 후 AST 구조를 추출해 원래 명세서 규격과 일치하는지 역검증하는 `services/drift_detector.py` 기초 레이어를 구현해라. Spec과 코드 불일치 시 `FailureType.SPEC_DRIFT`를 발생시켜라.
6. **프롬프트 스키마 계약 및 보안 (Prompt Contract Validation):**
   - `services/prompt_loader.py`에 마크다운 가이드 파싱 후 Pydantic 기반의 `PromptContract` 스키마 검증(Validation) 단계를 추가해라. 가이드 문서의 포맷이 깨졌거나 오염되었을 경우 실행을 즉시 차단하고, 오직 지정된 Allowlist 섹션(## ROLE, ## CONSTRAINTS, ## OUTPUT_FORMAT)만 발췌하여 안전하게 주입해라.
7. **구간 기반 패치 및 매니페스트 (Artifact Guard & Partial Patch):**
   - 전체 Overwrite 생성을 금지한다. 파일 저장 시 `# BEGIN GENERATED`와 `# END GENERATED` 구간 기반 Patch 전략을 사용하여 인간이 직접 수정하고 커스텀 패치한 영역은 절대 덮어쓰지 마라.
   - 코드 드롭 시 상단의 `# @generated` 마커 삽입과 더불어, `my-harness-platform/.generated_manifest.json`에 파일별 SHA-256 해시값과 매핑 스펙을 원자적으로 기록해라. 기존 파일에 마커가 유실되어 있다면 `OverwriteError` 예외를 발생시켜라.
8. **관측 가능성 및 디터미니스틱 리플레이 (Observability & Replay):**
   - LLM 호출 시 `temperature=0`을 강제하고, 실패 재현을 위해 사용된 prompt, spec, tool output의 스냅샷을 `storage/replays/`에 JSON 파일로 물리 저장하는 디터미니스틱 리플레이 구조를 구현해라. 모든 노드 전환 시 Structured Logging과 가상 Trace ID를 부여해 `services/telemetry.py`로 타임라인을 추적해라.

## 2. 구축해야 할 디렉토리 구조 (Target Architecture)
```text
my-harness-automation-factory/        # 🏭 [Main Factory System Root]
├── .clauderules                      # 📌 클로드 CLI 전용 절대 명령 규칙서
├── CLAUDE.md                         # 📌 클로드 CLI 개발 명령어 및 빌드 규격서
├── pyproject.toml                    # 🛠️ 프로젝트 의존성 관리 정의서 (docker, pydantic, pyyaml, langgraph 필수 포함)
├── README.md                         # 👤 인간 개발자를 위한 메인 설명서
├── .env                              # 환경 변수 관리 파일
├── .gitignore                        # Git 관리 제외 설정
│
├── infrastructure/                   # 🔌 [외부 벤더 어댑터 레이어]
│   └── adapters/
│       ├── claude/                   #   - Claude API 인터페이스 격리 구역
│       ├── openai/                   #   - OpenAI API 인터페이스 격리 구역
│       └── aider/                    #   - Aider API 인터페이스 격리 구역
│
├── ⚙️ .claude/                        # 🛠️ [Claude CLI] 전용 환경 및 기억 장소 (자동 생성됨)
│   ├── memory.json                   # 🔄 컨텍스트 유실 방지용 작업 히스토리 기록
│   └── skills/                       # 🧰 커스텀 자동화 파이썬 스킬 모음
│       └── run_harness_tests.py      #   - 샌드박스 구동 스킬 트리거 스크립트
│
├── 🐕 .husky/                        # 🪝 Git Hooks 자동화 폴더 (커밋 전 검증)
│   └── pre-commit                    #   - 커밋 직전 린터 및 테스트 하네스를 강제 실행하는 스크립트
├── 🐙 .github/workflows/             # 🌐 CI/CD 자동화 (GitHub Actions)
│   └── ci.yml                        #   - 푸시/PR 시 자동으로 TDD 테스트를 실행하는 workflow
│
├── agent_runtime/                    # 🧠 [추상화 플랫폼 레이어] (벤더 종속성 0%)
│   ├── memory/                       #   - Ephemeral(휘발성) vs Persistent(영속성) 메모리 분리 구조
│   ├── specifications/               #   - [Spec DSL] 각 규칙 명세서 분리 구역
│   │   ├── domain_spec.yaml          #     * 도메인 핵심 물리 수식/규칙 명세서
│   │   ├── api_contract.yaml         #     * 인터페이스 API 규격 계약서
│   │   └── architecture_policy.yaml  #     * 클린 아키텍처 의존성 금지 규칙 명세서
│   └── policy_engine/                #   - 허용 import, 파일시스템 허용 범위 통제 엔진
│       ├── import_policy.py          
│       └── filesystem_policy.py      
│
├── harness_engine/                   # 🧠 [오케스트레이션 서브 시스템]
│   ├── graph/                        #   - 중앙 제어 및 라우팅 파이프라인
│   │   ├── workflow.py               #     * LangGraph 상태 머신 빌드 스크립트
│   │   ├── routing.py                #     * Pass/Fail 조건부 분기 스크립트
│   │   └── hitl.py                   #     * 인간 수동 개입 인터럽트 제어 스크립트
│   ├── agents/                       #   - 3대 실속형 에이전트 코어 독립화
│   │   ├── planner.py                #     * 기능 설계 및 실패 로그 원인 분석 (Planner + Analyzer)
│   │   ├── engineer.py               #     * 최초 코드 생성 및 자가 치유 패치 수정 (Generator + Repairer)
│   │   └── reviewer.py               #     * 스펙 준수 검사 및 코드 비판 리뷰 (Validator + Critic)
│   ├── services/                     #   - 샌드박싱 및 보안 유틸리티 인프라
│   │   ├── prompt_loader.py          #     * Pydantic (PromptContract) 기반 안전 섹션 파서
│   │   ├── spec_loader.py            #     * YAML 스펙 데이터 로더
│   │   ├── sandbox_runner.py         #     * Docker 컨테이너 기반 격리 테스트 실행기
│   │   ├── drift_detector.py         #     * 코드 ➡️ AST 추출 후 Spec 역비교 디텍터
│   │   ├── artifact_writer.py        #     * # BEGIN/END GENERATED 구간 기반 패치 스크립트
│   │   ├── replay_store.py           #     * 리플레이 스냅샷 JSON 입출력 스크립트
│   │   └── telemetry.py              #     * Structured Logging 및 가상 Trace ID 매핑기
│   └── state/                        
│       ├── ephemeral_state.py        #     * 휘발성 노드 상태 스키마
│       ├── persistent_state.py       #     * 영속성 체크포인트 상태 스키마
│       └── failure_types.py          #     * 확장된 FailureType Enum 선언 파일
│
├── storage/                          # 📦 [격리 저장소] State Explosion 방지용 대용량 파일 덤프 공간
│   ├── traces/                       #   - pytest 에러 traceback 덤프 로그 저장 폴더
│   ├── replays/                      #   - 디터미니스틱 리플레이용 JSON 스냅샷 저장 폴더
│   └── telemetry/                    #   - 에이전트 실행 타임라인 정형 구조화 로그 저장 폴더
│
└── ⚡ my-harness-platform/           # 📦 [Output System] 최종 자동 생성 시스템 결과물 디렉토리
    ├── .generated_manifest.json      # 🧾 생성물 위변조 및 해시 추적용 매니페스트 파일
    ├── tests/                        # 🧪 TDD 검증을 위해 선행 작성된 테스트 하네스 슈트
    │   ├── harnesses/                #   - db_harness.py, api_harness.py (인프라 모킹 하네스)
    │   ├── integration/              #   - 모듈 간 결합 통합 테스트
    │   └── unit/                     #   - 순수 로직 검증 단위 테스트 (Red-Green 반복 구역)
    │
    └── src/                        # ✨ 스킬과 룰을 통과해 "최종 자동 생성된" 클린 코드 구현부
        ├── config/                   #   - 환경 변수 및 전역 설정
        ├── domain/                   #   - 순수 핵심 도메인 로직 및 물리 수식 (외부 의존성 0%)
        ├── use_cases/                #   - 애플리케이션 서비스 (비즈니스 흐름 제어)
        ├── interfaces/               #   - 포트(Port) 레이어 (인터페이스 및 DTO 정의)
        └── infrastructure/           #   - 어댑터(Adapter) 레이어 (FastAPI, DB 등 실제 기술 구현부)
## 3. 단계별 작업 지시 (Action Plan)
나에게 중간에 질문하지 말고 아래 순서에 의거하여 예외 처리와 엔터프라이즈 아키텍처 패턴을 적용해 즉시 모든 소스코드를 완성해 나가라.

Step 1: 최종 고도화된 디렉토리 구조에 맞춰 폴더들을 완벽히 생성하고, pyproject.toml에 langgraph, pydantic, docker, pyyaml, opentelemetry-api 의존성을 명시해라. 최상위 규칙 파일들(.clauderules, CLAUDE.md, .husky/pre-commit, .github/workflows/ci.yml)의 초기 인프라 뼈대 내용을 채워라.

Step 2: harness_engine/state/failure_types.py에 확장된 FailureType Enum(SYNTAX, IMPORT_ERROR, TYPE_ERROR, TEST_ASSERTION, SECURITY_VIOLATION, RESOURCE_LIMIT, INFRA_TIMEOUT, SPEC_DRIFT, UNKNOWN)을 선언하고, ephemeral_state.py와 persistent_state.py에 State Explosion을 방어할 정제된 상태 모델 구조체를 정의해라. (Traceback 문자열의 직접 저장은 금지하며 오직 storage 파일 경로만 바인딩)

Step 3: harness_engine/services/ 하위에 Pydantic 계약 기반 및 허용 섹션만 발췌 파싱하는 prompt_loader.py, Docker 및 타임아웃 격리 채점 스크립트인 sandbox_runner.py, 코드 트리를 추적해 Spec 역비교를 감행하는 drift_detector.py, 매니페스트 위변조 검증 및 인간 코드 구간 보호 오버라이트 방어 로직을 포함한 artifact_writer.py, 그리고 structured logging을 담당할 telemetry.py를 정밀하게 코딩해라.

Step 4: harness_engine/graph/ 하위에 LangGraph 상태 머신(workflow.py, routing.py, hitl.py)을 완성해라. docs/agent_guides/ 안의 마크다운 지시서를 실시간 open() 및 read()로 파싱 후 계약 검증하여 각 노드에 주입하는 로직을 구현해라. 특히 [코드 생성 ➡️ drift_detector 명세 대조 ➡️ sandbox_runner 격리 채점 ➡️ 통과 시에만 artifact_writer를 통해 매니페스트 갱신 및 최종 드롭] 순으로 이어지는 원자적 파이프라인 흐름을 강제해라. 만약 3회 이상 실패하거나 보안 위반(SECURITY_VIOLATION), 인프라 타임아웃(INFRA_TIMEOUT), 명세 이탈(SPEC_DRIFT) 발생 시 즉시 해당 예외를 캐치하여 interrupt()를 발생시켜 개발자 입력을 대기하는 HITL 로직을 완벽히 연동하여 코딩해라.