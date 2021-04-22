import os
import discord
from dotenv import load_dotenv

load_dotenv() 
TOKEN = os.environ['DISCORD_TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$score'):
        await message.channel.send('Score is your mom!')

client.run(TOKEN)
