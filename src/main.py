import os 
import discord 
import requests 
from bs4 import BeautifulSoup 
from dotenv import load_dotenv 

load_dotenv() 
URL = 'https://www.cricbuzz.com/'
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
        page = requests.get(URL) 
        soup = BeautifulSoup(page.content, 'html.parser')
        bowl = soup.find(class_ = 'cb-hmscg-bwl-txt') 
        bowl_team = bowl.find(class_ = 'cb-hmscg-tm-nm').text 
        bowl_score = bowl.find(style = 'display:inline-block; width:140px').text 
        bat = soup.find(class_ = 'cb-hmscg-bat-txt') 
        bat_team = bat.find(class_ = 'cb-hmscg-tm-nm').text 
        bat_score = bat.find(style = 'display:inline-block; width:140px').text 
        summary = soup.find(class_ = 'cb-text-complete').text
        title = bat_team + ' vs ' + bowl_team 
        await message.channel.send(
            title + '\n' + 
            summary + '\n' +
            (len(summary) * '-') + '\n' + 
            bat_team + '\n' + 
            bat_score + '\n' + 
            bowl_team + '\n' + 
            bowl_score + '\n' + 
            (len(summary) * '-') 
        )


client.run(TOKEN)
