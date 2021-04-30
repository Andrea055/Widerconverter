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
from fpdf import FPDF
import docx2txt



def set_dll_search_path():
   # Python 3.8 no longer searches for DLLs in PATH, so we have to add
   # everything in PATH manually. Note that unlike PATH add_dll_directory
   # has no defined order, so if there are two cairo DLLs in PATH we
   # might get a random one.
   if os.name != "nt" or not hasattr(os, "add_dll_directory"):
       return
   for p in os.environ.get("PATH", "").split(os.pathsep):
       try:
           os.add_dll_directory(p)
       except OSError:
           pass


set_dll_search_path()

import cairosvg

client = commands.Bot(command_prefix=".")  
config_file = open('hotfolders_config.json', 'r')
config_info = json.load(config_file)
api_key = config_info['api_key'][0]
config_info = config_info["conversions"]
pdf = FPDF()   


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
async def converttxt(ctx):

    try:
        url = ctx.message.attachments[0].url            # check for an image, call exception if none found
    except IndexError:
        print("Error: No attachments")
        await ctx.send("No attachments detected!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   # look to see if url is from discord
            r = requests.get(url, stream=True)
            open('url', 'wb').write(r.content)
            os.rename(r'E:\BOT\bot-env\zamzar-samples-hotfolders-master\src\url',r'E:\BOT\bot-env\zamzar-samples-hotfolders-master\src\url.txt')
            pdf.add_page()
            pdf.set_font("Arial", size = 15)
            f = open("url.txt", "r")
            for x in f:
                pdf.cell(200, 10, txt = x, ln = 1, align = 'C')
                pdf.output("url.pdf")  
            await ctx.send('I have a PDF for you!' , file=discord.File('url.pdf'))
            time.sleep(5)
            os.remove("url.pdf")
            os.remove("url.txt")

@client.command()                                       # wide command and processing 
async def imagetogif(ctx):
    try:
        url = ctx.message.attachments[0].url            # check for an image, call exception if none found
    except IndexError:
        print("Error: No attachments")
        await ctx.send("No attachments detected!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   # look to see if url is from discord
            r = requests.get(url, stream=True)
            open('url', 'wb').write(r.content)
            os.rename(r'E:\BOT\bot-env\zamzar-samples-hotfolders-master\src\url',r'E:\BOT\bot-env\zamzar-samples-hotfolders-master\src\url.png')
            time.sleep(25)
            await ctx.send('Gif', file=discord.File('url.gif'))
            time.sleep(3)
            os.remove('url.gif')

@client.command()
async def convertdocx(ctx):
    try:
        url = ctx.message.attachments[0].url            # check for an image, call exception if none found
    except IndexError:
        print("Error: No attachments")
        await ctx.send("No attachments detected!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   # look to see if url is from discord
            r = requests.get(url, stream=True)
            open('url', 'wb').write(r.content)
            os.rename(r'E:\BOT\bot-env\zamzar-samples-hotfolders-master\src\url',r'E:\BOT\bot-env\zamzar-samples-hotfolders-master\src\url.docx')
            MY_TEXT = docx2txt.process("url.docx")
            with open("Output.txt", "w") as text_file:
                print(MY_TEXT, file=text_file)
            time.sleep(15)
            await ctx.send('TXT', file=discord.File('Output.txt'))
            time.sleep(3)
            os.remove('Output.txt')
            os.remove('url.docx')
                
@client.command()
async def test(ctx):
    attachment_url = ctx.message.attachments[0].url
    file_request = requests.get(attachment_url)
    attachment.save()

@client.command()
async def svg2png(ctx):
    try:
        url = ctx.message.attachments[0].url            # check for an image, call exception if none found
    except IndexError:
        print("Error: No attachments")
        await ctx.send("No attachments detected!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   # look to see if url is from discord
            r = requests.get(url, stream=True)
            open('url', 'wb').write(r.content)
            os.rename(r'E:\BOT\bot-env\zamzar-samples-hotfolders-master\src\url',r'E:\BOT\bot-env\zamzar-samples-hotfolders-master\src\url.svg')
            cairosvg.svg2png(
                url="url.svg", write_to="output.png")
            await ctx.send('PNG for you!', file=discord.File('output.png'))
            time.sleep(3)
            os.remove('output.png')
            os.remove('url.svg')

@client.command()
async def svg2pdf(ctx):
    try:
        url = ctx.message.attachments[0].url            # check for an image, call exception if none found
    except IndexError:
        print("Error: No attachments")
        await ctx.send("No attachments detected!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   # look to see if url is from discord
            r = requests.get(url, stream=True)
            open('url', 'wb').write(r.content)
            os.rename(r'E:\BOT\bot-env\zamzar-samples-hotfolders-master\src\url',r'E:\BOT\bot-env\zamzar-samples-hotfolders-master\src\url.svg')
            cairosvg.svg2pdf(
                file_obj=open("url.svg", "rb"), write_to="output.pdf")
            await ctx.send('PDF for you!', file=discord.File('output.pdf'))
            time.sleep(3)
            os.remove('output.pdf')
            os.remove('url.svg')



    

client.run('TOKEN')
