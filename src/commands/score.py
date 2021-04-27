import discord 
import requests 
from bs4 import BeautifulSoup 

TEAMS = ['RCB', 'CSK', 'PBKS', 'MI', 'DC', 'KKR', 'SRH', 'RR']
LIVE_SCORES_URL = 'https://www.cricbuzz.com/cricket-match/live-scores'


def get_no_match_message():
    embedVar_score = discord.Embed(title=" IPL Score", color=0x223577)
    embedVar_score.add_field(name = 'No ongoing IPL match', value =  "For more information, visit [criccbuzz]({})".format(LIVE_SCORES_URL), inline=False)
    return embedVar_score

def get_score():
    page = requests.get(LIVE_SCORES_URL) 
    soup = BeautifulSoup(page.content, 'html.parser')

    rank_tabs_nav = soup.find(class_ = 'cb-rank-tabs').find('nav')
    if rank_tabs_nav == None:
        return get_no_match_message()

    live_scores = list(map(lambda x: x.text, rank_tabs_nav.find_all('a')))
    if live_scores[0] == 'International' or live_scores[0] == 'Domestic':
        return get_no_match_message()
            
    summary = soup.find(class_ = 'text-hvr-underline').text[: - 1]
    bowl = soup.find(class_ = 'cb-hmscg-bwl-txt') 
    bowl_team = bowl.find(class_ = 'cb-hmscg-tm-nm').text 
    bowl_score = bowl.find(style = 'display:inline-block; width:140px').text 
    bat = soup.find(class_ = 'cb-hmscg-bat-txt') 
    bat_team = bat.find(class_ = 'cb-hmscg-tm-nm').text 
    bat_score = bat.find(style = 'display:inline-block; width:140px').text 

    preview = soup.find(class_ = 'cb-text-preview')
    live = soup.find(class_ = 'cb-text-live')
    complete = soup.find(class_ = 'cb-text-complete')

    if preview != None:
        embedVar_score = discord.Embed(title=" IPL Score", color=0x223577)
        embedVar_score.add_field(name = summary, value = preview.text + "\n\nFor more information, visit [criccbuzz]({})".format(LIVE_SCORES_URL), inline=False)
        return embedVar_score
        
    desc = live if live != None else complete
        
    message_list = [bat_team, bat_score, bowl_team, bowl_score, desc.text]
    message_text = '\n'.join(message_list)

    embedVar_score = discord.Embed(title=" IPL Score", color=0x223577)
    embedVar_score.add_field(name = score_list[0], value = score_list[1] + "\n\nFor more information, visit [criccbuzz]({})".format(LIVE_SCORES_URL), inline=False)
        
    return embedVar_score