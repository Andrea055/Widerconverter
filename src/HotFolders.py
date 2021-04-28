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
                shutil.copyfileobj(r.raw, out_file)     # save image from discord server
                




@client.command()                                       # wide command and processing 
async def process(ctx):
    print("Starting HotFolders.py")                         # Load the config file
    try:
        config_file = open('hotfolders_config.json', 'r')
    except FileNotFoundError as err:
        print("ERROR: Could not find JSON config file - ensure current working directory contains hotfolders_config.json")
    sys.exit(0)
    try:
        config_info = json.load(config_file)
        api_key = config_info['api_key'][0]
        config_info = config_info["conversions"]
    except json.decoder.JSONDecodeError as err:
        print("ERROR: Could not parse 'hotfolders_config.json' - invalid JSON found:")
        print(err)
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
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        for w in watch_list:
            del w
    await ctx.send('Wide!', file=discord.File('convert.png'))
    

client.run('TOKEN')
