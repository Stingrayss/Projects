import discord
from discord.ext import commands
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import json
import os
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

extensions = []

# Get configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	prefix = data["prefix"]

class Greetings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		#self._last_member = None

# Intents
intents = discord.Intents.all()
intents.members = True

# The bot
bot = commands.Bot(prefix, intents = intents)
bot.remove_command("help")
bot.intents.members = True

# Load cogs
if __name__ == '__main__':
	for filename in os.listdir("Cogs"):
		if filename.endswith(".py"):
			extensions += [filename[:-3]]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    for x in range(0, len(extensions)):
        bot.load_extension(f'Cogs.{extensions[x]}')
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name =f"in the ocean"))

@bot.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title = 'Commands', color=discord.Colour.dark_blue())

    embed.add_field(name = 'Help', value = 'Undergoing Construction', inline=True)

    embed.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)

    await ctx.send(embed = embed)

@bot.command(hidden=True)
async def load(ctx):
    date = datetime.now(ZoneInfo("America/Los_Angeles"))
    for x in range(0, len(extensions)):
        bot.load_extension(f'Cogs.{extensions[x]}')
    print(f'{date}:DEBUG: {extensions} has been loaded')
    
@bot.command(hidden=True)
async def unload(ctx):
    date = datetime.now(ZoneInfo("America/Los_Angeles"))
    for x in range(0, len(extensions)):
        bot.unload_extension(f'Cogs.{extensions[x]}')
    print(f'{date}:DEBUG: {extensions} has been unloaded')

@bot.command(hidden=True)
async def reload(ctx):
    date = datetime.now(ZoneInfo("America/Los_Angeles"))
    for x in range(0, len(extensions)):
        bot.reload_extension(f'Cogs.{extensions[x]}')
    print(f'{date}:DEBUG: {extensions} has been reloaded')

@bot.command(hidden=True, aliases = ['l'])
async def logout(ctx):
    date = datetime.now(ZoneInfo("America/Los_Angeles"))
    print(f'{date}:INFO: {bot.user} is logging out')
    await bot.close()

bot.run(token)