# from discord.ext import commands

# from chatgpt.chatgpt_functions import ChatGPTFunctions
# from chatgpt.openai_api import chatgpt_response
# from utils.utils import DEFAULT_DM_MESSAGE


# class ChatGPTCog(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.chatgptfunctions = ChatGPTFunctions(self)

#     @commands.command()
#     async def chatgpt(self, ctx, *, message: str = None):
#         if message is None:
#             await ctx.send("Please provide a message to discuss with ChatGPT.")
#         else:
#             bot_response = chatgpt_response(prompt=message)
#             await ctx.send(f"{ctx.author.mention}: {bot_response}")

#     @commands.command()
#     async def dm(self, ctx):
#         dm_channel = await ctx.author.create_dm()
#         self.bot.logger.info("test")
#         await dm_channel.send(f"Hello {ctx.author.name}, {DEFAULT_DM_MESSAGE}")

#     @commands.command()
#     async def close_thread(self, ctx):
#         self.bot.logger.command("closing thread")
#         ChatGPTFunctions.delete_thread_after_delay(ctx.thread, delay=10)


# async def setup(bot):
#     await bot.add_cog(ChatGPTCog(bot))
