import logging
import logging.handlers
import os
import shutil

# CONSTANTS

HELP_STR = """
Help section for ChatGPT Discord Bot\n
!chatgpt - Start a conversation with ChatGPT
!dm - Start a private conversation with ChatGPT
!about - Brief description
!help - This help message
"""

ABOUT_STR = """
For now the bot till NOT remember past conversations.
It is something i am working on getting done.
"""

LOG_FOLDER = "logs"

DEFAULT_THREAD_MESSAGE = """
Hey! I have created this thread for us to have a public conversation.
If you want to have a private conversation with me use the command '!dm',
otherwise state your question and i will gladly help you!
"""

DEFAULT_DM_MESSAGE = (
    """this is a DM from ChatGPT. You can now have a conversation with me here and it will be our little secret."""
)


DISCLAIMER = """
DISCLAIMER:
I do not have a memory yet. I wont be able to remember our conversation.
Threads will be automatically closed after 24 hours.
"""


def remove_log_folder():
    if os.path.exists(LOG_FOLDER):
        shutil.rmtree(LOG_FOLDER)
    os.mkdir("logs")
    with open("logs/.gitkeep", "w") as f:
        f.close()


def discordloghandler():
    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)
    logging.getLogger("discord.http").setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename="logs/info.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
