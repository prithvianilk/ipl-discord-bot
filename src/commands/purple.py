import discord 
import requests 
from bs4 import BeautifulSoup 

PCAPURL = "https://www.sportskeeda.com/go/ipl/purple-cap?ref=carousel"

def get_purple_cap():
    page_pcap = requests.get(PCAPURL) 
    soup_pcap = BeautifulSoup(page_pcap.content, 'html.parser')
    keeda_pcap = soup_pcap.find(class_ = "keeda_widget")
    tr_pcap = keeda_pcap.find_all('tr')
   
    tds_pcap = [[0]] * 6

    for i in range(1, 6):
        tds_pcap[i] = tr_pcap[i].find_all('td')
        tds_pcap[i] = list(map(lambda x: x.text, tds_pcap[i]))

    embedVar_pcap = discord.Embed(title=" Purple Cap", color=0x8A2BE2)
        
    for i in range(1, 6):
        pcap_stats = " Wickets : " + tds_pcap[i][6].replace('\n', '') + "\nMatches : " + tds_pcap[i][4].replace('\n', '') + "\nInnings : " + tds_pcap[i][5].replace('\n', '') 
        embedVar_pcap.add_field(name = str(i) + '. '+ tds_pcap[i][1].replace('\n', '') , value = tds_pcap[i][2].replace('\n', '') + '\n' + pcap_stats, inline=False)
        
    embedVar_pcap.add_field(name = '\u200b' , value = "\nFor more information, visit [sportskeeda]({})".format(PCAPURL), inline=False) 
        
    return embedVar_pcap