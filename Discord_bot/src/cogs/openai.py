import traceback

import discord
from discord import app_commands
from discord.ext import commands

from AI.openai_api import chatgpt_response, image_generator
from logger_conf import DiscordBotLogger
from helperfunctions import COMMAND_DESCRIPTIONS, DEFAULT_DM_MESSAGE, read_config

logger = DiscordBotLogger().get_logger()
config = read_config("discord")


class OpenAI(commands.Cog):

    def __init__(self, bot, ai):
        self.bot = bot
        self.ai = ai

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"{__name__}: Initializing...")
        await self.bot.tree.sync()
        self.bot.loaded_cogs_count += 1
        logger.info(f"{__name__}: Initialized")

    @app_commands.command(name="chatgpt",
                          description=COMMAND_DESCRIPTIONS["chatgpt"])
    async def chatgpt(self,
                      interaction: discord.Interaction,
                      message: str = None):
        """
        A function that sends a chatGPT response to the user's input message.

        Args:
            interaction (discord.Interaction): The interaction object representing the user command.
            message (str, optional): The message provided by the user. Defaults to None.
        """
        try:
            logger.command(
                f"Command '{interaction.data['name']}' executed by {str(interaction.user)}"
            )
            if message is None:
                logger.warning("No message provided!")
                await interaction.response.send_message(
                    "Please provide a message to discuss with ChatGPT.",
                    ephemeral=True)
            else:
                logger.command(
                    f"{str(interaction.user)} >> {self.bot.user}: {message}")
                if interaction.channel.id == config["dedicated_channel_id"]:
                    await interaction.response.defer()
                    bot_response = await chatgpt_response(prompt=message)
                    await interaction.followup.send(
                        f"{interaction.user.mention}: {bot_response}")
                    logger.command(
                        f"{self.bot.user} >> {str(interaction.user)}: {bot_response}"
                    )
                else:
                    await interaction.response.defer(ephemeral=True)
                    bot_response = await chatgpt_response(prompt=message)
                    await interaction.followup.send(
                        f"{interaction.user.mention}: {bot_response}",
                        ephemeral=True)
                    logger.command(
                        f"{self.bot.user} >> {str(interaction.user)}: {bot_response}"
                    )

        except Exception as error:
            logger.error(f"Error in chatgpt command: {str(error)}")
            logger.error(traceback.format_exc())

    @app_commands.command(name="dm", description=COMMAND_DESCRIPTIONS["dm"])
    async def dm(self, interaction: discord.Interaction, message: str = None):
        logger.command(
            f"Command '{interaction.data['name']}' executed by {str(interaction.user)}"
        )
        logger.command(f"Arguments used - Message: '{message}'")

        if message is None:
            message = "This is the default message when the user doesn't provide one."
            logger.warning("No message supplied!")

        bot_response = DEFAULT_DM_MESSAGE
        await self.ai.handle_dm(interaction, message, bot_response,
                                self.bot.user, str(interaction.user))
        await interaction.response.send_message("I have sent you a DM",
                                                ephemeral=True)

    @app_commands.command(name="image",
                          description=COMMAND_DESCRIPTIONS["image"])
    async def image(
        self,
        interaction: discord.Interaction,
        message: str = None,
        size: str = None,
        num_of_pictures: int = None,
    ):
        logger.command(
            f"Command '{interaction.data['name']}' executed by {str(interaction.user)}"
        )
        logger.command(
            f"Arguments used - Message: '{message}', Size: '{size}' and num_of_pics: '{num_of_pictures}'"
        )

        if message is None:
            await interaction.response.send_message(
                "You have to provide what you want the AI to generate.",
                ephemeral=True)
            logger.warning("No message supplied!")
            return

        if size is None:
            size = "256x256"
        if num_of_pictures is None:
            num_of_pictures = 1

        if interaction.channel.id == config["dedicated_channel_id"]:
            await interaction.response.defer()
        else:
            await interaction.response.defer(ephemeral=True)

        response = await image_generator(message, size, num_of_pictures, logger)
        if not isinstance(response, list):
            await interaction.followup.send(response, ephemeral=True)
        else:
            for image_url in response:
                logger.info(image_url)
                embed = discord.Embed()
                embed.set_image(url=image_url)
                if interaction.channel.id == config["dedicated_channel_id"]:
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot, ai):
    await bot.add_cog(OpenAI(bot, ai))
