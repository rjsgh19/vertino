# 프로젝트명: 신도림역 버티포트 증축 설계

## 도메인
sindorim_vertiport

## 개요

신도림역 기존 건축물 옥상에 UAM 버티포트를 증축하는 BIM 기반 설계 자동화 시스템.
Revit/Dynamo 추출 데이터를 온톨로지로 변환한 뒤, 멀티 에이전트가 공간 배치를
생성·채점·수정하는 루프를 반복한다. 최종 산출물은 Revit Transaction으로 커밋된다.

기존 건축물의 배관·코어와 충돌하지 않는 TLOF, FATO, 패드, 기둥 등을 배치하며,
항공법·건축법·OLS(장애물 제한 표면) 규정을 준수해야 한다.

## 도메인 함수

| 함수명 | 파라미터 | 반환 | docstring 필수 |
|--------|----------|------|:--------------:|
| build_initial_ontology_state | bim_extract: dict, prevailing_wind_deg: float | dict | ✓ |
| generate_spatial_layout | state: dict, user_instruction: str, locks: list | dict | ✓ |
| score_compliance_ols | layout: dict, regulations: dict | dict | ✓ |
| score_aero_structure | layout: dict, wind_rose: dict | dict | ✓ |
| score_operation_flow | layout: dict | dict | ✓ |
| merge_audit_reports | reports: list | dict | ✓ |

## 금지 import

revit_api, dynamo, clr, openai, anthropic

## 인바리언트

| ID | 설명 | 검증방법 | 값 |
|----|------|----------|----|
| INV-VP-001 | Layout JSON은 version, elements[], locks_applied 키를 가진다 | required_keys | version, elements, locks_applied |
| INV-VP-002 | 평가자 에이전트 출력에 coordinates 필드가 있으면 SPEC_DRIFT | pattern | ^((?!coordinates).)*$ |
| INV-VP-003 | Compliance 위반 시 verdict는 FAIL이며 layout_agent로 라우팅 | required_keys | verdict |

## 워크플로 단계

| 단계 | 노드 | 실패 시 |
|------|------|---------|
| setup | bim_sync, ontology_bootstrap | - |
| input_generation | parse_instruction, apply_locks, spatial_layout | - |
| multi_agent_audit | compliance_ols, aero_structure, operation_flow | spatial_layout |
| decision_integration | preview_ghost_model, proposal_cards, selective_apply | input_generation |
| finalization | revit_transaction_commit, engineering_report | - |

## 라우팅 규칙

| 조건 | 다음 | 페이로드 |
|------|------|----------|
| all_auditors_pass | decision_integration | - |
| any_auditor_fail | spatial_layout | merged_feedback |

## 에이전트

| 이름 | 역할 요약 | 금지 행위 | 출력 키 |
|------|-----------|-----------|---------|
| supervisor | Spatial Layout이 낸 Layout JSON을 Compliance, Aero-Structure, Operation Flow에 병렬 배포하고 채점표를 취합. 세 평가자 모두 PASS할 때만 프리뷰 단계 진행. 하나라도 FAIL이면 수정 가이드를 합쳐 Layout에 반송. | 좌표·elements 배열 직접 수정 금지. 출력은 JSON만. | routing, merged_feedback, auditor_verdicts, revision_directives |
| spatial_layout | 유일한 Layout 생성자. 온톨로지 state, 사용자 지시, Lock 목록을 받아 TLOF·FATO·패드·기둥 등의 Layout JSON 생성. 기존 배관·코어와 1차 clash 해소. | 법규 수치 직접 재계산 금지. Lock된 element geometry 변경 금지. | layout, self_check |
| compliance_ols | 법규·이격 채점관. Layout JSON in → 리포트 out. | coordinates/elements mutation 금지. 수정 금지. | verdict, violations, legal_refs |
| aero_structure | 하중·풍·소음 채점관. | coordinates/elements mutation 금지. 수정 금지. | verdict, metrics |
| operation_flow | 동선·병목 채점관. | coordinates/elements mutation 금지. 수정 금지. | verdict, bottlenecks |

## 추가 제약

- 생성·수정 대상은 `my-harness-platform/src/` 및 `tests/` 하위만
- 좌표 변경 로직은 `domain/layout/` 또는 Supervisor가 호출하는 Spatial Layout 노드에만
- 평가자(Compliance / Aero / Operation) 모듈은 채점 함수만 — layout JSON mutation 금지
- Revit API 호출은 반드시 `infrastructure/` 어댑터에만

## 테스트 요구사항

| 유형 | 파일명 | 검증 내용 |
|------|--------|-----------|
| unit | test_layout_schema.py | Layout JSON 스키마·lock 반영 |
| unit | test_compliance_scoring.py | OLS 위반 시 FAIL + violation 목록 |
| unit | test_supervisor_routing.py | 3 evaluator PASS 전까지 layout 재호출 |
| integration | test_audit_parallel.py | 병렬 채점 → supervisor merge |
| harness | test_no_coordinate_mutation_in_auditors.py | 평가자가 coordinates 수정 시도 시 실패 |
