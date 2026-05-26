# @generated
"""infrastructure.adapters — Claude / OpenAI / Aider 벤더 격리 진입점.

이 모듈 외부에서는 절대로 벤더 SDK를 import해서는 안 된다.
LLM 호출은 본 패키지의 `LLMAdapter` 프로토콜을 통해서만 이루어진다.
"""
# BEGIN GENERATED
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class LLMRequest:
    """벤더 비종속 LLM 호출 요청.

    프롬프트 캐싱 최적화를 위해 내용을 3계층으로 분리한다:
      [1] system_prompt       — 정적 가이드 (ROLE/CONSTRAINTS/OUTPUT_FORMAT)  ← 캐시 대상
      [2] static_spec_context — 세미정적 스펙 요약 (프로젝트 수명 동안 고정) ← 캐시 대상
      [3] user_prompt         — 동적 페이로드 (에러 로그, 계획 등)           ← 매번 변동
    접두사 일치(prefix matching) 캐싱이므로 [1]→[2]→[3] 순서를 반드시 지켜야 한다.
    """

    system_prompt: str
    user_prompt: str
    temperature: float = 0.0       # 결정성 강제 — 절대 수정 금지
    max_tokens: int = 4096
    static_spec_context: str = ""  # 세미정적 스펙 컨텍스트 — 가이드 직후, 동적 내용 직전 배치
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LLMResponse:
    """벤더 비종속 LLM 호출 응답."""

    text: str
    model: str
    finish_reason: str
    usage: dict[str, int] = field(default_factory=dict)


class LLMAdapter(Protocol):
    """모든 벤더 어댑터가 만족해야 하는 프로토콜."""

    name: str

    def complete(self, request: LLMRequest) -> LLMResponse: ...


__all__ = ["LLMRequest", "LLMResponse", "LLMAdapter"]
# END GENERATED
