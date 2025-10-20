from enum import Enum
from unittest.mock import MagicMock, patch

import pytest

from services import llm_adapter
from services.llm_adapter import (
    _ADAPTERS,
    LLM,
    GeminiAdapter,
    LLMOutputSize,
    get_adapter,
)

# ==================================== Tests for `get_adapter` ====================================


# UNIT: Singleton behavior
@patch.object(llm_adapter, "GeminiAdapter")
def test_get_adapter_creates_once_per_key(mock_adapter_class):
    # ---------------- ARRANGE ----------------
    mock_inst = MagicMock(spec=llm_adapter.LLMAdapter)
    mock_adapter_class.return_value = mock_inst
    _ADAPTERS.clear()

    # ----------------- ACT ------------------
    a1 = get_adapter(LLM.GEMINI_2_0_FLASH, LLMOutputSize.M)
    a2 = get_adapter(LLM.GEMINI_2_0_FLASH, LLMOutputSize.M)

    # ---------------- ASSERT ----------------
    assert a1 is a2
    mock_adapter_class.assert_called_once_with(LLMOutputSize.M, LLM.GEMINI_2_0_FLASH)


# UNIT: Unsupported model
def test_get_adapter_unsupported_model():
    _ADAPTERS.clear()

    class FakeModel(Enum):
        OTHER = "other"

    with pytest.raises(ValueError):
        get_adapter(FakeModel.OTHER, LLMOutputSize.S)


# ==================================== Tests for GEMINI Adapter ====================================


# UNIT: GeminiAdapter.invoke
@patch("services.llm_adapter.ChatGoogleGenerativeAI")
def test_gemini_adapter_invoke(mock_llm_class):
    # ---------------- ARRANGE ----------------
    fake_txt = "user message"
    fake_prompt = MagicMock()
    fake_messages = ["formatted message"]
    expected_response = "fake response"
    fake_prompt.format_messages.return_value = fake_messages

    # Mock LLM response
    fake_llm_instance = mock_llm_class.return_value
    fake_llm_result = MagicMock()
    fake_llm_result.content = expected_response
    fake_llm_instance.invoke.return_value = fake_llm_result

    adapter = GeminiAdapter(max_tokens=123)

    # ----------------- ACT ------------------
    actual_response = adapter.invoke(fake_txt, fake_prompt)

    # ---------------- ASSERT ----------------
    fake_prompt.format_messages.assert_called_once_with(
        txt=fake_txt
    )  # prompt was used to format messages
    fake_llm_instance.invoke.assert_called_once_with(
        fake_messages
    )  # LLM was invoked with the formatted messages
    assert actual_response == expected_response
