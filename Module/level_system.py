import discord
from discord.ext import commands, tasks
import json, os, random, time
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

LEVEL_UP_CHANNEL = your-CHANNEL-id
LEADERBOARD_CHANNEL = your-CHANNEL-id

LEVEL_ROLES = {
    1: your-role-id,
    2: your-role-id,
    3: your-role-id,
    4: your-role-id,
    5: your-role-id,
    6: your-role-id,
    7: your-role-id,
    8: your-role-id,
    9: your-role-id,
    10: your-role-id
}

DATA_FILE = "levels.json"
XP_COOLDOWN = 10  # seconds

last_message_time = {}


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


levels = load_data()


def xp_needed(level):
    xp_table = {
        0: 100,
        1: 125,
        2: 150,
        3: 175,
        4: 200,
        5: 225,
        6: 250,
        7: 275,
        8: 300,
        9: 325,
        10: 350
    }

    if level in xp_table:
        return xp_table[level]
    else:
        return 350 + (level - 10) * 25


async def create_level_card(user, level, xp):

    width, height = 800, 250
    img = Image.new("RGB", (width, height), (30, 30, 30))
    draw = ImageDraw.Draw(img)

    # Avatar laden
    avatar_url = user.display_avatar.url
    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content)).resize((180, 180))

    img.paste(avatar, (30, 35))

    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()

    draw.text((250, 50), user.name, font=font_big, fill=(255, 255, 255))
    draw.text((250, 100), f"Level: {level}", font=font_small, fill=(200, 200, 200))
    draw.text((250, 130), f"XP: {xp}/{xp_needed(level)}", font=font_small, fill=(200, 200, 200))

    bar_x = 250
    bar_y = 170
    bar_width = 400
    progress = int((xp / xp_needed(level)) * bar_width)

    draw.rectangle((bar_x, bar_y, bar_x + bar_width, bar_y + 20), fill=(50, 50, 50))
    draw.rectangle((bar_x, bar_y, bar_x + progress, bar_y + 20), fill=(0, 200, 255))

    path = f"level_{user.id}.png"
    img.save(path)

    return path


class LevelView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="📊 My Level", style=discord.ButtonStyle.blurple)
    async def my_level(self, interaction: discord.Interaction, button: discord.ui.Button):

        user_id = str(interaction.user.id)

        if user_id not in levels:
            lvl, xp = 0, 0
        else:
            lvl = levels[user_id]["level"]
            xp = levels[user_id]["xp"]

        card = await create_level_card(interaction.user, lvl, xp)

        file = discord.File(card, filename="level.png")

        await interaction.response.send_message(file=file, ephemeral=True)


class LevelSystem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.leaderboard.start()

    def cog_unload(self):
        self.leaderboard.cancel()

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        now = time.time()
        last_time = last_message_time.get(message.author.id, 0)

        if now - last_time < XP_COOLDOWN:
            return

        last_message_time[message.author.id] = now

        user_id = str(message.author.id)

        if user_id not in levels:
            levels[user_id] = {"xp": 0, "level": 0}

        levels[user_id]["xp"] += random.randint(10, 20)

        level = levels[user_id]["level"]
        xp = levels[user_id]["xp"]

        if xp >= xp_needed(level):
            levels[user_id]["xp"] -= xp_needed(level)
            levels[user_id]["level"] += 1

            role_id = LEVEL_ROLES.get(levels[user_id]["level"])
            if role_id:
                role = message.guild.get_role(role_id)
                if role:
                    await message.author.add_roles(role)

            channel = message.guild.get_channel(LEVEL_UP_CHANNEL)

            if channel:
                card = await create_level_card(message.author, levels[user_id]["level"], 0)
                file = discord.File(card, filename="level.png")

                await channel.send(
                    content=f"{message.author.mention}",
                    file=file
                )

        save_data(levels)

    @tasks.loop(seconds=30)
    async def leaderboard(self):

        await self.bot.wait_until_ready()

        channel = self.bot.get_channel(LEADERBOARD_CHANNEL)
        if not channel:
            return

        sorted_users = sorted(levels.items(), key=lambda x: x[1]["level"], reverse=True)[:10]

        desc = ""
        for i, (uid, data) in enumerate(sorted_users, 1):
            desc += f"**#{i}** <@{uid}> • Level {data['level']}\n"

        embed = discord.Embed(
            title="🏆 Leaderboard",
            description=desc or "No data",
            color=discord.Color.gold()
        )

        async for msg in channel.history(limit=5):
            if msg.author == self.bot.user:
                await msg.edit(embed=embed, view=LevelView(self.bot))
                return

        await channel.send(embed=embed, view=LevelView(self.bot))


async def setup(bot):
    await bot.add_cog(LevelSystem(bot))