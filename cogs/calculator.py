from discord.ext import commands
import discord

class CalculatorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='c', description="式を入れると計算します")
    async def calculate(self, interaction: discord.Interaction, expression: str):
        try:
            result = eval(expression)
            await interaction.response.send_message(f'結果: {result}')
        except Exception:
            await interaction.response.send_message('計算式が無効です。')
