import discord
from discord import Spotify
import json
import random
from discord.ext import commands

#initalize the cog
class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #commands
    @commands.command(hidden=True)
    async def users(self, ctx):
        user_list = {}
        user = {}
        user_guilds = []
        #cannot figure out how to keep same member.id with different guilds, maybe append?
        #trying to just have one id store all guilds shared for now
        for guild in self.bot.guilds:
            for member in guild.members:
                user_guilds = member.mutual_guilds
                print(user_guilds)
                user = {"name": member.name, "time": 0, "servers": f'{user_guilds}'}
                user_list[member.id] = user

        out = open("data.json", "w")
        json.dump(user_list, out, indent = 6)
        out.close()


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
