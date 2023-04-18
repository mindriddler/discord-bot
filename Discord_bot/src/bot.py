import asyncio
import os

from discord.ext import commands
from dotenv import load_dotenv

import discord
from chatgpt.chatgpt_functions import ChatGPTFunctions
from chatgpt.openai_api import chatgpt_response
from utils.logger_conf import DiscordBotLogger
from utils.utils import discordloghandler, read_config, split_message

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
discord_config = read_config("discord")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

dedicated_channel_id: int = discord_config["dedicated_channel_id"]
dedicated_thread_channel_id: int = discord_config["dedicated_thread_channel_id"]
thread_auto_close_delay: int = discord_config["thread_auto_close_delay"]
bot_logger = DiscordBotLogger(
    enqueue=True,
    _log_path_channel=discord_config["log_path_channel"],
    _log_path_command=discord_config["log_path_command"],
)
logger = bot_logger.get_logger()
discordloghandler()

chatgpt = ChatGPTFunctions(bot)


async def load():
    from cogs.appcommands import setup

    for filename in os.listdir("./src/cogs"):
        if filename.endswith(".py"):
            cog_name = filename[:-3]
            if cog_name == "appcommands":
                await setup(bot, chatgpt)
                logger.info(f"Loading cog: {cog_name}")


async def main():
    async with bot:
        await load()
        await bot.start(discord_token)


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
    asyncio.run(main())
