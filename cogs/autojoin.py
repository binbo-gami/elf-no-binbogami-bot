import discord
from discord.ext import commands

class AutoJoinVoice(commands.Cog):
    def __init__(self, bot, voice_cog):
        self.bot = bot
        self.voice_client = None
        self.voice_cog = voice_cog

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:  # 他のBOTは無視
            return

        # ユーザーがボイスチャンネルに参加した場合
        if before.channel is None and after.channel is not None:
            channel = after.channel
            # ボイスチャンネルに他のメンバーがいない場合のみ参加
            if len(channel.members) == 1 and (self.voice_client is None or not self.voice_client.is_connected()):
                self.voice_client = await channel.connect()
                self.voice_cog.voice_client = self.voice_client  # VoiceCog の voice_client を更新
                print(f'{channel.name} に参加しました！')

        # ユーザーがボイスチャンネルから退出し、誰もいなくなった場合
        if before.channel is not None and after.channel is None:
            channel = before.channel
            # ボイスチャンネルに残ったのがBOTのみか確認
            if len(channel.members) == 1 and self.voice_client is not None:
                await self.voice_client.disconnect()
                self.voice_client = None
                self.voice_cog.voice_client = None  # VoiceCog の voice_client をリセット
                print(f'{channel.name} から退出しました！')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user}')

def setup(bot, voice_cog):
    bot.add_cog(AutoJoinVoice(bot, voice_cog))
