import discord
from discord.ext import commands
import asyncio
import pyttsx3
from discord import FFmpegPCMAudio

class VoiceCog(commands.Cog):
    def __init__(self, bot, message_queue):
        self.bot = bot
        self.message_queue = message_queue
        self.voice_client = None
        self.read_channel_id = None
        self.read_channel = None
        self.tts_engine = pyttsx3.init()
        self.running = True  # ループ制御用フラグ

        # 読み上げループ開始
        self.read_task = bot.loop.create_task(self.read_messages())

    async def read_messages(self):
        while self.running:
            if self.voice_client and self.voice_client.is_connected():
                print("読み上げループ開始")
                try:
                    message = await self.message_queue.get()
                    print(f"メッセージ取得: {message.content}")

                    # メッセージの内容を置き換え
                    content = message.content.replace("www", "わらわら").replace("ｗｗｗ", "わらわら").replace("うんこ","かんてん").replace("うんち","かんてん")

                    # メッセージとユーザー名をTTSで読み上げ
                    text_to_read = f"{message.author.display_name}さん {content}"
                    self.tts_engine.save_to_file(text_to_read, 'temp.mp3')
                    self.tts_engine.runAndWait()
                    print("TTSエンジンがメッセージを音声に変換")

                    audio_source = FFmpegPCMAudio('temp.mp3')
                    self.voice_client.play(audio_source, after=lambda e: print(f'Finished playing: {e}'))

                    # 読み上げが終了するまで待機
                    while self.voice_client.is_playing():
                        await asyncio.sleep(1)
                except asyncio.TimeoutError:
                    # タイムアウト処理（何もしない）
                    pass
    
            await asyncio.sleep(1)  # 短いスリープを追加してCPU使用率を下げる

    @discord.app_commands.command(name="join")
    async def join(self, interaction: discord.Interaction):
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            self.voice_client = await channel.connect()
            self.read_channel_id = interaction.channel.id
            await interaction.response.send_message(f'{channel.name} に参加しました！')
        else:
            await interaction.response.send_message('ボイスチャンネルに参加してからコマンドを実行してください。')

    @discord.app_commands.command(name="leave")
    async def leave(self, interaction: discord.Interaction):
        if self.voice_client and self.voice_client.is_connected():
            await self.voice_client.disconnect()
            self.running = False  # ループを停止
            await interaction.response.send_message('ボイスチャンネルから退出しました！')
        else:
            await interaction.response.send_message('現在、ボイスチャンネルに接続していません。')

    @discord.app_commands.command(name="setchannel", description="読み上げチャンネルを指定します")
    async def setchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        self.read_channel = channel
        self.read_channel_id = channel.id
        await interaction.response.send_message(f'読み上げチャンネルを {channel.name} に設定しました！')

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.read_channel_id and message.channel.id == self.read_channel_id and not message.author.bot:
            await self.message_queue.put(message)
            print(f"メッセージをキューに追加: {message.content}")
        elif self.voice_client and self.read_channel_id is None and not message.author.bot:
            self.read_channel_id = message.channel.id
            await self.message_queue.put(message)  # 最初のメッセージもキューに追加して読み上げる
            await message.channel.send(f'読み上げチャンネルが {message.channel.name} に設定されました！')
            print(f"読み上げチャンネルを設定: {message.channel.name}")

    def cog_unload(self):
        self.running = False  # ループを停止
        self.read_task.cancel()



# -----------------------------------------------------------------------------
# Copyright (c) 2025 みらい@milie_usotsuki
#https://x.com/milie_usotsuki
# -----------------------------------------------------------------------------