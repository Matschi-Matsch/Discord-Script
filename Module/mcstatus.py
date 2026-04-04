import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer

SERVER_IP = "Your Server IP"
SERVER_NAME = "Your Server Name"
CHANNEL_ID = Your-channel-Id


class CopyIPButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Copy IP",
        style=discord.ButtonStyle.primary,
        custom_id="copy_ip_button"
    )
    async def copy_ip(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"```{SERVER_IP}```",
            ephemeral=True
        )


class MinecraftStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_task.start()
        bot.add_view(CopyIPButton())  # Persistent Button

    def cog_unload(self):
        self.status_task.cancel()

    @tasks.loop(seconds=30)
    async def status_task(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(CHANNEL_ID)

        if channel is None:
            return

        try:
            server = JavaServer.lookup(SERVER_IP)
            status = server.status()

            motd = status.description
            if isinstance(motd, dict):
                motd = motd.get("text", "No MOTD available")

            embed = discord.Embed(
                title=f"{SERVER_NAME} - Server Online",
                color=discord.Color.green()
            )

            embed.add_field(name="Server IP", value=SERVER_IP, inline=False)
            embed.add_field(
                name="Players Online",
                value=f"{status.players.online}/{status.players.max}",
                inline=False
            )
            embed.add_field(name="MOTD", value=motd, inline=False)

        except Exception:
            embed = discord.Embed(
                title=f"{SERVER_NAME} - Server Offline",
                description="The server is currently offline or unreachable.",
                color=discord.Color.red()
            )

        async for message in channel.history(limit=20):
            if message.author == self.bot.user and message.embeds:
                if message.embeds[0].title.startswith(SERVER_NAME):
                    await message.edit(embed=embed, view=CopyIPButton())
                    return

        await channel.send(embed=embed, view=CopyIPButton())


async def setup(bot):
    await bot.add_cog(MinecraftStatus(bot))

