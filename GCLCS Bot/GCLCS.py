import discord
import random
import os
from discord.ext import commands, tasks

extensions = []

for filename in os.listdir('./cogs'):
   if filename.endswith('.py'):
       extensions += [filename[:-3]]

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = '!', intents=intents)
bot.remove_command("help")

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=862537818021429260)
    await member.add_roles(role)

@bot.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title = 'Commands', color=discord.Colour.dark_blue())

    embed.add_field(name = 'Join‎', value = 'Join the GCLCS queue to see who is looking to play', inline=True)
    embed.add_field(name = 'Randomize‎', value = 'Randomize the players currently in queue to make up teams (only works with 10 players)', inline=True)
    embed.add_field(name = '‎Roll', value = 'A randomly generated number between 1-100', inline=True)
    embed.add_field(name = 'Leave‎', value = 'Leave the GCLCS queue', inline=True)
    embed.add_field(name = 'Clear‎', value = 'Clear the queue entirely of players', inline=True)
    embed.add_field(name = '‎Predict', value = 'A random 8ball response (you must provide the bot a question)', inline=True)
    embed.add_field(name = '‎Queue', value = 'See all of the players currently in queue', inline=True)
    embed.add_field(name = 'Game', value = 'See details of the current game', inline=True)
    embed.add_field(name = '‎Stats', value = 'See stats for the current season', inline=True)

    embed.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)

    await ctx.send(embed = embed)

for x in range(0, len(extensions)):
    bot.load_extension(f'cogs.{extensions[x]}')

@bot.command(hidden=True)
async def load(ctx):
    for x in range(0, len(extensions)):
        bot.load_extension(f'cogs.{extensions[x]}')
    print(f'{extensions} has been loaded')
    
@bot.command(hidden=True)
async def unload(ctx):
    for x in range(0, len(extensions)):
        bot.unload_extension(f'cogs.{extensions[x]}')
    print(f'{extensions} has been unloaded')

@bot.command(hidden=True)
async def reload(ctx):
    for x in range(0, len(extensions)):
        bot.reload_extension(f'cogs.{extensions[x]}')
    print(f'{extensions} has been reloaded')

bot.run('ODYyMjQ4NTQwMzU3Mzk0NDYy.YOVlhw.GkbZCOIyjaXL4hoYUMbiEjGtGKY')