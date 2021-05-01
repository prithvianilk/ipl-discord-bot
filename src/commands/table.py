import discord 
import requests 
from bs4 import BeautifulSoup 
from PIL import Image
from io import BytesIO

TABLE_URL = 'https://www.cricbuzz.com/cricket-series/3472/indian-premier-league-2021/points-table'
def get_table(driver):
    driver.refresh()
    png = driver.get_screenshot_as_png() # saves screenshot of entire page
    im = Image.open(BytesIO(png)) # uses PIL library to open image in memory
    
    width, height = im.size
    # await message.channel.send(width, height)

    left = 0
    right = width - 80
    top = 0
    bottom = height + 50

    im1_cropped = im.crop((left, top, right, bottom))
    im1_cropped.save("table.png")
    # im.save("table.png")

    return 
