import discord
from discord import Spotify
from discord.ext import commands
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
		self._last_member = None

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
    for x in range(0, len(extensions)):
        bot.load_extension(f'Cogs.{extensions[x]}')
    print(f'{extensions} has been loaded')
    
@bot.command(hidden=True)
async def unload(ctx):
    for x in range(0, len(extensions)):
        bot.unload_extension(f'Cogs.{extensions[x]}')
    print(f'{extensions} has been unloaded')

@bot.command(hidden=True)
async def reload(ctx):
    for x in range(0, len(extensions)):
        bot.reload_extension(f'Cogs.{extensions[x]}')
    print(f'{extensions} has been reloaded')

@bot.command(hidden=True, aliases = ['l'])
async def logout(ctx):
    print(f'{bot.user} is logging out')
    await bot.close()

@bot.command(aliases = ['s'])
async def spotify(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
        pass
    if user.activities:
        for activity in user.activities:
            if isinstance(activity, Spotify):
                embed = discord.Embed(title = f"{user.name}'s Spotify", description = "Listening to{}".format(activity.title), color = 0xC902FF)
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Artist", value=activity.artist)
                embed.add_field(name="Album", value=activity.album)
                embed.set_footer(text="Song started at {}".format(activity.created_at.strftime("%H:%M")))
                await ctx.send(embed=embed)

bot.run(token)