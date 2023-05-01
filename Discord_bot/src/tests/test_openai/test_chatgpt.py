# import pytest
# from unittest.mock import MagicMock, AsyncMock
# from discord import Interaction
# from cogs.openai import OpenAI


# def async_test(coroutine):
#     import asyncio

#     loop = asyncio.get_event_loop()
#     return loop.run_until_complete(coroutine)


# @pytest.fixture
# def bot():
#     return MagicMock()


# def test_chatgpt_no_message_provided(bot):
#     chatgpt_convo = MagicMock()
#     openai_cog = OpenAI(bot, chatgpt_convo)
#     interaction = MagicMock(spec=Interaction)
#     interaction.data = {"name": "chatgpt"}
#     interaction.user = MagicMock()
#     interaction.response.send_message = AsyncMock()

#     async_test(openai_cog.chatgpt(interaction))

#     interaction.response.send_message.assert_called_once_with(
#         "Please provide a message to discuss with ChatGPT.", ephemeral=True
#     )


# def test_chatgpt_with_message_provided(bot):
#     chatgpt_convo = MagicMock()
#     openai_cog = OpenAI(bot, chatgpt_convo)
#     interaction = MagicMock(spec=Interaction)
#     interaction.data = {"name": "chatgpt"}
#     interaction.user = MagicMock()
#     interaction.response.send_message = AsyncMock()

#     chatgpt_response_mock = AsyncMock()
#     chatgpt_response_mock.return_value = "Sample response from ChatGPT"
#     openai_cog.chatgpt_response = chatgpt_response_mock

#     message = "Hello, ChatGPT!"

#     async_test(openai_cog.chatgpt(interaction, message))

#     chatgpt_response_mock.assert_called_once_with(prompt=message)
#     interaction.response.send_message.assert_called_once_with(
#         f"{interaction.user.mention}: Sample response from ChatGPT"
#     )
