import discord 
import requests 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from PIL import Image
from io import BytesIO

def get_squad2(driver): 
    # driver.refresh()

    png1 = driver.get_screenshot_as_png()
    squad1 = Image.open(BytesIO(png1))

    width, height = squad1.size
    left = 0
    top = height/2
    right = width - 25
    bottom = height

    im1_cropped = squad1.crop((left, top, right, bottom))
    im1_cropped.save("squad2.png")

    return
