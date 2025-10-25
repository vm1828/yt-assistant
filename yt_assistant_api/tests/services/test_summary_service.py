from unittest.mock import MagicMock, patch

import pytest

from services.llm_adapter import LLM, LLMAdapter, LLMOutputSize
from services.summary import get_summary_size, summarize
from tests.data import TEST_SUMMARY_1, TEST_TRANSCRIPT_1


# =================================== Tests for `summary size` ===================================
@pytest.mark.parametrize(
    "txt, expected",
    [
        ("", LLMOutputSize.S),
        ("a" * 100, LLMOutputSize.S),
        ("b" * 500, LLMOutputSize.S),
        ("c" * 1500, LLMOutputSize.M),
        ("d" * 2000, LLMOutputSize.M),
        ("e" * 5000, LLMOutputSize.L),
    ],
)
def test_get_summary_size(txt, expected):
    assert get_summary_size(txt) == expected


# ==================================== Tests for `summarize` =====================================


# UNIT: summarize
@pytest.mark.asyncio
@patch("services.summary.summarization_prompt", new_callable=MagicMock)
@patch("services.summary.get_summary_size")
@patch("services.summary.get_adapter")
async def test_summarize(mock_get_adapter, mock_get_size, mock_prompt):
    # ---------------- ARRANGE ----------------
    transcript_txt = TEST_TRANSCRIPT_1.transcript_text
    expected_summary = TEST_SUMMARY_1.summary_text

    mock_get_size.return_value = LLMOutputSize.L
    fake_adapter = MagicMock(spec=LLMAdapter)
    fake_adapter.invoke.return_value = expected_summary
    mock_get_adapter.return_value = fake_adapter

    # ----------------- ACT ------------------
    actual_summary = await summarize(transcript_txt)

    # ---------------- ASSERT ----------------
    mock_get_size.assert_called_once_with(transcript_txt)
    mock_get_adapter.assert_called_once_with(LLM.GEMINI_2_0_FLASH, LLMOutputSize.L)
    fake_adapter.invoke.assert_called_once_with(transcript_txt, mock_prompt)
    assert actual_summary == expected_summary
