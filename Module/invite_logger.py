import discord
from discord.ext import commands

CHANNEL_ID = your-channel-ID


class InviteLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invites = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            try:
                self.invites[guild.id] = await guild.invites()
            except:
                pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        channel = guild.get_channel(CHANNEL_ID)

        try:
            new_invites = await guild.invites()
        except:
            return

        old_invites = self.invites.get(guild.id, [])
        used_invite = None

        for invite in new_invites:
            for old in old_invites:
                if invite.code == old.code and invite.uses > old.uses:
                    used_invite = invite
                    break

        self.invites[guild.id] = new_invites

        if not used_invite:
            return

        embed = discord.Embed(
            title="📥 New member joined",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Member",
            value=f"{member.mention} ({member.id})",
            inline=False
        )

        embed.add_field(
            name="Invite",
            value=(
                f"Invite-Code: `{used_invite.code}`\n"
                f"Channel: {used_invite.channel.mention}\n"
                f"Invited by: {used_invite.inviter.mention}\n"
                f"Uses: {used_invite.uses}"
            ),
            inline=False
        )

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.get_channel(CHANNEL_ID)
        if channel is None:
            return

        embed = discord.Embed(
            title="📤 Member left",
            description=f"{member} ({member.id})",
            color=discord.Color.red()
        )

        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(InviteLogger(bot))

