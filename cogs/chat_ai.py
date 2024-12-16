import discord
from discord.ext import commands
import openai
from config.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class ChatAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ask")
    async def ask(self, ctx, *, question: str):
        """Hỏi AI: !ask Câu hỏi của bạn"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # Hoặc model bạn muốn sử dụng, như gpt-3.5-turbo, gpt-4,...
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            await ctx.send(response['choices'][0]['message']['content'])
        except Exception as e:
            await ctx.send(f"Đã có lỗi xảy ra: {e}")

def setup(bot):
    bot.add_cog(ChatAI(bot))
