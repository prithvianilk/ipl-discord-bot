import os 
import discord 
import requests 
from bs4 import BeautifulSoup 
from dotenv import load_dotenv 

load_dotenv() 
URL = 'https://www.cricbuzz.com/'
NEW_URL = "https://www.cricbuzz.com/cricket-series/3472/indian-premier-league-2021/stats"
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
        await message.channel.send(bat_team + '\n' + bat_score + '\n' + bowl_team + '\n' + bowl_score)

    if message.content.startswith('$orange cap'): 
        page_cap = requests.get(NEW_URL) 
        cap_soup = BeautifulSoup(page_cap.content, 'html.parser')
        stats_table = cap_soup.find('div', id = "seriesStatsTable")
        tbody = stats_table.find('tbody')
        tr = tbody.find('tr')
        orange_cap = tr.find(class_ = "cb-text-link").text
        tds = tr.find_all('td')
        tds = list(map(lambda x: x.text, tds))
        await message.channel.send(orange_cap + " with " + tds[4] + " runs")

client.run(TOKEN)
