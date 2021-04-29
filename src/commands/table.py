import discord 
from PIL import Image
from io import BytesIO

def get_table(driver):

    driver.refresh()
    png = driver.get_screenshot_as_png() # saves screenshot of entire page
    im = Image.open(BytesIO(png)) # uses PIL library to open image in memory

    width, height = im.size

    left = 265
    right = width - 278
    top = height/2 - 185
    bottom = height - 200   

    im1_cropped = im.crop((left, top, right, bottom))
    im1_cropped.save("table.png")

    return 
    