import discord
from discord.ext import commands
import json
from utils.db import load_data

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="total")
    async def stats(self, ctx):
        """Hiển thị thống kê công việc"""
        tasks = load_data("data/tasks.json", default=[])
        completed = sum(1 for task in tasks if task.get("completed"))
        total = len(tasks)
        await ctx.send(f"📊 Bạn đã hoàn thành {completed}/{total} công việc.")

def setup(bot):
    bot.add_cog(Stats(bot))