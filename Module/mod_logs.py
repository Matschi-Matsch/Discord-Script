import discord
from discord.ext import commands

LOG_CHANNEL_ID = your-channel-ID


class ModLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------- BAN --------------------
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        channel = guild.get_channel(LOG_CHANNEL_ID)
        if channel is None:
            return

        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            moderator = entry.user
            reason = entry.reason or "No reason provided"

            embed = discord.Embed(
                title="🔨 Member Banned",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            )

            embed.add_field(name="User", value=f"{user} ({user.id})", inline=False)
            embed.add_field(name="Banned by", value=f"{moderator} ({moderator.id})", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)

            await channel.send(embed=embed)
            break

    # -------------------- UNBAN --------------------
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        channel = guild.get_channel(LOG_CHANNEL_ID)
        if channel is None:
            return

        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
            moderator = entry.user

            embed = discord.Embed(
                title="🔓 Member Unbanned",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )

            embed.add_field(name="User", value=f"{user} ({user.id})", inline=False)
            embed.add_field(name="Unbanned by", value=f"{moderator} ({moderator.id})", inline=False)

            await channel.send(embed=embed)
            break

    # -------------------- KICK --------------------
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.get_channel(LOG_CHANNEL_ID)
        if channel is None:
            return

        async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            # Prüfen ob es wirklich dieser User war
            if entry.target.id == member.id:
                moderator = entry.user
                reason = entry.reason or "No reason provided"

                embed = discord.Embed(
                    title="👢 Member Kicked",
                    color=discord.Color.orange(),
                    timestamp=discord.utils.utcnow()
                )

                embed.add_field(name="User", value=f"{member} ({member.id})", inline=False)
                embed.add_field(name="Kicked by", value=f"{moderator} ({moderator.id})", inline=False)
                embed.add_field(name="Reason", value=reason, inline=False)

                await channel.send(embed=embed)
                break


async def setup(bot):
    await bot.add_cog(ModLogs(bot))
