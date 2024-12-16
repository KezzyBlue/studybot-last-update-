import discord
from discord.ext import commands
import os
from config.settings import BOT_TOKEN, PREFIX

# Tạo bot với tiền tố lệnh
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Load các cogs từ thư mục cogs
@bot.event
async def on_ready():
    print(f"{bot.user.name} đã sẵn sàng hoạt động!")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"Đã tải {filename}")
            except Exception as e:
                print(f"Lỗi khi tải {filename}: {e}")

# Lệnh reload cogs (only admin)
@bot.command(name='reload', help="Tải lại một hoặc tất cả các cogs.")
@commands.is_owner()
async def reload(ctx, cog_name=None):
    if cog_name:
        try:
            bot.unload_extension(f'cogs.{cog_name}')
            bot.load_extension(f'cogs.{cog_name}')
            await ctx.send(f"🔄 Đã tải lại cog: {cog_name}")
        except Exception as e:
            await ctx.send(f"❌ Không thể tải lại cog {cog_name}: {e}")
    else:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.unload_extension(f'cogs.{filename[:-3]}')
                bot.load_extension(f'cogs.{filename[:-3]}')
        await ctx.send("🔄 Đã tải lại tất cả các cogs!")

# Chạy bot
if __name__ == "__main__":
    try:
        bot.run(BOT_TOKEN)
    except Exception as e:
        print(f"Lỗi khi chạy bot: {e}")