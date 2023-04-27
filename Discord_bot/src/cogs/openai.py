from discord.ext import commands

import discord
from AI.openai_api import chatgpt_response
from discord import app_commands
from utils.logger_conf import DiscordBotLogger
from utils.utils import COMMAND_DESCRIPTIONS, DEFAULT_DM_MESSAGE

logger = DiscordBotLogger().get_logger()


class OpenAI(commands.Cog):
    def __init__(self, bot, chatgpt_convo):
        self.bot = bot
        self.chatgpt_convo = chatgpt_convo

    def log_command_execution(self, interaction: discord.Interaction):
        logger.command(f"Command '{interaction.data['name']}' executed by {str(interaction.user)}")

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"{__name__}: Initializing...")
        await self.bot.tree.sync()
        self.bot.loaded_cogs_count += 1
        logger.info(f"{__name__}: Initialized")

    @app_commands.command(name="chatgpt", description=COMMAND_DESCRIPTIONS["chatgpt"])
    async def chatgpt(self, interaction: discord.Interaction, message: str = None):
        """
        A function that sends a chatGPT response to the user's input message.

        Args:
            interaction (discord.Interaction): The interaction object representing the user command.
            message (str, optional): The message provided by the user. Defaults to None.
        """
        if message is None:
            # If no message is provided by the user
            self.log_command_execution(interaction)
            logger.warning("No message provided!")
            await interaction.response.send_message("Please provide a message to discuss with ChatGPT.", ephemeral=True)
        else:
            # If a message is provided by the user
            self.log_command_execution(interaction)
            logger.command(f"{str(interaction.user)} >> {self.bot.user}: {message}")
            bot_response = await chatgpt_response(prompt=message)
            await interaction.response.send_message(f"{interaction.user.mention}: {bot_response}")
            logger.command(f"{self.bot.user} >> {str(interaction.user)}: {bot_response}")

    @app_commands.command(name="dm", description=COMMAND_DESCRIPTIONS["dm"])
    async def dm(self, interaction: discord.Interaction, message: str = None):
        self.log_command_execution(interaction)

        if message is None:
            message = "This is the default message when the user doesn't provide one."

        bot_response = DEFAULT_DM_MESSAGE
        await self.chatgpt_convo.handle_dm(interaction, message, bot_response, self.bot.user, str(interaction.user))


async def setup(bot, chatgpt):
    await bot.add_cog(OpenAI(bot, chatgpt))
