import discord
from discord.ext import commands
import json
import os

class FinanceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.balances = self.load_balances()

    BALANCE_FILE = "balances.json"

    def load_balances(self):
        if os.path.exists(self.BALANCE_FILE):
            with open(self.BALANCE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_balances(self):
        with open(self.BALANCE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.balances, f, indent=4, ensure_ascii=False)

    @discord.app_commands.command(name="syu", description="収支を更新します")
    @discord.app_commands.describe(type="pかmか入力してね！", amount="金額を入力してね！")
    async def syu(self, interaction: discord.Interaction, type: str, amount: int):
        user_id = str(interaction.user.id)

        if user_id not in self.balances:
            self.balances[user_id] = 0

        if type == "p":
            self.balances[user_id] += amount
        elif type == "m":
            self.balances[user_id] -= amount
        else:
            await interaction.response.send_message("typeは 'p' または 'm' のみです。")
            return

        self.save_balances()

        await interaction.response.send_message(f"{interaction.user.name} の現在の収支は {('p' if self.balances[user_id] >= 0 else 'm')}{abs(self.balances[user_id])} です。")

async def setup(bot):
    await bot.add_cog(FinanceCog(bot))
