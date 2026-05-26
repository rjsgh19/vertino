# @generated
"""Claude API 어댑터 격리 구역.

벤더 SDK(`anthropic`) 임포트는 본 모듈로만 한정한다. 부재 시 명확한
ImportError를 발생시키며, 절대로 호스트 폴백 LLM 호출을 시도하지 않는다.
"""
# BEGIN GENERATED
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from .. import LLMAdapter, LLMRequest, LLMResponse


@dataclass
class ClaudeAdapter(LLMAdapter):
    name: str = "claude"
    model: str = "claude-opus-4-7"
    api_key_env: str = "ANTHROPIC_API_KEY"

    def complete(self, request: LLMRequest) -> LLMResponse:
        try:
            import anthropic  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "anthropic SDK 미설치 — 어댑터 외부에서 호스트 폴백 금지"
            ) from exc

        api_key = os.environ.get(self.api_key_env)
        if not api_key:
            raise RuntimeError(f"환경변수 {self.api_key_env} 미설정")

        client = anthropic.Anthropic(api_key=api_key)

        # === 프롬프트 캐싱 최적화 (정적 앞단 고정) ===
        # 접두사 일치 캐싱이므로 반드시 [정적 가이드 → 세미정적 스펙 → 동적 내용] 순서를 지킨다.
        system_blocks: list[dict[str, Any]] = [
            {
                "type": "text",
                "text": request.system_prompt,  # [1] 정적 가이드 (ROLE/CONSTRAINTS/OUTPUT_FORMAT)
                "cache_control": {"type": "ephemeral"},
            },
        ]
        # [2] 세미정적 스펙 컨텍스트가 존재하면 별도 캐시 블록으로 추가
        if request.static_spec_context:
            system_blocks.append({
                "type": "text",
                "text": request.static_spec_context,
                "cache_control": {"type": "ephemeral"},
            })

        result = client.messages.create(
            model=self.model,
            system=system_blocks,  # 문자열 → 블록 배열 (캐시 마커 포함)
            max_tokens=request.max_tokens,
            temperature=request.temperature,  # 반드시 0
            messages=[{"role": "user", "content": request.user_prompt}],  # [3] 동적 내용은 최후방
        )
        text = "".join(
            block.text for block in result.content if getattr(block, "type", None) == "text"
        )
        usage: dict[str, int] = {}
        if hasattr(result, "usage") and result.usage:
            usage = {
                "input_tokens": int(getattr(result.usage, "input_tokens", 0) or 0),
                "output_tokens": int(getattr(result.usage, "output_tokens", 0) or 0),
                "cache_creation_input_tokens": int(getattr(result.usage, "cache_creation_input_tokens", 0) or 0),
                "cache_read_input_tokens": int(getattr(result.usage, "cache_read_input_tokens", 0) or 0),
            }
        return LLMResponse(
            text=text,
            model=self.model,
            finish_reason=getattr(result, "stop_reason", "stop") or "stop",
            usage=usage,
        )
# END GENERATED
