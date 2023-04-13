import os
import shutil

import discord
from dotenv import load_dotenv

from src.chatgpt_ai.openai import chatgpt_response
from src.discord_bot.discord_log_handler import discordloghandler
from src.discord_bot.logger_conf import DiscordBotLogger

load_dotenv()

# Just for testing purpose. Remove when code is "done"
# TODO
discord_token = os.getenv("DISCORD_TOKEN")
LOG_FOLDER = "logs"
if os.path.exists(LOG_FOLDER):
    shutil.rmtree(LOG_FOLDER)


class Bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dedicated_channel_id = 1095796880706908160
        self.channel_log_name = "channel_{time:YYYY-MM-DD-HH-mm-ss-SSS!UTC}.log"
        self.command_log_name = "command_{time:YYYY-MM-DD-HH-mm-ss-SSS!UTC}.log"
        self.bot_logger = DiscordBotLogger(
            enqueue=True,
            _log_path_channel=f"logs/{self.channel_log_name}",
            _log_path_command=f"logs/{self.command_log_name}",
        )
        #
        self.logger = self.bot_logger.get_logger()
        discordloghandler()
        self.dm_loggers = {}

    async def on_ready(self):
        self.logger.info(f"Successfully logged in as: {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if isinstance(message.channel, discord.DMChannel):
            user_id = str(message.author)
            if user_id not in self.dm_loggers:
                dm_logger = self.bot_logger.get_dm_logger_for_user(user_id)
                self.dm_loggers[user_id] = dm_logger
            self.dm_loggers[user_id].user_id(
                f"Hello {message.author.name}, this is a DM from ChatGPT. You can now have a conversation with me here and it will be our little secret."
            )
            user_message = message.content
            self.dm_loggers[user_id].user_id(
                f"{message.author} >> {self.user}: {user_message}"
            )
            bot_response = chatgpt_response(prompt=user_message)
            await message.channel.send(bot_response)
            self.dm_loggers[user_id].user_id(
                f"{self.user} >> {message.author}: {bot_response}"
            )

        elif message.channel.id == self.dedicated_channel_id:
            user_message = message.content
            self.logger.channel(f"{message.author} >> {self.user}: {user_message}")
            bot_response = chatgpt_response(prompt=user_message)
            await message.channel.send(f"{message.author.mention}: {bot_response}")
            self.logger.channel(f"{self.user} >> {message.author}: {bot_response}")

        else:
            command, user_message = None, None
            for text in ["/ai", "/bot", "/chatgpt", "/gpt", "/dm"]:
                if message.content.startswith(text):
                    command = message.content.split(" ")[0]
                    user_message = message.content.replace(text, "")

            if command in ["/ai", "/bot", "/chatgpt", "/gpt"]:
                self.logger.command(
                    f"{message.author}, Command: '{command}' >> {self.user}: {user_message}"
                )
                bot_response = chatgpt_response(prompt=user_message)
                await message.channel.send(f"{message.author.mention}: {bot_response}")
                self.logger.command(f"{self.user} >> {message.author}: {bot_response}")
            elif command == "/dm":
                self.logger.command(f"Command: {command}, User: {message.author}")
                self.logger.info(f"Starting private conversation with {message.author}")
                dm_channel = await message.author.create_dm()
                await dm_channel.send(
                    f"Hello {message.author.name}, this is a DM from ChatGPT. You can now have a conversation with me here and it will be our little secret."
                )


intents = discord.Intents.default()
intents.message_content = True

client = Bot(intents=intents)
