import os 
import discord 
import requests 
from tabulate import tabulate
from bs4 import BeautifulSoup 
from dotenv import load_dotenv 

load_dotenv() 
URL = 'https://www.cricbuzz.com/'
TABLE_URL = 'https://www.cricbuzz.com/cricket-series/3472/indian-premier-league-2021/points-table'
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

    if message.content.startswith('$table'):
        page = requests.get(TABLE_URL) 
        soup = BeautifulSoup(page.content, 'html.parser')
        tbody = soup.find('tbody')
        headers = list(map(lambda x: x.text, soup.find_all(class_ = 'cb-srs-pnts-th')))[1:]
        trs = tbody.find_all('tr')
        table_data = []
        for tr in trs:
            tds = list(map(lambda x: x.text, tr.find_all(class_ = 'cb-srs-pnts-td')))
            if len(tds) != 0:
                table_data.append(tds)
        names = list(map(lambda x: x.find('a').text, soup.find_all(class_ = 'cb-srs-pnts-name')))
        msg_txt = ""
        for i in range(len(table_data)):
            msg_txt = msg_txt + '-> ' + names[i] + '\n'
            desc = ""
            for j in range(len(table_data[i])):
                desc = desc + headers[j] + ' : ' + table_data[i][j] + '\n'
            msg_txt += desc
        await message.channel.send(msg_txt)


client.run(TOKEN)
