import discord
from discord import app_commands
from discord.ext import commands

from logger_conf import DiscordBotLogger
from helperfunctions import COMMAND_DESCRIPTIONS, convert_svg_url_to_png, read_config

logger = DiscordBotLogger().get_logger()
github_config = read_config("github")


class Github(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"{__name__}: Initializing...")
        await self.bot.tree.sync()
        self.bot.loaded_cogs_count += 1
        logger.info(f"{__name__}: Initialized")

    @app_commands.command(name="github_stats", description=COMMAND_DESCRIPTIONS["github stats"])
    async def github_stats(self, interaction: discord.Interaction, username: str = None):
        logger.command(f"Command '{interaction.data['name']}' executed by {str(interaction.user)} for user: {username}")

        # defaults to creator
        # feel free to change
        if username is None:
            username = github_config["default_user"]
            logger.warning(f"No username supplied! Defaulting to {username}")

        await interaction.response.defer(ephemeral=True)

        urls = {
            "user_stats": github_config["user_stats"].format(username),
            "streak_stats": github_config["streak_stats"].format(username),
        }

        png_user, png_streak = await convert_svg_url_to_png(
            urls["user_stats"],
            urls["streak_stats"],
            suppress_warnings=True,
        )

        files = [
            discord.File(fp=png_user, filename="github_user_stats.png"),
            discord.File(fp=png_streak, filename="github_streak_stats.png"),
        ]

        embeds = [
            discord.Embed().set_image(url="attachment://github_user_stats.png"),
            discord.Embed().set_image(url="attachment://github_streak_stats.png"),
        ]

        for file, embed in zip(files, embeds):
            await interaction.followup.send(embed=embed, files=[file], ephemeral=True)


async def setup(bot):
    await bot.add_cog(Github(bot))
