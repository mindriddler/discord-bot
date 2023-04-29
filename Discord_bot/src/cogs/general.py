import discord
from discord import app_commands
from discord.ext import commands

from utils.logger_conf import DiscordBotLogger
from utils.utils import ABOUT_STR, COMMAND_DESCRIPTIONS, HELP_STR

logger = DiscordBotLogger().get_logger()


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"{__name__}: Initializing...")
        await self.bot.tree.sync()
        self.bot.loaded_cogs_count += 1
        logger.info(f"{__name__}: Initialized")

    @app_commands.command(name="help", description=COMMAND_DESCRIPTIONS["help"])
    async def help(self, interaction: discord.Interaction):
        """
        Sends a help message to the user.

        Args:
            interaction (discord.Interaction): The interaction object representing the user command.
        """
        logger.command(f"Command '{interaction.data['name']}' executed by {str(interaction.user)}")
        await interaction.response.send_message(HELP_STR, ephemeral=True)

    @app_commands.command(name="about", description=COMMAND_DESCRIPTIONS["about"])
    async def about(self, interaction: discord.Interaction):
        """
        Sends an about message to the user.

        Args:
            interaction (discord.Interaction): The interaction object representing the user command.
        """
        logger.command(f"Command '{interaction.data['name']}' executed by {str(interaction.user)}")
        await interaction.response.send_message(ABOUT_STR, ephemeral=True)


async def setup(bot):
    await bot.add_cog(General(bot))
