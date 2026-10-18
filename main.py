import os
import discord
from flask import Flask
from threading import Thread

# 1. Discord Botの準備
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == '!ping':
        await message.channel.send('Pong!')

# 2. Renderスリープ対策用の簡易Webサーバー (Flask)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    # Renderが割り当てるポート番号（環境変数 PORT）を使用する
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 3. 起動処理
if __name__ == "__main__":
    # Webサーバーを別スレッドで起動
    keep_alive()
    # Discord Botを起動（環境変数からトークンを取得）
    TOKEN = os.environ.get("DISCORD_TOKEN")
    client.run(TOKEN)
