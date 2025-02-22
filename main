import discord
import asyncio
from discord.ext import commands
from cogs.scheduler import SchedulerCog
from cogs.voice import VoiceCog
from cogs.finance import FinanceCog
from cogs.calculator import CalculatorCog
from cogs.utility import UtilityCog
from cogs.dice import DiceCog
from cogs.autojoin import AutoJoinVoice  # 新しいCogをインポート
import json

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# グローバルな変数
voice_client = None
read_channel_id = None
message_queue = asyncio.Queue()  # ここで定義します

@bot.event
async def on_ready():
    print(f'ログインしました: {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="/used で使い方表示"))

    # ✅ on_ready() 内で同期を実行
    try:
        await bot.tree.sync()
        print("スラッシュコマンドを同期しました。")
    except Exception as e:
        print(f"スラッシュコマンドの同期に失敗しました: {e}")

async def load_cogs():
    voice_cog = VoiceCog(bot, message_queue)  # VoiceCog をインスタンス化
    await bot.add_cog(voice_cog)
    await bot.add_cog(FinanceCog(bot))
    await bot.add_cog(CalculatorCog(bot))
    await bot.add_cog(UtilityCog(bot))
    await bot.add_cog(DiceCog(bot))
    await bot.add_cog(AutoJoinVoice(bot, voice_cog))  # AutoJoinVoice に VoiceCog を渡す
    await bot.add_cog(SchedulerCog(bot))
    await bot.load_extension("cogs.BombGame")  # 変更: 拡張としてロード

async def main():
    async with bot:
        await load_cogs()
        with open('token.json') as f:
            token_data = json.load(f)
        await bot.start(token_data['token'])

asyncio.run(main())

# -----------------------------------------------------------------------------
# Copyright (c) 2025 みらい@milie_usotsuki
#https://x.com/milie_usotsuki
# -----------------------------------------------------------------------------
