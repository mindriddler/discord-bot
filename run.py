from src.discord_bot.discord_api import bot, discord_token


if __name__ == "__main__":
    bot.run(discord_token, log_handler=None)
