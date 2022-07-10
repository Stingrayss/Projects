from typing import OrderedDict
import discord
import random
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import json
from discord.ext import commands

#only need for users command
#from collections import defaultdict

def read_json():
    with open('data.json', 'r') as data: 
        users = json.load(data)
        return users

def write_json(users):
    with open('data.json', 'w') as data:
        json.dump(users, data, indent = 4)

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
        #server_list = defaultdict(dict)
        #user = {}
        #for guild in self.bot.guilds:
            #for member in guild.members:
                #user = {"server": guild.name, "name": member.name, "tracking": True, "inactive": 0, "messages": 0, "time": 0, "last_session": 0, "voice_join": 0, "voice_leave": 0}
                #server_list[guild.id][member.id] = user

        #out = open("data2.json", "w")
        #json.dump(server_list, out, indent = 4)
        #out.close()

        #THIS CODE IS UGLY BUT WORKS, ONLY NEEDED TO TRANSFER DATA

        #users = read_json()

        #with open('data2.json', 'r') as data2: 
            #users_data2 = json.load(data2)

            #for guild in users_data2:
                #user_list = users_data2[guild]
                #for key in user_list:
                    #users_data2[guild][key]['time'] = users[guild][key]['time']
                    #users_data2[guild][key]['messages'] = users[guild][key]['messages']
                    #users_data2[guild][key]['last_session'] = users[guild][key]['last_session']
                    #users_data2[guild][key]['voice_join'] = users[guild][key]['voice_join']
                    #users_data2[guild][key]['voice_leave'] = users[guild][key]['voice_leave']

            #with open('data2.json', 'w') as data:
                #json.dump(users_data2, data, indent = 4)

    @commands.command(hidden=True)
    async def leaderboard(self, ctx):
        topten = []
        data = read_json()
        for key in data[str(ctx.guild.id)]:
            user = data[str(ctx.guild.id)][key]
            if len(topten) < 10:
                tuple = user["name"], user["time"]
                topten.append(tuple)
            else:
                topten.sort(key=lambda x : x[1], reverse = True)
                if user["time"] > topten[-1][1]:
                    tuple = user["name"], user["time"]
                    topten[-1] = tuple

        topten.sort(key=lambda x : x[1], reverse = True)

        #MAKE THIS LOOK PRETTY AT SOME POINT
        users = ''
        for i in range (0, len(topten)): 
            users += f'{i + 1}. {topten[i][0]}: {round(topten[i][1], 1) } minutes\n\n'
        embed = discord.Embed(title = 'Voice Leaderboard', color=discord.Colour.dark_blue())
        embed.add_field(name = f'Top 10:', value=users)
        await ctx.send(embed = embed)
                  
    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def data(self, ctx):
        date = datetime.now(ZoneInfo("America/Los_Angeles"))
        if(ctx.author.id == 105032801715290112):
            file = open('data.json', 'r')
            json_data = json.load(file)
            file.close()
            #not sure how this orders the data, but it was the best I could do
            #I don't think ordering by name values is possible
            json_data = OrderedDict(sorted(json_data.items(), key=lambda k: k[0][1]))

            file = open('data.json', 'w')
            json.dump(json_data, file, indent = 4)
            file.close()
            
            await self.bot.get_channel(734204331552669738).send(file=discord.File(r'./data.json'))
            print(f'{date}:INFO: {ctx.author} retrieved user data')
        else: print(f'{date}:WARNING: {ctx.author} attempted to retrieve user data')

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
