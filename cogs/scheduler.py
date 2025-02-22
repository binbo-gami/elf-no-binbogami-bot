import discord
from discord.ext import commands, tasks
import aiohttp
import datetime
import asyncio

class SchedulerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1342871275076325588  # メッセージを送信するチャンネルIDに置き換えてください
        self.start_date = datetime.datetime(2025, 2, 25, 6, 0, 0)  # パニガルム更新の開始日
        self.weekly_task.start()
        self.panigalum_task.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'SchedulerCog: Logged in as {self.bot.user}')

    @tasks.loop(hours=168)  # 7日間ごとに実行（日曜日）
    async def weekly_task(self):
        if self.channel_id:
            channel = self.bot.get_channel(self.channel_id)
            if channel:
                await channel.send("週課更新だぞ！みんなやろうね！")

    @weekly_task.before_loop
    async def before_weekly_task(self):
        await self.bot.wait_until_ready()
        now = datetime.datetime.now()
        next_sunday = now + datetime.timedelta((6 - now.weekday()) % 7)  # 次の日曜日を計算
        next_run = next_sunday.replace(hour=6, minute=0, second=0, microsecond=0)
        wait_time = (next_run - now).total_seconds()
        print(f"週課スケジューラーが {wait_time} 秒後に開始します。")
        await asyncio.sleep(wait_time)

    @tasks.loop(hours=72)  # 3日間ごとに実行
    async def panigalum_task(self):
        if self.channel_id:
            channel = self.bot.get_channel(self.channel_id)
            if channel:
                await channel.send("今日はパニガルム更新だぞ！")

    @panigalum_task.before_loop
    async def before_panigalum_task(self):
        await self.bot.wait_until_ready()
        now = datetime.datetime.now()
        if now > self.start_date:
            delta_days = (now - self.start_date).days
            days_until_next_run = 3 - (delta_days % 3)
            next_run = now + datetime.timedelta(days=days_until_next_run)
        else:
            next_run = self.start_date
        next_run = next_run.replace(hour=6, minute=0, second=0, microsecond=0)
        wait_time = (next_run - now).total_seconds()
        print(f"パニガルムスケジューラーが {wait_time} 秒後に開始します。")
        await asyncio.sleep(wait_time)

def setup(bot):
    bot.add_cog(SchedulerCog(bot))
