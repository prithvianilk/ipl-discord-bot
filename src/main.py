import os 
import discord 
import requests 
from bs4 import BeautifulSoup 
# from dotenv import load_dotenv 

# load_dotenv() 
URL = 'https://www.cricbuzz.com/'
LIVE_SCORES_URL = 'https://www.cricbuzz.com/cricket-match/live-scores'
OCAPURL = "https://www.cricbuzz.com/cricket-series/3472/indian-premier-league-2021/stats"
PCAPURL = "https://www.sportskeeda.com/go/ipl/purple-cap?ref=carousel"
TABLE_URL = 'https://www.cricbuzz.com/cricket-series/3472/indian-premier-league-2021/points-table'
STATS_URL = 'https://www.cricbuzz.com/cricket-series/3472/indian-premier-league-2021/stats'

TOKEN = os.environ['DISCORD_TOKEN']

client = discord.Client() 

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return  

    if message.content.startswith('$help'):
        commands = [
            '`$score` - Gives live score of ongoing IPL match\n',
            '`$table` - Gives entire points table of the IPL season\n',
            '`$orange-cap` - Gives the current Orange Cap holder of the IPL season\n',
            '`$purple-cap` - Gives the current Purple Cap holder of the IPL season\n'
        ]

        embedVar_help = discord.Embed(title="Commands", color= 0xFFD700)
        embedVar_help.add_field(name="List of Commands\n", value = '\n'.join(commands), inline=False)
        await message.channel.send(embed=embedVar_help)

    if message.content.startswith('$score'): 
        page = requests.get(LIVE_SCORES_URL) 
        soup = BeautifulSoup(page.content, 'html.parser')
        live_scores = list(map(lambda x: x.text, soup.find(class_ = 'cb-rank-tabs').find('nav').find_all('a')))
        if live_scores[0] == 'International' or live_scores[0] == 'Domestic':
            await message.channel.send('No ongoing IPL match')
            return 
        summary = soup.find(class_ = 'text-hvr-underline').text[: - 1]
        bowl = soup.find(class_ = 'cb-hmscg-bwl-txt') 
        bowl_team = bowl.find(class_ = 'cb-hmscg-tm-nm').text 
        bowl_score = bowl.find(style = 'display:inline-block; width:140px').text 
        bat = soup.find(class_ = 'cb-hmscg-bat-txt') 
        bat_team = bat.find(class_ = 'cb-hmscg-tm-nm').text 
        bat_score = bat.find(style = 'display:inline-block; width:140px').text 
        desc = soup.find(class_ = 'cb-text-complete').text
        message_list = [bat_team, bat_score, bowl_team, bowl_score, desc]
        message_text = '\n'.join(message_list)

        embedVar_score = discord.Embed(title=" IPL Score", color=0xFFD700)
        embedVar_score.add_field(name = summary, value = message_text + "\n\n For more information, visit [criccbuzz]({})".format(LIVE_SCORES_URL), inline=False)
        await message.channel.send(embed=embedVar_score)

    if message.content.startswith('$table'):
        
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
        msg_txt = ""
        for i in range(len(table_data)):
            msg_txt = msg_txt + str(i+1) + '. ' + names[i] + '\n'
            desc = ""
            for j in range(len(table_data[i])):
                desc = desc + headers[j] + ' : ' + table_data[i][j] + '\n'
            msg_txt += desc
            embedVar_table.add_field(name = str(i+1) + '. ' + names[i] , value = desc, inline=False)
           
        embedVar_table.add_field( name = '\u200b' , value = "For more information, visit [criccbuzz]({})".format(TABLE_URL), inline=False)
        await message.channel.send(embed=embedVar_table)

    if message.content.startswith('$orange-cap'): 
        page_cap = requests.get(OCAPURL) 
        cap_soup = BeautifulSoup(page_cap.content, 'html.parser')
        stats_table = cap_soup.find('div', id = "seriesStatsTable")
        tbody = stats_table.find('tbody')
        tr = tbody.find('tr')
        orange_cap = tr.find(class_ = "cb-text-link").text
        tds = tr.find_all('td')
        tds = list(map(lambda x: x.text, tds))

        embedVar_ocap = discord.Embed(title=" Orange Cap", color=0xFFA500)
        embedVar_ocap.add_field(name = orange_cap , value = " Runs : " + tds[4] + "\n\n For more information, visit [criccbuzz]({})".format(STATS_URL), inline=False)
        await message.channel.send(embed=embedVar_ocap)

    if message.content.startswith('$purple-cap'): 
        page_pcap = requests.get(PCAPURL) 
        soup_pcap = BeautifulSoup(page_pcap.content, 'html.parser')
        keeda_pcap = soup_pcap.find(class_ = "keeda_widget")
        tr_pcap = keeda_pcap.find_all('tr')[1]
        tds_pcap = tr_pcap.find_all('td')
        tds_pcap = list(map(lambda x: x.text, tds_pcap))

        embedVar_pcap = discord.Embed(title=" Purple Cap", color=0x8A2BE2)
        embedVar_pcap.add_field(name = tds_pcap[1].replace('\n', '') , value = " Wickets : " + tds_pcap[6].replace('\n', '') + "\n\n For more information, visit [criccbuzz]({})".format(STATS_URL), inline=False)
        await message.channel.send(embed=embedVar_pcap)

        
client.run(TOKEN)