# import shutil
import json
import logging
import logging.handlers
import os

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

COMMAND_DESCRIPTIONS = {
    "avatar": "Send något",
    "chatgpt": "Ask ChatGPT a question of your choice and you will get a answer back.",
    "help": "Show a small help section with available commands.",
    "about": "Show a small about section for the bot.",
    "dm": "ChatGPT will start DMs with you.",
}


# def remove_log_folder():
#     if os.path.exists(LOG_FOLDER):
#         shutil.rmtree(LOG_FOLDER)
#     os.mkdir("logs")
#     with open("logs/.gitkeep", "w", encoding="utf-8") as file:
#         file.close()
def split_message(message, max_length=2000):
    if len(message) <= max_length:
        return [message]
    messages = []
    current_message = ""
    for word in message.split():
        if len(current_message) + len(word) + 1 <= max_length:
            current_message += f" {word}"
        else:
            messages.append(current_message)
            current_message = f"{word}"
    messages.append(current_message)
    return messages


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


def read_config(section, file_path=None):
    if file_path is None:
        # Get the directory of the current script/module
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Construct the config file path relative to the script/module directory
        file_path = os.path.join(script_dir, "..", "config", "config.json")

    with open(file_path, "r", encoding="UTF-8") as file:
        config_data = json.load(file)

    if section in config_data:
        return config_data[section]
    raise ValueError(f"The section '{section}' was not found in the configuration file.")
