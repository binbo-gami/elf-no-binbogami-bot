import discord
from discord.ext import commands
import random

class DiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="roll", description="1d100のダイスを振ります")
    async def roll(self, interaction: discord.Interaction):
        result = random.randint(1, 100)
        await interaction.response.send_message(f'🎲 ダイスの結果は {result} です！')

async def setup(bot):
    await bot.add_cog(DiceCog(bot))

# -----------------------------------------------------------------------------
# Copyright (c) 2025 みらい@milie_usotsuki
#https://x.com/milie_usotsuki
# -----------------------------------------------------------------------------