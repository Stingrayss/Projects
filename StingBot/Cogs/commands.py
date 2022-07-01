from email.policy import default
import discord
from discord import Spotify
import json
from collections import defaultdict
import random
from discord.ext import commands

#initalize the cog
class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #This was the original command to grab all users and give them
    #base variables for data I wanted to track
    #Adding new variables will need a new command for appending
    #@commands.command(hidden=True)
    #@commands.has_permissions(administrator=True)
    #async def users(self, ctx):
        #user_list = defaultdict(list)
        #user = {}
        #for guild in self.bot.guilds:
            #for member in guild.members:
                #user = {"name": member.name, "messages": 0, "voice_join": 0, "voice_leave": 0, "last_session": 0, "time": 0, "server": f'{guild}'}
                #user_list[member.id].append(user)

        #out = open("data.json", "w")
        #json.dump(user_list, out, indent = 6)
        #out.close()

    @commands.command()
    async def predict(self, ctx, *, question):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        await ctx.send(random.choice(responses))

    @commands.command(aliases = ['prune', 'p'])
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, *, amount=1):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'messages have been deleted', delete_after = 2)

    @commands.command()
    async def roll(self, ctx):
        await ctx.send(random.randint(1, 100))

def setup(bot):
    bot.add_cog(Commands(bot))
