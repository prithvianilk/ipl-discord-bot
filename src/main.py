import os
import time
import discord
from selenium import webdriver
from commands import get_help, get_score, get_table, get_orange_cap, get_purple_cap

# from dotenv import load_dotenv 
# load_dotenv() 

TOKEN = os.environ['DISCORD_TOKEN']
PYTHON_ENV = os.environ['PYTHON_ENV'] # Can be 'dev' or 'prod'
PREFIX = '${}'.format('dev-' if PYTHON_ENV == 'dev' else '') # Must be added to every 'starts with' command case

DRIVER_PATH = "./chromedriver"

score_driver = webdriver.Chrome(DRIVER_PATH)
score_driver.get("https://www.iplt20.com/")
score_driver.find_elements_by_class_name("btn--inverse")[1].click()

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
        await message.channel.send(embed = get_score(score_driver))

    if message.content.startswith(PREFIX + 'table'):
       await message.channel.send(embed = get_table())

    if message.content.startswith(PREFIX + 'orange-cap'):
        await message.channel.send(embed = get_orange_cap())

    if message.content.startswith(PREFIX + 'purple-cap'): 
        await message.channel.send(embed = get_purple_cap())

client.run(TOKEN)
