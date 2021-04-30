import os
import discord
from commands import get_help, get_score, get_table, get_orange_cap, get_purple_cap
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from dotenv import load_dotenv 
load_dotenv() 

TOKEN = os.environ['DISCORD_TOKEN']
PYTHON_ENV = os.environ['PYTHON_ENV'] # Can be 'dev' or 'prod'
PREFIX = '${}'.format('dev-' if PYTHON_ENV == 'dev' else '') # Must be added to every 'starts with' command case

# to store these paths into heroku environment variables
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

# PATH = "{}chromedriver.exe".format('./' if PYTHON_ENV == 'prod' else 'C:\Program Files (x86)\\') 
# driver = webdriver.Chrome(PATH) 
driver.get("https://www.iplt20.com/points-table/men/2021") 
driver.maximize_window()
tag = driver.find_element_by_tag_name("body")

element = driver.find_element_by_id("main-content")
driver.execute_script("window.scrollTo(0, {})".format(element.location['y'] - 190))

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
        await message.channel.send(embed = get_score())

    if message.content.startswith(PREFIX + 'table'):
        get_table(driver)
        await message.channel.send(file=discord.File("table.png"))
        os.remove("table.png")

    if message.content.startswith(PREFIX + 'orange-cap'):
        await message.channel.send(embed = get_orange_cap())

    if message.content.startswith(PREFIX + 'purple-cap'): 
        await message.channel.send(embed = get_purple_cap())

client.run(TOKEN)
