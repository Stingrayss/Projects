import discord
import json
from datetime import datetime, timedelta
import random
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot


#initalize the cog
class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #commands
    @commands.command()
    async def users(self, ctx):
        client = discord.client
        for guild in client.guilds:
            for member in guild.members:
                print(member) # or do whatever you wish with the member detail

        #data['users'] = [f"name: {member.id}", "time: ", f"server: {discord.Guild}"]
        #json_data = json.dumps(data)
        #print(f'{json_data}')


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