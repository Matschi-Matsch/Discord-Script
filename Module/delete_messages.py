import discord
from discord.ext import commands

# 🔒 Hier deine erlaubten Rollen eintragen
ALLOWED_ROLE_IDS = [
    Your Role ID,  # Rolle 1
    Your Role ID   # Rolle 2
]


class DeleteMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="delete")
    async def delete_messages(self, ctx, amount: int):

        # Prüfen ob User eine erlaubte Rolle hat
        user_role_ids = [role.id for role in ctx.author.roles]
        if not any(role_id in ALLOWED_ROLE_IDS for role_id in user_role_ids):
            await ctx.send("You are not allowed to use this command.", delete_after=5)
            return

        if amount < 1:
            await ctx.send("Please enter a number greater than 0.", delete_after=5)
            return

        # Max 100 Nachrichten (Discord Limit)
        if amount > 100:
            amount = 100

        # +1 damit der Befehl selbst gelöscht wird
        deleted = await ctx.channel.purge(limit=amount + 1)

        confirmation = await ctx.send(f"Deleted {len(deleted)-1} messages.")
        await confirmation.delete(delay=5)

    @delete_messages.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Please provide a valid number.", delete_after=5)


async def setup(bot):
    await bot.add_cog(DeleteMessages(bot))

