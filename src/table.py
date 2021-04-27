import os 
import discord 
import requests 
from bs4 import BeautifulSoup 

TABLE_URL = 'https://www.cricbuzz.com/cricket-series/3472/indian-premier-league-2021/points-table'

def table_func():
    embedVar_table = discord.Embed(title=" IPL Points Table", color=0xFFD700)

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
    for i in range(len(table_data)):
        desc = ""
        for j in range(len(table_data[i])):
            desc = desc + headers[j] + ' : ' + table_data[i][j] + '\n'
        embedVar_table.add_field(name = str(i+1) + '. ' + names[i] , value = desc, inline=False)
    
    embedVar_table.add_field( name = '\u200b' , value = "For more information, visit [criccbuzz]({})".format(TABLE_URL), inline=False)
        
    return embedVar_table