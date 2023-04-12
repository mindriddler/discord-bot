from dotenv import load_dotenv
import discord
import os

from src.chatgpt_ai.openai import chatgpt_response

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")


class Client(discord.Client):
    async def on_ready(self):
        print("Successfully logged in as: ", self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        # Replace CHANNEL_ID with the ID of the channel dedicated to the bot
        dedicated_channel_id = 1095796880706908160

        # Check if the message comes from the dedicated channel or DMs
        if message.channel.id == dedicated_channel_id:
            user_message = message.content
            print(f"Message from {message.author}: \n{user_message}\n")
            bot_response = chatgpt_response(prompt=user_message)
            await message.channel.send(
                f"Answer for {message.author.mention}: {bot_response}"
            )

            print(f"Answer in DM for author {message.author}: \n{bot_response}\n")
        elif message.channel.id == isinstance(message.channel, discord.DMChannel):
            user_message = message.content
            print(f"Message from {message.author}: \n{user_message}\n")
            bot_response = chatgpt_response(prompt=user_message)
            await message.channel.send(f"{bot_response}")
            print(f"Answer in DM for author {message.author}: \n{bot_response}\n")

        else:
            command, user_message = None, None

            for text in ["/ai", "/bot", "/chatgpt", "/gpt", "/dm"]:
                if message.content.startswith(text):
                    command = message.content.split(" ")[0]
                    user_message = message.content.replace(text, "")

            if command in ["/ai", "/bot", "/chatgpt", "/gpt"]:
                print(f"Command: {command}, User message: {user_message}")
                bot_response = chatgpt_response(prompt=user_message)
                await message.channel.send(f"Answer: {bot_response}")
            elif command == "/dm chatgpt":
                print(f"DM Command received from {message.author}")
                dm_channel = await message.author.create_dm()
                await dm_channel.send(
                    f"Hello {message.author.name}, this is a DM from the bot. You can now have a conversation with me here."
                )


intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
