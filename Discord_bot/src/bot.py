import asyncio
import importlib.util
import os
import signal
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

from AI.openai_api import chatgpt_response
from AI.openai_functions import OpenAIFunctions
from logger_conf import DiscordBotLogger
from helperfunctions import discordloghandler, read_config, split_message

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
discord_config = read_config("discord")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

bot_logger = DiscordBotLogger(
    enqueue=True,
    _log_path_channel=discord_config["log_path_channel"],
    _log_path_command=discord_config["log_path_command"],
)
logger = bot_logger.get_logger()
dedicated_channel_id: int = discord_config["dedicated_channel_id"]
if dedicated_channel_id == 0:
    logger.critical("No dedicated channel in config.json!")
    exit()
discordloghandler()

chatgpt = OpenAIFunctions(bot)


async def load_cog(cog_bot, cog_name):
    # Import the cog module dynamically
    cog_module_name = f"cogs.{cog_name}"
    spec = importlib.util.find_spec(cog_module_name)
    if spec is None:
        logger.error(f"cogs.{cog_name} not found")
        return

    cog_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cog_module)

    # Call the setup function if it exists
    if hasattr(cog_module, "setup"):
        logger.info(f"Loading: cogs.{cog_name}")
        if cog_name == "openai":
            await cog_module.setup(cog_bot, chatgpt)
        else:
            await cog_module.setup(bot)
        logger.info(f"cogs.{cog_name}: loaded")
    else:
        logger.error(f"cogs.{cog_name} does not have a setup function")


async def load(cog_bot):
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            cog_name = filename[:-3]
            await load_cog(cog_bot, cog_name)


async def setup_signal_handlers(shutdown_event):
    if sys.platform == "win32":

        async def shutdown_check():
            while not shutdown_event.is_set():
                await asyncio.sleep(1)

        loop = asyncio.get_running_loop()
        loop.create_task(shutdown_check())
    else:
        loop = asyncio.get_running_loop()

        def signal_handler():
            shutdown_event.set()

        loop.add_signal_handler(signal.SIGINT, signal_handler)
        loop.add_signal_handler(signal.SIGTERM, signal_handler)


async def main():
    bot.loaded_cogs_count = 0
    shutdown_event = asyncio.Event()

    await setup_signal_handlers(shutdown_event)

    async with bot:
        await load(bot)
        bot.loop.create_task(check_all_cogs_loaded(bot))
        try:
            await bot.start(discord_token)
        except KeyboardInterrupt:
            pass
        finally:
            logger.info("CTRL+C executed. Shutting down gracefully...")
            await send_shutdown_message()
            await bot.close()
            logger.info("Shutdown complete")

    await shutdown_event.wait()


async def send_shutdown_message():
    channel = bot.get_channel(dedicated_channel_id)
    if channel:
        await channel.send("I have been forced to quit my services for now.. See you another time!")
    else:
        logger.error("Couldn't find the specified channel.")


async def check_all_cogs_loaded(cog_bot):
    while cog_bot.loaded_cogs_count < len(cog_bot.cogs):
        await asyncio.sleep(1)
    logger.info("All cogs have been loaded successfully")
    channel = bot.get_channel(dedicated_channel_id)
    if channel:
        await channel.send("Hello everyone! Im here to save your day!")


@bot.event
async def on_ready():
    await bot.tree.sync()
    guilds = bot.guilds
    guild_names = [guild.name for guild in guilds]
    logger.info(f"Successfully logged in as: {bot.user}")
    logger.info(f"Bot is running on {len(guilds)} servers: '{', '.join(guild_names)}'")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_message = message.content

    if message.channel.id == dedicated_channel_id or isinstance(message.channel, discord.DMChannel):
        async with message.channel.typing():
            if message.channel.id == dedicated_channel_id:
                logger.channel(f"{message.author} >> {bot.user}: {user_message}")
                bot_response = await chatgpt_response(prompt=user_message)
                if len(bot_response) > 2000:
                    for message_part in split_message(f"{message.author.mention}: {bot_response}"):
                        await message.channel.send(message_part)
                        logger.channel(f"{bot.user} >> {message.author}: {message_part}")
                else:
                    await message.channel.send(bot_response)
                    logger.channel(f"{bot.user} >> {message.author}: {bot_response}")
            elif isinstance(message.channel, discord.DMChannel):
                user_id = str(message.author)
                bot_response = await chatgpt_response(prompt=user_message)
                await chatgpt.handle_dm(message, user_message, bot_response, bot.user, user_id)
    else:
        pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
