from unittest.mock import MagicMock, patch

import pytest

from chatgpt.openai_api import chatgpt_response


@pytest.mark.asyncio
async def test_chatgpt_response():
    prompt = "What is the capital of France?"

    # Mock the OpenAI API response
    mock_response = MagicMock()
    mock_response.choices = [{"message": {"content": "The capital of France is Paris."}}]

    with patch("openai.ChatCompletion.create", return_value=mock_response):
        response = await chatgpt_response(prompt)

    assert response == "The capital of France is Paris."


@pytest.mark.asyncio
async def test_chatgpt_response_empty():
    prompt = "What is the capital of France?"

    # Mock an empty OpenAI API response
    mock_response = MagicMock()
    mock_response.choices = []

    with patch("openai.ChatCompletion.create", return_value=mock_response):
        response = await chatgpt_response(prompt)

    assert response == ""
