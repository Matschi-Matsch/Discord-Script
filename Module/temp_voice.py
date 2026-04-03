import discord
from discord.ext import commands

# Channel where you go to create your own voice chat
JOIN_CHANNEL_ID = your-channel-ID
# Category in which the temporary VCs are created
VC_CATEGORY_ID = your-category-ID


class TempVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_vcs = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild
        category = guild.get_channel(VC_CATEGORY_ID)
        if category is None:
            return


        if after.channel and after.channel.id == JOIN_CHANNEL_ID:
            
            temp_vc = await guild.create_voice_channel(
                name=f"{member.name}'s Channel",
                category=category,

                overwrites={
                    guild.default_role: discord.PermissionOverwrite(connect=False),
                    member: discord.PermissionOverwrite(
                        connect=True, speak=True, manage_channels=True
                    )
                }
            )

            await member.move_to(temp_vc)
            self.temp_vcs[temp_vc.id] = member.id

        if before.channel and before.channel.id in self.temp_vcs:
            vc = before.channel
            # Wenn kein Mitglied mehr drin
            if len(vc.members) == 0:
                del self.temp_vcs[vc.id]
                await vc.delete()


async def setup(bot):
    await bot.add_cog(TempVoice(bot))