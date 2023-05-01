import discord

from AI.openai_api import chatgpt_response
from logger_conf import DiscordBotLogger
from helperfunctions import DEFAULT_DM_MESSAGE, split_message

logger = DiscordBotLogger()


class OpenAIFunctions:
    def __init__(self, bot):
        self.bot = bot
        self.dm_loggers = {}

    async def handle_dm(self, message, user_message, bot_response, bot_user, user_id):
        if user_id not in self.dm_loggers:
            dm_logger = logger.get_dm_logger_for_user(user_id)
            self.dm_loggers[user_id] = dm_logger
            self.dm_loggers[user_id].user_id(f"{bot_user} >> {user_id}: Hello {user_id}, {DEFAULT_DM_MESSAGE}")
            if isinstance(message, discord.Interaction):
                await message.user.send(f"Hello {user_id}, {bot_response}")
            else:
                await message.channel.send(f"Hello {user_id}, {bot_response}")
            self.dm_loggers[user_id].user_id(f"{user_id} >> {bot_user}: {user_message}")
        else:
            if isinstance(message, discord.Interaction):
                self.dm_loggers[user_id].user_id(f"{bot_user} >> {user_id}: {bot_response}")
                bot_response = await chatgpt_response(prompt=user_message)
                for chunk in split_message(bot_response):
                    await message.user.send(chunk)
            else:
                self.dm_loggers[user_id].user_id(f"{bot_user} >> {user_id}: {bot_response}")
                bot_response = await chatgpt_response(prompt=user_message)
                for chunk in split_message(bot_response):
                    await message.channel.send(chunk)
