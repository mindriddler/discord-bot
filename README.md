[![Test and lint](https://github.com/mindriddler/chatgpt-discord-bot/actions/workflows/test-and-lint.yml/badge.svg)](https://github.com/mindriddler/chatgpt-discord-bot/actions/workflows/test-and-lint.yml)
[![Release image](https://github.com/mindriddler/chatgpt-discord-bot/actions/workflows/release.yml/badge.svg)](https://github.com/mindriddler/chatgpt-discord-bot/actions/workflows/release.yml)
[![Dev image](https://github.com/mindriddler/chatgpt-discord-bot/actions/workflows/dev.yml/badge.svg)](https://github.com/mindriddler/chatgpt-discord-bot/actions/workflows/dev.yml)
[![Remove old Dev images](https://github.com/mindriddler/chatgpt-discord-bot/actions/workflows/remove-old-dev-images.yml/badge.svg)](https://github.com/mindriddler/chatgpt-discord-bot/actions/workflows/remove-old-dev-images.yml.yml)
# Discord Bot
# Table of Contents

- [Discord Bot](#discord-bot)
- [Table of Contents](#table-of-contents)
  - [Background](#background)
  - [Description](#description)
  - [Usage](#usage)
  - [Coming features](#coming-features)
  - [Contributing](#contributing)
  - [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Creating a discord bot](#creating-a-discord-bot)
    - [Creating an OpenAI API key](#creating-an-openai-api-key)
    - [config.json](#configjson)
      - [OpenAI settings](#openai-settings)
      - [Discord settings](#discord-settings)
      - [Logger settings](#logger-settings)
      - [Schedule settings](#schedule-settings)
      - [Github settings](#github-settings)
    - [Running the bot with Docker](#running-the-bot-with-docker)
      - [Using pre-built Docker images from GHCR](#using-pre-built-docker-images-from-ghcr)
  - [Troubleshooting](#troubleshooting)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)
  - [Contact](#contact)
  - [Disclaimer](#disclaimer)

## Background

I wanted something to do on my spare time outside of my work as a DevSecOps Engineer and my studies at Nackademin.
So i decided to create a discord bot for use in my class discord server.
I also wanted to experiment with setting up github actions.

## Description

This is a discord bot that currently has a few functionalities
* OpenAI ChatGPT
* OpenAI Image Generation
* Able to show a schedule
* Github Stats

## Usage

Once the Discord Bot is running in your server, you can interact with it using the following methods:

1. Use a specific command: `/command_name arguments`

Commands available:
- `/chatgpt <message>`: Interact with ChatGPT using the provided message.
- `/image <message>`: DALL-E will generate a image for you based on the message.
- - Takes 2 optional inputs. Size and number of images
- `/dm`: Send a direct message to the specified user with the provided message.
- - Takes an optional input of a message
- `/github_stats`: Shows simple github stats
- - Takes an optional input of a username.
- `/schedule`: Shows a schedule for the next n days
- - n = number of days (excluding weekends). Take the optional input of number of days. If not supplied it will default to 7 days.
- `/about`: Get information about the ChatGPT Discord Bot.
- `/help`: Display a list of available commands and their usage.



Example:
```
Sender: /chatgpt What is the capital of France?
Theodore: @Sender: The capital of France is Paris.
```
## Coming features

* Give the ChatGPT part of the bot a memory
* DONE! ~~Add image generating AI~~
* Add more options to config.json for AI image generation
* Make the schedule be more dynamic and take more inputs from the user

## Contributing

If you want to contribute to this project, please read the [CONTRIBUTING](CONTRIBUTING.md) file.
## Installation

## Prerequisites

* Docker

## Setup

I have not provided either the OpenAI API key or the discord bot token.
You will need to create your own.

### Creating a discord bot
1. Go to [developer applications](https://discord.com/developers/applications) and log in with your discord account.
2. Click on "New Application" and give it a name.
3. Click on "Bot" in the menu on the left.
4. Click on "Reset Token"
5. Copy the token and save it somewhere safe, you're going to need it later
6. Make sure that that you tick the 3 bottoms checks ([like this](https://github.com/mindriddler/discord-bot/blob/main/assets/bot_settings.jpg?raw=true))
7. Click on "Add Bot" and confirm.
8. Click on "OAuth2"
9. Click on "URL Generator"
10.  Select "bot" and "applications.commands"
11. Make sure that that you set the correct permissions ([example](https://github.com/mindriddler/discord-bot/blob/main/assets/bot_permissions.jpg?raw=true))
12. Copy the link and paste it in your browser.
13. Select the server you want to add the bot to.
14. Click on "Authorize"
15. You should now see the bot in your server.

### Creating an OpenAI API key
1. Go to [OpenAI](https://beta.openai.com/) and log in with your OpenAI account.
2. Click on your account in the op right
3. Click on "View API keys"
4. Click on "Create new secret key"
5. Copy the key and save it somewhere safe, you're going to need it later
### config.json

The config.json file is used to configure some settings of the bot.
The file is located in the `src/config` folder.

#### OpenAI settings
| Variable           | What it is                                                          | Default           |
| ------------------ | ------------------------------------------------------------------- | ----------------- |
| openai.model       | The OpenAI model to use                                             | chatgpt-3.5-turbo |
| openai.temperature | The temperature to use for OpenAI model responses                   | 1                 |
| openai.max_tokens  | The maximum number of tokens to generate for OpenAI model responses | 4000              |

#### Discord settings

<h5> The two top values NEEDS to be set, otherwise the bot will not listen to anything </h5>

| Variable                     | What it is                                                           | Default                                                                                              |
| ---------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| discord.dedicated_channel_id | The ID of the dedicated channel for the bot to listen to messages on | None                                                                                                 |
| discord.log_folder           | The folder where logs will be stored                                 | logs                                                                                                 |
| discord.log_path_channel     | The path for channel logs                                            | <details> <summary> *Show* </summary> logs/channel_{time:YYYY-MM-DD-HH-mm-ss-SSS!UTC}.log </details> |
| discord.log_path_command     | The path for command logs                                            | <details> <summary> *Show* </summary> logs/command_{time:YYYY-MM-DD-HH-mm-ss-SSS!UTC}.log </details> |

#### Logger settings
| Variable                      | What it is                                             | Default   |
| ----------------------------- | ------------------------------------------------------ | --------- |
| logger.log_level              | The level of logging to use                            | DEBUG     |
| logger.log_rotation           | The maximum size of each log file before it is rotated | 100000000 |
| logger.log_retention          | The length of time to retain log files for             | 730 days  |
| logger.log_compression_format | The format of the compressed log files                 | zip       |

#### Schedule settings
| Variable     | What it is                 | Default |
| ------------ | -------------------------- | ------- |
| schedule.url | URL to your class schedule | None    |

#### Github settings
| Variable            | What it is                                                                      | Default                                                                                                                                              |
| ------------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| github.user_stats   | API link for stats                                                              | <details> <summary> *Show* </summary> https://github-readme-stats.vercel.app/api?username={}&show_icons=true&theme=dark&hide_border=true" </details> |
| github.user_streak  | API link for streak                                                             | <details> <summary> *Show* </summary> https://streak-stats.demolab.com/?user={}&theme=dark&hide_border=true </details>                               |
| github.default_user | Default user for stats and streak API of no username is provided in the command | mindriddler                                                                                                                                          |

You can change these values to whatever (as long as they're valid) you want and the bot will respect them

### Running the bot with Docker
1. Clone the repo
2. Rename the file called `.env.template` in the root of the project to `.env`
3. Add the following lines to the file:
```bash
OPENAI_API_KEY=<your api key>
DISCORD_TOKEN=<your bot token>
```
4. Change your working directory to `Docker`
5. Run `docker-compose up -d`

#### Using pre-built Docker images from GHCR
If you prefer not to build the Docker image yourself, you can pull the pre-built images from GitHub Container Registry (GHCR). However, you will still need to provide your own OpenAI API key and Discord bot token.

To pull the images from GHCR, use the following command:

```bash
docker pull ghcr.io/mindriddler/discord-bot:<tag>
```
Replace `<tag>` with the appropriate tag for the version you want to use (e.g., `latest`).

After pulling the image, you can run the container using the following command:
```bash
docker run -d --name discord-bot --env-file .env ghcr.io/mindriddler/discord-bot:<tag>
```

Replace `<tag>` with the same tag used when pulling the image.

## Troubleshooting

If you encounter any issues while setting up or using the ChatGPT Discord Bot, please consult the following resources:

1. Check the [OpenAI API documentation](https://beta.openai.com/docs/) and ensure your API key is set up correctly.
2. Review the [discord.py documentation](https://discordpy.readthedocs.io/en/stable/) for possible issues related to Discord interactions.
3. If you still need help, please create an issue on this repository or contact me through one of the methods provided in the "Contact" section of this README.

## License

This project is licensed under the GNU License - see the [LICENSE](LICENSE.md) file for details

## Acknowledgments

* [OpenAI](https://openai.com/)
* [Discord](https://discord.com/)
* [Docker](https://www.docker.com/)
* [Python](https://www.python.org/)
* [discord.py](https://discordpy.readthedocs.io/en/stable/)

## Contact

If you want to contact me you can reach me at

* Discord: `Wikipedia#5457`
* Email: `fredrikmagnusson10@live.se`
* Github: [mindriddler](https://github.com/mindriddler)
* LinkedIn: [Link](https://www.linkedin.com/in/fredrik-m/)

## Disclaimer

This project is not affiliated with OpenAI or Discord in any way.
