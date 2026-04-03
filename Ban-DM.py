import discord
from discord.ext import commands

APPEAL_LINK = "your Link"


class BanDM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        try:
            embed = discord.Embed(
                title="🚫 You have been banned",
                description=(
                    f"You have been banned from **{guild.name}**.\n\n"
                    "If you believe this was a mistake, you can submit an unban appeal here:\n\n"
                    f"🔗 {APPEAL_LINK}"
                ),
                color=discord.Color.red()
            )

            embed.set_footer(text="Blackout SMP Moderation System")

            await user.send(embed=embed)

        except discord.Forbidden:
            # User has DMs disabled
            print(f"Could not DM banned user: {user}")

        except Exception as e:
            print(f"Error sending ban DM: {e}")


async def setup(bot):
    await bot.add_cog(BanDM(bot))
