#!/usr/bin/env python3
"""
    A script to monitor folders and subdirectories for file movement, creation
    or modification so that files are automatically converted from predefined
    filetypes to target filetypes set by the user.

    Zamzar API keys can be obtained by registering at: https://developers.zamzar.com/pricing
"""

# Imports
import discord                                          #import libraries
from discord.ext import commands
from discord.ext.commands import bot
import time
import json
from Watch import Watch
import os
import sys
import asyncio
import datetime as dt
import uuid
import requests
import shutil
from requests import Response


client = commands.Bot(command_prefix="+")  
config_file = open('hotfolders_config.json', 'r')
config_info = json.load(config_file)
api_key = config_info['api_key'][0]
config_info = config_info["conversions"]


# This will hold the watch objects for the paths
watch_list = []

for key in config_info:
    # Check the path exists, if not, skip it with an error message in the log
    if not os.path.exists(key):
        print("ERROR: " + key + " does not exist - cannot monitor\n")
        sys.exit(0)
    else:
        print("Monitoring: " + key)
        # Each key is a directory path.
        watch_list.append(Watch(key, config_info[key]['to'], config_info[key]['from'], config_info[key]['options'],
                            config_info[key]['ignore'], api_key))

@client.event                                           #message connect!
async def on_ready():
    print("Bot is ready")

@client.command()                                       # wide command and processing 
async def convert(ctx):

    try:
        url = ctx.message.attachments[0].url            # check for an image, call exception if none found
    except IndexError:
        print("Error: No attachments")
        await ctx.send("No attachments detected!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   # look to see if url is from discord
            r = requests.get(url, stream=True)
            imageName = 'fullsized_image' + '.png'      # save image to wide
            with open(imageName, 'wb') as out_file:
                print('Saving image: ' + imageName)
                shutil.copyfileobj(r.raw, out_file)
                time.sleep(15)                          # Sleep for 15 seconds 
                await ctx.send('In .gif', file=discord.File('fullsized_image.gif')) # send image in server discord
                time.sleep(5)                          # Sleep for 5 seconds 
                os.remove("fullsized_image.gif")       # Destroy file to no-loop program
                





    

client.run('ODM3MDA5ODA2MDUyNTU2ODYw.YImUIA.pi0XJ8twTi5Zlbva8zhQeSo5zS8')
