import discord
from discord.ext import commands
import json
import os

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
intents = discord.Intents.default()

# The bot
bot = commands.Bot(prefix, intents = intents)
bot.remove_command("help")

# intents
bot.intents.members = True
intents.members = True

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

bot.run(token)