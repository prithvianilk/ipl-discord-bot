import os
import time
import discord
from commands import get_help, get_score, get_table, get_orange_cap, get_purple_cap, get_toggle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# from dotenv import load_dotenv 
# load_dotenv() 

test = 0
TOKEN = os.environ['DISCORD_TOKEN']
PYTHON_ENV = os.environ['PYTHON_ENV'] # Can be 'dev' or 'prod'
PREFIX = '${}'.format('dev-' if PYTHON_ENV == 'dev' else '') # Must be added to every 'starts with' command case

# to store these paths into heroku environment variables
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver1 = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
# driver2 = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
# driver3 = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
driver4 = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

# PATH = "{}chromedriver.exe".format('./' if PYTHON_ENV == 'prod' else 'C:\Program Files (x86)\\') 
# driver1 = webdriver.Chrome(PATH) 
# driver2 = webdriver.Chrome(PATH) 
# driver3 = webdriver.Chrome(PATH) 
# driver4 = webdriver.Chrome(PATH)

driver1.get("https://www.iplt20.com/points-table/men/2021") 
driver1.maximize_window()
tag = driver1.find_element_by_tag_name("body")
element = driver1.find_element_by_id("main-content")
driver1.execute_script("window.scrollTo(0, {})".format(element.location['y'] - 190))

# driver2.get("https://www.iplt20.com/")
# driver2.maximize_window()
# time.sleep(5)
# scorecard_1 = driver2.find_element_by_class_name("homePageTakeover__button--data-only")
# scorecard_1.click()
# time.sleep(1)
# teams_1 = driver2.find_element_by_link_text("Teams")
# teams_1.click()
# element_squad1 = driver2.find_element_by_class_name("teamTabs")
# driver2.execute_script("window.scrollTo(0, {})".format(element_squad1.location['y'] - 50))

# driver3.get("https://www.iplt20.com/")
# driver3.maximize_window()
# time.sleep(5)
# scorecard = driver3.find_element_by_class_name("homePageTakeover__button--data-only")
# scorecard.click()
# time.sleep(1)
# teams = driver3.find_element_by_link_text("Teams")
# teams.click()
# team_2 = driver3.find_element_by_class_name("teamNav")
# team_2.find_elements_by_tag_name("a")[-1].click()
# element_squad2 = driver3.find_element_by_class_name("teamTabs")
# driver3.execute_script("window.scrollTo(0, {})".format(element_squad2.location['y'] - 50))

driver4.get("https://www.iplt20.com/")
driver4.maximize_window()
time.sleep(1)
scorecard4 = driver4.find_element_by_class_name("homePageTakeover__button--data-only")
scorecard4.click()

client = discord.Client() 

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(PREFIX + 'help'):
        await message.channel.send(embed = get_help())

    if message.content.startswith(PREFIX + 'score'):
        await message.channel.send(embed = get_score(driver4))

    if message.content.startswith(PREFIX + 'table'):
        get_table(driver1)
        await message.channel.send(file=discord.File("table.png"))
        os.remove("table.png")

    # if message.content.startswith(PREFIX + 'squad'):
    #     get_squad1(driver2)
    #     get_squad2(driver3)
    #     await message.channel.send(file=discord.File("squad1.png"))
    #     await message.channel.send(file=discord.File("squad2.png"))
    #     os.remove("squad1.png")
    #     os.remove("squad2.png")

    if message.content.startswith(PREFIX + 'orange-cap'):
        await message.channel.send(embed = get_orange_cap())

    if message.content.startswith(PREFIX + 'purple-cap'): 
        await message.channel.send(embed = get_purple_cap())


client.run(TOKEN)
