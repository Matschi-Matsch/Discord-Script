import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.invites = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_all_cogs():
    for filename in os.listdir("./module"):
        if filename.endswith(".py") and filename != "__init__.py":
            cog_name = f"module.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                print(f"✅ Loaded module: {filename}")
            except Exception as e:
                print(f"❌ Fehler beim Laden von {filename}: {e}")


@bot.event
async def on_ready():
    print(f"Bot ready: {bot.user}")
    for view in bot._views:
        bot.add_view(view)

async def main():
    async with bot:
        await load_all_cogs()
        await bot.start("Your Bot Token")

asyncio.run(main())
