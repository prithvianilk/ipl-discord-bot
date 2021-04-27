import os
import discord
import score
import table
import orange
import purple
from dotenv import load_dotenv 

load_dotenv() 
URL = 'https://www.cricbuzz.com/'

TOKEN = os.environ['DISCORD_TOKEN']
PYTHON_ENV = os.environ['PYTHON_ENV'] # Can be 'dev' or 'prod'
PREFIX = '${}'.format('dev-' if PYTHON_ENV == 'dev' else '') # Must be added to every 'starts with' command case

client = discord.Client() 

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(PREFIX + 'help'):
        commands = [
            '`$score` - Gives live score of ongoing IPL match',
            '`$table` - Gives entire points table of the IPL season',
            '`$orange-cap` - Gives the current Orange Cap holder of the IPL season',
            '`$purple-cap` - Gives the current Purple Cap holder of the IPL season'
        ]

        embedVar_help = discord.Embed(title="Commands", color= 0xFFD700)
        embedVar_help.add_field(name="List of Commands\n", value = '\n\n'.join(commands), inline=False)
        await message.channel.send(embed=embedVar_help)

    if message.content.startswith(PREFIX + 'score'):
        await message.channel.send(embed=score.score_func())

    if message.content.startswith(PREFIX + 'table'):
       await message.channel.send(embed=table.table_func())

    if message.content.startswith(PREFIX + 'orange-cap'):
        orange.orange_func()
        await message.channel.send(embed=orange.orange_func())
    if message.content.startswith('$purple-cap'): 
        await message.channel.send(embed=purple.purple_func())

client.run(TOKEN)
