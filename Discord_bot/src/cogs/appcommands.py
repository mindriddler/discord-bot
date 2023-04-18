from datetime import datetime, timedelta

import pytz
import requests
from discord.ext import commands
from icalendar import Calendar

import discord
from chatgpt.openai_api import chatgpt_response
from discord import app_commands
from utils.logger_conf import DiscordBotLogger
from utils.utils import ABOUT_STR, COMMAND_DESCRIPTIONS, DEFAULT_DM_MESSAGE, HELP_STR, read_config

logger = DiscordBotLogger().get_logger()

schedule_config = read_config("schedule")


class AppCommands(commands.Cog):
    """
    A class defining custom commands for the Discord bot.
    """

    def __init__(self, bot, chatgpt_convo):
        """
        Class constructor.

        Args:
            bot (commands.Bot): An instance of a Discord bot.
        """
        self.bot = bot
        self.chatgpt_convo = chatgpt_convo

    def log_command_execution(self, interaction: discord.Interaction):
        logger.command(f"Command '{interaction.data['name']}' executed by {str(interaction.user)}")

    @commands.Cog.listener()
    async def on_ready(self):
        """
        A function that runs when the bot is first started up.
        """
        logger.info(f"Please wait for {__name__} to load correctly, it can take up to 1 minute.")
        logger.info("You will get another log message when its loaded correctly.")
        await self.bot.tree.sync()
        logger.info(f"{__name__} loaded correctly!")

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

    @app_commands.command(name="help", description=COMMAND_DESCRIPTIONS["help"])
    async def help(self, interaction: discord.Interaction):
        """
        Sends a help message to the user.

        Args:
            interaction (discord.Interaction): The interaction object representing the user command.
        """
        self.log_command_execution(interaction)
        await interaction.response.send_message(HELP_STR, ephemeral=True)

    @app_commands.command(name="about", description=COMMAND_DESCRIPTIONS["about"])
    async def about(self, interaction: discord.Interaction):
        """
        Sends an about message to the user.

        Args:
            interaction (discord.Interaction): The interaction object representing the user command.
        """
        self.log_command_execution(interaction)
        await interaction.response.send_message(ABOUT_STR, ephemeral=True)

    @app_commands.command(name="dm", description=COMMAND_DESCRIPTIONS["dm"])
    async def dm(self, interaction: discord.Interaction, message: str):
        self.log_command_execution(interaction)

        if message is None:
            message = "This is the default message when the user doesn't provide one."

        bot_response = DEFAULT_DM_MESSAGE
        await self.chatgpt_convo.handle_dm(interaction, message, bot_response, self.bot.user, str(interaction.user))

    @app_commands.command(name="schedule", description="Shows schedule")
    async def schedule(self, interaction: discord.Interaction, num_of_days: int = None):
        self.log_command_execution(interaction)
        if num_of_days is None:
            num_of_days = 7
        elif num_of_days > 20:
            message = "Max 20 days!"
            await interaction.response.send_message(message, ephemeral=True)

        url = schedule_config["url"]
        response = requests.get(url)
        response.raise_for_status()
        ical_data = response.text
        calendar = Calendar.from_ical(ical_data)

        tz = pytz.timezone("Europe/Stockholm")

        now = datetime.now(tz=tz)
        end_date = now + timedelta(days=num_of_days)
        start_of_weekday_after_now = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(
            days=(7 - now.weekday()) % 7 + 1
        )
        start_of_weekday_after_end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(
            days=(7 - end_date.weekday()) % 7 + 1
        )

        events = (
            e
            for e in calendar.walk()
            if e.name == "VEVENT"
            and start_of_weekday_after_now <= e.get("dtstart").dt < start_of_weekday_after_end_date
            and e.get("dtstart").dt.weekday() < 5
        )

        event_dict = {}
        for event in events:
            start_time = event.get("dtstart").dt.astimezone(tz).strftime("%m/%d/%Y")
            start_time_formatted = event.get("dtstart").dt.astimezone(tz).strftime("%H:%M")
            end_time_formatted = event.get("dtend").dt.astimezone(tz).strftime("%H:%M")
            location = event.get("location")
            description = event.get("summary")

            if description and "," in description:
                xlass, teacher, course = description.split(",")[:3]
            else:
                teacher = ""
                course = ""

            if start_time not in event_dict:
                event_dict[start_time] = []

            event_dict[start_time].append(
                {
                    "start_time_formatted": start_time_formatted,
                    "end_time_formatted": end_time_formatted,
                    "teacher": teacher.strip(),
                    "course": course.strip(),
                    "location": location.strip(),
                }
            )

        message = "**Schedule for the next {} days (excluding weekends):**\n".format(num_of_days)
        for start_time, events in event_dict.items():
            message += "\n• **Date:** {}\n".format(start_time)
            for event in events:
                message += "     **Time:** {} - {}\n".format(event["start_time_formatted"], event["end_time_formatted"])
                message += "         Teacher: {}\n".format(event["teacher"])
                message += "         Course: {}\n".format(event["course"])
                message += "         Classroom: {}\n".format(event["location"])

        await interaction.response.send_message(message, ephemeral=True)


async def setup(bot, chatgpt):
    await bot.add_cog(AppCommands(bot, chatgpt))
