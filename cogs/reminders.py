import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = []

    @commands.command(name="remind")
    async def remind(self, ctx, time: str, *, message: str):
        # Kiểm tra và chuyển đổi thời gian
        delay = self.parse_time(time)
        if delay is None:
            await ctx.send("⚠️ Định dạng thời gian không hợp lệ. Ví dụ: 10s, 5m, 1h, 2d, 1w.")
            return

        # Tính thời gian nhắc nhở
        reminder_time = datetime.now() + timedelta(seconds=delay)
        self.reminders.append((ctx.author.id, reminder_time, message))
        await ctx.send(f"⏰ Đã đặt nhắc nhở: {message} sau {time}")

        # Chờ đợi thời gian trễ và gửi nhắc nhở
        await asyncio.sleep(delay)
        await ctx.author.send(f"🔔 Nhắc nhở: {message}")

    def parse_time(self, time_str):
        units = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}  # Đơn vị thời gian
        try:
            time_unit = time_str[-1]  # Lấy ký tự cuối cùng làm đơn vị
            time_value = int(time_str[:-1])  # Phần còn lại là giá trị thời gian
            if time_unit in units:
                return time_value * units[time_unit]  # Chuyển đổi sang giây
            else:
                return None
        except (ValueError, KeyError):
            return None

def setup(bot):
    bot.add_cog(Reminder(bot))
