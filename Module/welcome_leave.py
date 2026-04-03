import discord
from discord.ext import commands
from datetime import datetime

WELCOME_CHANNEL_ID = your-channel-ID
LEAVE_CHANNEL_ID = your-channel-ID


class WelcomeLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------- MEMBER JOIN --------------------

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
        if channel is None:
            return

        embed = discord.Embed(
            title="Welcome!",
            description=(
                f"Hey {member.mention}! Please follow all our rules and "
                f"make sure you are polite and respectful to others.\n\n"
                f"Now, have fun!"
            ),
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )

        # Profilbild des Users als Thumbnail
        embed.set_thumbnail(url=member.display_avatar.url)

        # Footer mit User-ID
        embed.set_footer(text=f"Member ID: {member.id}")

        await channel.send(embed=embed)

    # -------------------- MEMBER LEAVE --------------------

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.get_channel(LEAVE_CHANNEL_ID)
        if channel is None:
            return

        embed = discord.Embed(
            title="Bye!",
            description=(
                f"We will miss u {member.mention} "
                f"(unless u got banned by violating the rules 😶)"
            ),
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )

        # Profilbild des Users als Thumbnail
        embed.set_thumbnail(url=member.display_avatar.url)

        # Footer mit User-ID
        embed.set_footer(text=f"User ID: {member.id}")

        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(WelcomeLeave(bot))
