import discord 
import requests 
from bs4 import BeautifulSoup 

OCAPURL = 'https://www.sportskeeda.com/go/ipl/orange-cap?ref=carousel'

def get_orange_cap():
    page_ocap = requests.get(OCAPURL) 
    soup_ocap = BeautifulSoup(page_ocap.content, 'html.parser')
    keeda_ocap = soup_ocap.find(class_ = "keeda_widget")
    tr_ocap = keeda_ocap.find_all('tr')

    tds_ocap = [[0]] * 6

    for i in range(1, 6):
        tds_ocap[i] = tr_ocap[i].find_all('td')
        tds_ocap[i] = list(map(lambda x: x.text, tds_ocap[i]))

    embedVar_ocap = discord.Embed(title=" Orange Cap", color=0xFF8C00)

    for i in range(1, 6):
        ocap_stats = "Matches : " + tds_ocap[i][4].replace('\n', '') + "\nInnings : " + tds_ocap[i][5].replace('\n', '') 
        embedVar_ocap.add_field(name = str(i) + '. ' + tds_ocap[i][1].replace('\n', '') + " : " + tds_ocap[i][6].replace('\n', '') + " runs", value = tds_ocap[i][2].replace('\n', '') + '\n' + ocap_stats, inline=False)
        
    embedVar_ocap.add_field( name = '\u200b' , value = "\nFor more information, visit [sportskeeda]({})".format(OCAPURL), inline=False)

    return embedVar_ocap