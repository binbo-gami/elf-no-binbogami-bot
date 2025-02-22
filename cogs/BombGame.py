import random
import discord
from discord.ext import commands
from discord import app_commands

class BombGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hp = 30
        self.turn = None  # "player" or "bot"
        self.roll_result = None  # 直前のサイコロ結果

    async def start_game(self, interaction: discord.Interaction):
        """爆弾ゲームを開始する"""
        self.hp = 30
        self.turn = "player"
        self.roll_result = None
        await interaction.response.send_message("開始しました！ `/bkroll` でダイスを振ってください。")

    async def roll_dice(self, interaction: discord.Interaction):
        """サイコロを振る"""
        if self.turn != "player":
            await interaction.response.send_message("現在はあなたのターンではありません！", ephemeral=True)
            return

        self.roll_result = random.randint(1, 100)
        if self.roll_result == 100:
            self.hp = 0
            self.turn = None
            await interaction.response.send_message("親即が出ました！Botの勝利です！")
            return

        await interaction.response.send_message(f"ダイスの結果: {self.roll_result}\n1の位を引くなら `/itikura` 、10の位を引くなら `/jukura`")

    async def player_choose(self, interaction: discord.Interaction, choice):
        """プレイヤーの選択処理"""
        if self.turn != "player":
            await interaction.response.send_message("現在はあなたのターンではありません！", ephemeral=True)
            return

        if self.roll_result is None:
            await interaction.response.send_message("先に `/bkroll` でダイスを振ってください！", ephemeral=True)
            return

        damage = self.roll_result % 10 if choice == "1" else self.roll_result // 10
        self.hp -= damage
        self.roll_result = None

        if self.hp <= 0:
            self.turn = None
            await interaction.response.send_message(f"{damage}ダメージ！HPが0になりました！あなたの負けです！")
            return

        self.turn = "bot"
        await interaction.response.send_message(f"{damage}ダメージ！ 残りHP: {self.hp}\n次はBotのターンです。")

        await self.bot_turn(interaction)

    async def bot_turn(self, interaction: discord.Interaction):
        """Botのターン"""
        if self.turn != "bot":
            return

        bot_roll = random.randint(1, 100)
        if bot_roll == 100:
            self.hp = 0
            self.turn = None
            await interaction.followup.send("親即が出ました！Botの勝利です！")
            return

        ones = bot_roll % 10
        tens = bot_roll // 10

        # 1,2,3,4,12,13,14,15を優先
        priority_numbers = {1, 2, 3, 4, 12, 13, 14, 15}
        if ones in priority_numbers:
            bot_choice = ones
        elif tens in priority_numbers:
            bot_choice = tens
        else:
            bot_choice = random.choice([ones, tens])

        self.hp -= bot_choice
        self.turn = "player"

        if self.hp <= 0:
            self.turn = None
            await interaction.followup.send(f" Botの出目: {bot_roll}\nBotは {bot_choice} を選びました！\nHPが0になりました！Botの負けです！")
            return

        await interaction.followup.send(f" Botの出目: {bot_roll}\nBotは {bot_choice} を選びました！ 残りHP: {self.hp}\nあなたのターンです。 `/bkroll` でダイスを振ってください！")

    @commands.Cog.listener()
    async def on_ready(self):
        print("BombGame Cog がロードされました")

    # スラッシュコマンド
    @app_commands.command(name="bk", description="botとｂｋで勝負！")
    async def bk(self, interaction: discord.Interaction):
        await self.start_game(interaction)

    @app_commands.command(name="bkroll", description="ダイスを振ります。")
    async def bkroll(self, interaction: discord.Interaction):
        await self.roll_dice(interaction)

    @app_commands.command(name="itikura", description="1の位を引きます。")
    async def itikura(self, interaction: discord.Interaction):
        await self.player_choose(interaction, "1")

    @app_commands.command(name="jukura", description="10の位を引きます。")
    async def jukura(self, interaction: discord.Interaction):
        await self.player_choose(interaction, "10")

async def setup(bot):
    """BotにCogを追加"""
    await bot.add_cog(BombGame(bot))

# -----------------------------------------------------------------------------
# Copyright (c) 2025 みらい@milie_usotsuki
#https://x.com/milie_usotsuki
# -----------------------------------------------------------------------------
