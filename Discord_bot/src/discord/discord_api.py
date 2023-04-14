import asyncio
import os

from dotenv import load_dotenv

import discord
from chatgpt.openai_api import chatgpt_response
from utils.logger_conf import DiscordBotLogger
from utils.utils import (
    ABOUT_STR,
    DEFAULT_DM_MESSAGE,
    DEFAULT_THREAD_MESSAGE,
    DISCLAIMER,
    HELP_STR,
    discordloghandler,
    remove_log_folder,
)

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")


class Bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        remove_log_folder()
        self.dedicated_channel_id = 1095796880706908160
        self.dedicated_thread_channel_id = 1096123841870303292
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

    async def delete_thread_after_delay(self, thread, delay):
        await asyncio.sleep(delay)
        if not thread.archived:
            await thread.edit(archived=True, reason="Thread auto-closed after 24 hours.")
        await thread.delete()

    async def on_ready(self):
        self.logger.info(f"Successfully logged in as: {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        user_message = message.content
        bot_response = chatgpt_response(prompt=user_message)
        if isinstance(message.channel, (discord.DMChannel, discord.Thread)):
            if isinstance(message.channel, discord.DMChannel):
                user_id = str(message.author)
                if user_id not in self.dm_loggers:
                    dm_logger = self.bot_logger.get_dm_logger_for_user(user_id)
                    self.dm_loggers[user_id] = dm_logger
                self.dm_loggers[user_id].user_id(f"Hello {message.author.name}, {DEFAULT_DM_MESSAGE}")

            if isinstance(message.channel, discord.Thread):
                if user_message == "!dm":
                    self.logger.command(f"Command: {user_message}, User: {message.author}")
                    self.logger.info(f"Starting private conversation with {message.author}")
                    dm_channel = await message.author.create_dm()
                    await dm_channel.send(f"Hello {message.author.name}, {DEFAULT_DM_MESSAGE}")
                    self.logger.info(f"{message.author} requesed DMs")
                    await message.channel.edit(archived=True, reason="Thread closed by bot.")
                    self.logger.info(f"Thread {message.channel.name} closed by {self.user}")
                elif user_message == "!close_thread":
                    if message.channel.permissions_for(message.guild.me).manage_threads:
                        await message.channel.edit(archived=True, reason="Thread closed by bot.")
                        self.logger.info(f"Thread {message.channel.name} closed by {message.author}")
                        await asyncio.sleep(5)
                        await message.channel.delete()
                        self.logger.info(f"Thread {message.channel.name} deleted by {message.author}")
                    else:
                        await message.channel.send("I do not have permission to manage threads.")
                else:
                    await message.channel.send(f"{message.author.mention}: {bot_response}")
                    self.logger.channel(f"{self.user} >> {message.author}: {bot_response}")

            if isinstance(message.channel, discord.Thread):
                self.logger.channel(f"{message.author} >> {self.user}: {user_message}")
            else:
                self.logger.channel(f"{message.author} >> {self.user}: {user_message}")
        elif message.channel.id == self.dedicated_channel_id:
            await message.channel.send(f"{message.author.mention}: {bot_response}")
            self.logger.channel(f"{self.user} >> {message.author}: {bot_response}")
        else:
            text_commands = {"!chatgpt", "!dm", "!help", "!about"}
            for text in text_commands:
                if user_message.startswith(text):
                    command_parts = user_message.split(" ", 1)
                    if len(command_parts) > 1:
                        command, user_message = command_parts
                        command = command.strip()
                        user_message = user_message.strip()
                    else:
                        command = user_message
            print(command)
            if command == "!chatgpt":
                if message.channel.permissions_for(message.guild.me).manage_threads:
                    dedicated_thread_channel_id = self.get_channel(self.dedicated_thread_channel_id)
                    thread_name = f"chatgpt-{message.author.name}"
                    thread = await dedicated_thread_channel_id.create_thread(
                        name=thread_name,
                        type=discord.ChannelType.public_thread,
                        auto_archive_duration=1440,
                    )
                    self.logger.command(f"Command: {command}, User: {message.author}")
                    self.logger.info(f"Starting threaded conversation with {message.author}")
                    asyncio.create_task(self.delete_thread_after_delay(thread, 24 * 60 * 60))
                    if user_message == command:
                        await thread.send(DISCLAIMER)
                        await thread.send(f"{message.author.mention}: {DEFAULT_THREAD_MESSAGE}")
                    else:
                        bot_response = chatgpt_response(prompt=user_message)
                        await thread.send(
                            "DISCLAIMER: I do not have a memory yet. I wont be able to remember our conversation."
                        )
                        await thread.send(f"{message.author.mention}: {bot_response}")
                        self.logger.channel(f"{self.user} >> {message.author}: {bot_response}")
                else:
                    await message.channel.send("I do not have permission to manage threads.")

            elif command == "!dm":
                self.logger.command(f"Command: {command}, User: {message.author}")
                self.logger.info(f"Starting private conversation with {message.author}")
                dm_channel = await message.author.create_dm()
                await dm_channel.send(f"Hello {message.author.name}, {DEFAULT_DM_MESSAGE}")
            elif command in ("!help", "!about"):
                dm_channel = await message.author.create_dm()
                self.logger.command(f"Command: {command}, User: {message.author}")
                if command == "!help":
                    await dm_channel.send(HELP_STR)
                else:
                    await dm_channel.send(ABOUT_STR)
            else:
                pass


intents = discord.Intents.default()
intents.message_content = True

bot = Bot(intents=intents)
