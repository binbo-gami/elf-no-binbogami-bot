from discord.ext import commands
import discord
import random

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="choose", description="選択肢をつくり、ランダムで選びます")
    async def choose(self, interaction: discord.Interaction, options: str):
        option_list = options.split()
        if option_list:
            await interaction.response.send_message(f'選ばれたのは: {random.choice(option_list)}')
        else:
            await interaction.response.send_message('選択肢を入力してください。')

    @discord.app_commands.command(name="used", description="使い方を表示します")
    async def used(self, interaction: discord.Interaction):
        description = (
            "**Botの使い方:**\n\n"
            "**ダイスを振る: `/roll`**\n"
            "ランダムで1から100の間で数字を振り、その結果を表示します。\n\n"
            "**ボイスチャットに参加: `/join`**\n"
            "自分が参加しているボイスチャットにボットを参加させます。\n\n"
            "**ボイスチャットから退出: `/leave`**\n"
            "ボイスチャットからボットを退出させます。\n\n"
            "**選択肢をランダムで選ぶ: `/choose 選択肢1 選択肢2 選択肢3 ...`**\n"
            "入力した選択肢の中からランダムで1つを選びます。\n\n"
            "**読み上げチャンネルを設定: `/set_channel`**\n"
            "現在のチャンネルをボットの読み上げ対象チャンネルとして設定します。\n\n"
            "**電卓機能: `/C`**\n"
            "入力した式を計算します。\n"
            "記号や数字は半角を使ってください。最後に＝はいりません。\n\n"
            "**注意:** \n"
            "ボットが読み上げるのは、`/set_channel`で指定されたチャンネルからのメッセージです。"
        )
        await interaction.response.send_message(description)

# -----------------------------------------------------------------------------
# Copyright (c) 2025 みらい@milie_usotsuki
#https://x.com/milie_usotsuki
# -----------------------------------------------------------------------------
