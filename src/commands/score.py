import discord 
import requests 
from bs4 import BeautifulSoup 

def get_details(team):
    detail_names = ["teamFull", "runs", "runRate", "overs"]
    return list(map(lambda x: team.find_element_by_class_name(x).text, detail_names))

def get_batsmen(driver):
    teamScore = driver.find_element_by_class_name("teamScorecard")
    batsmen_wrapper, _, bowlers_wrapper = teamScore.find_elements_by_class_name("wrapper")
    batsmen_tr = batsmen_wrapper.find_elements_by_tag_name("tr")
    batsmen = []
    for tr in batsmen_tr:
        tds = tr.find_elements_by_class_name("dismissal")
        if len(tds) != 0 and tds[0].text == "NOT OUT":
            player = tr.find_element_by_class_name("player").text
            runs = tr.find_element_by_class_name("runs").text
            balls = tr.find_element_by_class_name("balls").text
            batsmen.append("{}: {} runs from {} balls".format(player, runs, balls))
    return batsmen


def get_score(driver):
    home_team_details, away_team_details = list(map(get_details, driver.find_elements_by_class_name("team-details")))
    summary = home_team_details[0] + " vs " + away_team_details[0] + "\n" + driver.find_element_by_class_name("summary").text
    batsman_message = "Batsmen: " + "\n" + "\n".join(get_batsmen(driver))
    message_text = "\n".join(home_team_details) + "\n" + "\n".join(away_team_details) + "\n\n" + batsman_message + "\n"
    embed_score = discord.Embed(title = "IPL Score", color = 0x223577)
    embed_score.add_field(name = summary, value = message_text, inline = False)
    return embed_score
