from enum import Enum
import os
import pytest
from unittest.mock import patch, MagicMock

from services import summary
from services.summary import (
    get_summary_size,
    SumSize,
    SumModel,
    get_adapter,
    summarize,
    LLMAdapter,
    GeminiAdapter,
    _ADAPTERS,
)
from langchain.prompts import ChatPromptTemplate

from tests.data import TEST_SUMMARY_1, TEST_TRANSCRIPT_1


# =================================== Tests for `summary size` ===================================
@pytest.mark.parametrize(
    "txt, expected",
    [
        ("", SumSize.S),
        ("a" * 100, SumSize.S),
        ("b" * 500, SumSize.M),
        ("c" * 1500, SumSize.M),
        ("d" * 2000, SumSize.L),
        ("e" * 5000, SumSize.L),
    ],
)
def test_get_summary_size(txt, expected):
    assert get_summary_size(txt) == expected


# ==================================== Tests for `get_adapter` ====================================


# UNIT: Singleton behavior
@patch.object(summary, "GeminiAdapter")
def test_get_adapter_creates_once_per_key(mock_adapter_class):
    # ---------------- ARRANGE ----------------
    mock_inst = MagicMock(spec=LLMAdapter)
    mock_adapter_class.return_value = mock_inst
    _ADAPTERS.clear()

    # ----------------- ACT ------------------
    a1 = get_adapter(SumModel.GEMINI, SumSize.M)
    a2 = get_adapter(SumModel.GEMINI, SumSize.M)

    # ---------------- ASSERT ----------------
    assert a1 is a2
    mock_adapter_class.assert_called_once_with(SumSize.M)


# UNIT: Unsupported model
def test_get_adapter_unsupported_model():
    _ADAPTERS.clear()

    class FakeModel(Enum):
        OTHER = "other"

    with pytest.raises(ValueError):
        get_adapter(FakeModel.OTHER, SumSize.S)


# ==================================== Tests for GEMINI Adapter ====================================


# UNIT: GeminiAdapter summarize method
@patch("services.summary.ChatGoogleGenerativeAI")
@patch.object(ChatPromptTemplate, "format_messages", autospec=True)
def test_gemini_adapter_summarize(mock_format, mock_llm_class):
    # ---------------- ARRANGE ----------------
    fake_msg = ["msg"]
    expected_summary = TEST_SUMMARY_1.summary_text
    mock_format.return_value = fake_msg
    fake_response = MagicMock()
    fake_response.content = expected_summary
    inst_llm = mock_llm_class.return_value
    inst_llm.invoke.return_value = fake_response
    adapter = GeminiAdapter(123)

    # ----------------- ACT ------------------
    actual_summary = adapter.summarize(TEST_TRANSCRIPT_1.transcript_text)

    # ---------------- ASSERT ----------------
    mock_format.assert_called_once()  # ensure prompt formatting
    inst_llm.invoke.assert_called_once_with(fake_msg)
    assert actual_summary == expected_summary


# ==================================== Tests for `summarize` =====================================


# UNIT: summarize
@patch("services.summary.get_summary_size")
@patch("services.summary.get_adapter")
def test_summarize_delegates(mock_get_adapter, mock_get_size):
    # ---------------- ARRANGE ----------------
    transcript_txt = TEST_TRANSCRIPT_1.transcript_text
    expected_summary = TEST_SUMMARY_1.summary_text
    mock_get_size.return_value = SumSize.L
    fake_adapter = MagicMock(spec=LLMAdapter)
    fake_adapter.summarize.return_value = expected_summary
    mock_get_adapter.return_value = fake_adapter

    # ----------------- ACT ------------------
    actual_summary = summarize(transcript_txt)

    # ---------------- ASSERT ----------------
    mock_get_size.assert_called_once_with(transcript_txt)
    mock_get_adapter.assert_called_once_with(SumModel.GEMINI, SumSize.L)
    fake_adapter.summarize.assert_called_once_with(transcript_txt)
    assert actual_summary == expected_summary
