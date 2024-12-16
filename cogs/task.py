import discord
from discord.ext import commands
from utils.db import load_data, save_data

class TaskManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_data("data/data.json", default={})

    @commands.command(name="add")
    async def add_task(self, ctx, *, task: str):
        """Thêm công việc vào danh sách"""
        user_id = str(ctx.author.id)
        if user_id not in self.data:
            self.data[user_id] = {"tasks": [], "score": 0}
        self.data[user_id]["tasks"].append(task)
        save_data("data/data.json", self.data)

        
        embed = discord.Embed(
            title="✅ Công việc đã được thêm!",
            description=f"Đã thêm công việc: **{task}** vào danh sách công việc của bạn.",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=ctx.author.avatar.url)  
        embed.set_footer(text=f"Thêm công việc bởi {ctx.author.name}")
        embed.set_image(url="https://i.pinimg.com/736x/28/f6/d5/28f6d5b7fcdbcd438a7d6e554435ae5e.jpg")  # Hình ảnh động nếu cần
        await ctx.send(embed=embed)

    @commands.command(name="done")
    async def complete_task(self, ctx, task_number: int):
        """Hoàn thành công việc và nhận điểm"""
        user_id = str(ctx.author.id)
        if user_id not in self.data or len(self.data[user_id]["tasks"]) < task_number or task_number <= 0:
            await ctx.send("❌ Công việc không tồn tại hoặc số thứ tự không hợp lệ.")
            return

       
        completed_task = self.data[user_id]["tasks"].pop(task_number - 1)
        self.data[user_id]["score"] += 10
        save_data("data/data.json", self.data)

        
        embed = discord.Embed(
            title="✅ Công việc hoàn thành!",
            description=f"Đã hoàn thành công việc: **{completed_task}** (+10 điểm)",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=ctx.author.avatar.url)  
        embed.set_footer(text=f"Hoàn thành công việc bởi {ctx.author.name}")
        embed.set_image(url="https://i.pinimg.com/736x/28/f6/d5/28f6d5b7fcdbcd438a7d6e554435ae5e.jpg")  # Hình ảnh động nếu cần
        await ctx.send(embed=embed)

    @commands.command(name="list")
    async def list_tasks(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in self.data or not self.data[user_id]["tasks"]:
            embed = discord.Embed(
                title="❌ Không có công việc!",
                description="Danh sách công việc hiện đang trống.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Hãy thêm công việc để bắt đầu.")
            await ctx.send(embed=embed)
        else:
            task_list = "\n".join([f"{i+1}. {task}" for i, task in enumerate(self.data[user_id]["tasks"])])
            embed = discord.Embed(
                title="📋 Danh sách công việc:",
                description=task_list,
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Điểm hiện tại: {self.data[user_id]['score']}")
            await ctx.send(embed=embed)

    @commands.command(name="rank")
    async def rank(self, ctx):
        """Hiển thị điểm của bạn"""
        user_id = str(ctx.author.id)
        score = self.data.get(user_id, {}).get("score", 0)


        embed = discord.Embed(
            title=f"🏅 Điểm của {ctx.author.name}",
            description=f"Bạn hiện có **{score} điểm**.",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=ctx.author.avatar.url)  
        embed.set_footer(text="Tiếp tục làm việc để tăng điểm!")
        await ctx.send(embed=embed)

    @commands.command(name="top")
    async def leaderboard(self, ctx):
        """Hiển thị bảng xếp hạng"""
        sorted_users = sorted(self.data.items(), key=lambda x: x[1]["score"], reverse=True)
        if not sorted_users:
            embed = discord.Embed(
                title="📋 Bảng xếp hạng",
                description="Hiện tại không có ai có điểm.",
                color=discord.Color.red()
            )
            embed.set_image(url="https://i.pinimg.com/originals/5e/5b/d2/5e5bd20f5991cbd195f5c32e575dc22a.jpg")  # Hình ảnh trống
            embed.set_footer(text="Hãy bắt đầu thêm công việc và hoàn thành!")
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="📋 Bảng xếp hạng",
            color=discord.Color.gold()
        )

        for i, (user_id, user_data) in enumerate(sorted_users, 1):
            user = await self.bot.fetch_user(int(user_id))
            embed.add_field(
                name=f"#{i} {user.name if user else 'Unknown'}",
                value=f"Điểm: **{user_data['score']}** điểm",
                inline=False
            )
        
        embed.set_footer(text="Cập nhật: Bảng xếp hạng")
        await ctx.send(embed=embed)
    @commands.command(name="del")
    async def delete_task(self, ctx, task_number: int):
        """Xóa một công việc khỏi danh sách"""
        user_id = str(ctx.author.id)
        if user_id not in self.data or len(self.data[user_id]["tasks"]) < task_number or task_number <= 0:
            await ctx.send("❌ Công việc không tồn tại hoặc số thứ tự không hợp lệ.")
            return

        deleted_task = self.data[user_id]["tasks"].pop(task_number - 1)
        save_data("data/data.json", self.data)

        embed = discord.Embed(
            title="🗑️ Xóa công việc thành công!",
            description=f"Đã xóa công việc: **{deleted_task}** khỏi danh sách.",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=ctx.author.avatar.url)  
        embed.set_footer(text=f"Xóa công việc bởi {ctx.author.name}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(TaskManager(bot))
