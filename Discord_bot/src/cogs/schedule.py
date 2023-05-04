from datetime import datetime, timedelta

import discord
import pytz
import requests
from discord import app_commands
from discord.ext import commands
from icalendar import Calendar

from logger_conf import DiscordBotLogger
from helperfunctions import COMMAND_DESCRIPTIONS, read_config

logger = DiscordBotLogger().get_logger()

schedule_config = read_config("schedule")
config = read_config("discord")


class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"{__name__}: Initializing...")
        await self.bot.tree.sync()
        self.bot.loaded_cogs_count += 1
        logger.info(f"{__name__}: Initialized")

    @app_commands.command(name="schedule", description=COMMAND_DESCRIPTIONS["schedule"])
    async def schedule(self, interaction: discord.Interaction, num_of_days: int = None):
        logger.command(
            f"Command '{interaction.data['name']}' executed by {str(interaction.user)} with number: {num_of_days}"
        )
        if num_of_days is None:
            num_of_days = 7
            logger.warning("No number of days supplied!")
            logger.debug("Defaulting to 7 number of days")
        elif num_of_days > 20:
            logger.warning("To high number!")
            message = "Max 20 days!"
            await interaction.response.send_message(message, ephemeral=True)

        url = schedule_config["url"]
        if url == "":
            message = "No url supplied in src/config.json!"
            logger.error(message)
            await interaction.response.send_message(message, ephemeral=True)
        else:
            if interaction.channel.id == config["dedicated_channel_id"]:
                await interaction.response.defer()
            else:
                await interaction.response.defer(ephemeral=True)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            ical_data = response.text
            calendar = Calendar.from_ical(ical_data)

            timezone = pytz.timezone("Europe/Stockholm")

            now = datetime.now(tz=timezone)
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
                start_time = event.get("dtstart").dt.astimezone(timezone).strftime("%m/%d/%Y")
                start_time_formatted = event.get("dtstart").dt.astimezone(timezone).strftime("%H:%M")
                end_time_formatted = event.get("dtend").dt.astimezone(timezone).strftime("%H:%M")
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

            message = f"**Schedule for the next {num_of_days} days (excluding weekends):**\n"
            for start_time, events in event_dict.items():
                message += f"\n• **Date:** {start_time}\n"
                for event in events:
                    message += f"     **Time:** {event['start_time_formatted']} - {event['end_time_formatted']}\n"
                    message += f"         Teacher: {event['teacher']}\n"
                    message += f"         Course: {event['course']}\n"
                    message += f"         Classroom: {event['location']}\n"

            if interaction.channel.id == config["dedicated_channel_id"]:
                await interaction.followup.send(message)
            else:
                await interaction.followup.send(message, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Schedule(bot))
