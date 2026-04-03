import discord
from discord.ext import commands

APPEAL_CHANNEL_ID = your-channel-ID  # Channel for the Appeal button
LOG_CHANNEL_ID = your-channel-ID     # Channel where the answers are posted


# -------------------- MODAL --------------------
class UnbanAppealModal(discord.ui.Modal, title="Unban Appeal Form"):
    minecraft_name = discord.ui.TextInput(
        label="Your Minecraft name?",
        style=discord.TextStyle.short,
        required=True,
        max_length=50
    )

    action_done = discord.ui.TextInput(
        label="What did you do?",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=500
    )

    reason = discord.ui.TextInput(
        label="Why should we unban you?",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=500
    )
       
    clip = discord.ui.TextInput(
        label="Clip URL?",
        style=discord.TextStyle.short,
        required=True,
        max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction):
        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel is None:
            await interaction.response.send_message("Log channel not found.", ephemeral=True)
            return

        embed = discord.Embed(
            title="📝 New Unban Appeal",
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow()
        )

        embed.add_field(name="User", value=f"{interaction.user} ({interaction.user.id})", inline=False)
        embed.add_field(name="Minecraft Name", value=self.minecraft_name.value, inline=False)
        embed.add_field(name="What did you do?", value=self.action_done.value, inline=False)
        embed.add_field(name="Why should we unban you?", value=self.reason.value, inline=False)
        embed.add_field(name="Clip URL?", value=self.clip.value, inline=False)

        await log_channel.send(embed=embed)
        await interaction.response.send_message("Your appeal has been submitted!", ephemeral=True)


# -------------------- BUTTON --------------------
class UnbanAppealView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Unban Appeal",
        style=discord.ButtonStyle.green,
        emoji="📝",
        custom_id="unban_appeal_button"
    )
    async def appeal_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(UnbanAppealModal())



# -------------------- COG --------------------
class UnbanAppeal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Registriere die persistent View
        bot.add_view(UnbanAppealView())

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(APPEAL_CHANNEL_ID)
        if channel is None:
            return
        
                # Prüfen ob Embed schon existiert
        async for message in channel.history(limit=30):
            if message.embeds:
                if message.embeds[0].title == "U think ur ban was a mistake?":
                    print("Ban embed already exists.")
                    return


        embed = discord.Embed(
            title="U think ur ban was a mistake?",
            description="Click the button below to submit an unban appeal.",
            color=discord.Color.green()
        )

        await channel.send(embed=embed, view=UnbanAppealView())


async def setup(bot):
    await bot.add_cog(UnbanAppeal(bot))

