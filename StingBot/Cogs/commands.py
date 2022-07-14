from typing import OrderedDict
import discord
from datetime import datetime
import time
from zoneinfo import ZoneInfo
import json
from discord.ext import commands
#only need for users command
#from collections import defaultdict

def write_json(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent = 4)

#initalize the cog
class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open('data.json', 'r') as file: 
            self.bot.data = json.load(file)

    #This command gets changed to account for data updates
    #@commands.command(hidden=True)
    #@commands.has_permissions(administrator=True)
    #async def users(self, ctx):
        #server_list = defaultdict(dict)
        #user = {}
        #for guild in self.bot.guilds:
            #for member in guild.members:
                #user = {"server": guild.name, "name": member.display_name, "tracking": True, "inactive": 0, "messages": 0, "time": 0, "last_session": 0, "voice_join": 0, "voice_leave": 0}
                #server_list[guild.id][member.id] = user

        #out = open("data2.json", "w")
        #json.dump(server_list, out, indent = 4)
        #out.close()

        #writes the user display_name or their member.name if none

        #for guild in self.bot.data:
            #user_list = self.bot.data[guild]
            #for key in user_list:
                #user_list[key]['name'] = self.bot.get_guild(int(guild)).get_member(int(key)).display_name

            #with open('data2.json', 'w') as data:
                #json.dump(self.bot.data, data, indent = 4)

    #sends a leaderboard of the top 10 users for time spent in a server
    @commands.command(hidden=True, aliases = ['l'])
    async def leaderboard(self, ctx):
        topten = []
        currenttime = round(time.time(), 3)
        serverdata = self.bot.data[str(ctx.guild.id)]

        #grabs all members currently in a channel for the server the command was sent in
        #then updates those member's time variable
        for channel in ctx.guild.voice_channels:
            for user in channel.members:
                user_data = serverdata[str(user.id)]
                user_data["time"] += ((currenttime - user_data["voice_join"]) / 60)

        #add 10 users from the server to a list
        #then sort and start comparing the last person in the list to the current person
        #replace if current > last
        for key in serverdata:
            user = serverdata[key]
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
        #sends an embedded message from stingbot listing the top 10 users
        users = ''
        for i in range (0, len(topten)): 
            users += f'{i + 1}. {topten[i][0]}: {round(topten[i][1], 1) } minutes\n\n'
        embed = discord.Embed(title = 'Voice Leaderboard', color=discord.Colour.dark_blue())
        embed.add_field(name = f'Top 10:', value=users)
        await ctx.send(embed = embed)

    #sends a leaderboard of the top 10 users for messages sent in a server
    #code is same as the above leaderboard command
    @commands.command(hidden=True)
    async def messages(self, ctx):
        topten = []
        serverdata = self.bot.data[str(ctx.guild.id)]

        for key in serverdata:
            user = serverdata[key]
            if len(topten) < 10:
                tuple = user["name"], user["messages"]
                topten.append(tuple)
            else:
                topten.sort(key=lambda x : x[1], reverse = True)
                if user["messages"] > topten[-1][1]:
                    tuple = user["name"], user["messages"]
                    topten[-1] = tuple

        topten.sort(key=lambda x : x[1], reverse = True)

        users = ''
        for i in range (0, len(topten)): 
            users += f'{i + 1}. {topten[i][0]}: {round(topten[i][1], 1) } messages\n\n'
        embed = discord.Embed(title = 'Message Leaderboard', color=discord.Colour.dark_blue())
        embed.add_field(name = f'Top 10:', value=users)
        await ctx.send(embed = embed)

    #sends a message with the specified user's current time spent in call
    @commands.command(aliases = ['s'])
    async def session(self, ctx, *, user=""):
        currenttime = round(time.time(), 3)
        serverdata = self.bot.data[str(ctx.guild.id)]

        #checks if there was no user parameter
        #if not it assumes the message author and checks if they are in a call
        if not user and ctx.author.voice != None:
            await ctx.send(f'You have been in the call for {round((currenttime - serverdata[str(ctx.author.id)]["voice_join"]) / 60, 2)} minutes')
            return
        elif not user and ctx.author.voice == None:
            await ctx.send(f'You are not currently in a channel, try again when you are')
            return

        #could be faster?
        #creates two lists for a user's name and display name
        #then checks for duplicates in either list
        members_names = []
        members_nicks = []
        for member in ctx.guild.members:
            members_names.append(member.name)
            members_nicks.append(member.display_name)
        if members_names.count(user) > 1 or members_nicks.count(user) > 1:
            del members_names
            del members_nicks
            await ctx.send(f'{user} appears more than once in this server, try using their discord name or discord id')
            return
        del members_names
        del members_nicks
    
        #checks if the user parameter matches anyone in the server
        #and if they are in a call
        for member in serverdata:
            member = ctx.guild.get_member(int(member))
            
            if member.name.lower() == user.lower() or member.display_name.lower() == user.lower() or str(member.id) == user:
                if member.voice != None:
                    await ctx.send(f'{member.display_name} has been in the call for {round((currenttime - serverdata[str(member.id)]["voice_join"]) / 60, 2)} minutes')
                    return
                else:
                    await ctx.send(f'{member.display_name} is not currently in a channel, try again when they are')
                    return
        
        await ctx.send(f'{user} does not exist in this guild')

    #sends a message with the specified user's last amount of time spent in call
    #same as the above session command but doesn't check if a user is in call
    @commands.command(aliases = ['ls'])
    async def lastsession(self, ctx, *, user=""):
        serverdata = self.bot.data[str(ctx.guild.id)]

        if not user:
            await ctx.send(f'You were last in call for {serverdata[str(ctx.author.id)]["last_session"]} minutes')
            return

        members_names = []
        members_nicks = []
        for member in ctx.guild.members:
            members_names.append(member.name)
            members_nicks.append(member.display_name)
        if members_names.count(user) > 1 or members_nicks.count(user) > 1:
            del members_names
            del members_nicks
            await ctx.send(f'{user} appears more than once in this server, try using their discord name or discord id')
            return
        del members_names
        del members_nicks

        for member in serverdata:
            member = ctx.guild.get_member(int(member))
            
            if member.name.lower() == user.lower() or member.display_name.lower() == user.lower() or str(member.id) == user:
                await ctx.send(f'{member.display_name} was last in call for {serverdata[str(member.id)]["last_session"]} minutes')
                return
        
        await ctx.send(f'{user} does not exist in this guild')

    @commands.command(aliases = ['prune', 'p'])
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, *, amount=1):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'messages have been deleted', delete_after = 2)

    #Only I can use this command and it sends me the data from the json file
    #into a private discord channel for me to easily obtain from the server ran bot
    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def data(self, ctx):
        date = datetime.now(ZoneInfo("America/Los_Angeles"))
        if(ctx.author.id == 105032801715290112):
            #not sure how this orders the data, but it does something
            self.bot.data = OrderedDict(sorted(self.bot.data.items(), key=lambda k: k[0][2], reverse=True))

            write_json(self.bot.data)
            
            await self.bot.get_channel(734204331552669738).send(file=discord.File(r'./data.json'))
            print(f'{date}:INFO: {ctx.author} retrieved user data')
        else: print(f'{date}:WARNING: {ctx.author} attempted to retrieve user data')

def setup(bot):
    bot.add_cog(Commands(bot))
