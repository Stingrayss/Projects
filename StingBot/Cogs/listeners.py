import json
from datetime import datetime
from zoneinfo import ZoneInfo
import time
from discord.ext import commands
from collections import defaultdict

def write_json(users):
    with open('data.json', 'w') as data:
        json.dump(users, data, indent = 4)

class listeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open('data.json', 'r') as file: 
            self.bot.data = json.load(file)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        data = self.bot.data
        
        if str(guild.id) in data.keys():
            data = self.bot.data[str(guild.id)]
            for member in guild.members:
                if str(member.id) in data.keys():
                    data[str(member.id)]['tracking'] = True
                else:
                    data[member.id] = {"server": guild.id, "name": member.display_name, "tracking": True, "inactive": 0, "messages": 0, "time": 0, "last_session": 0, "voice_join": 0, "voice_leave": 0}
                write_json(data)
        else:
            server_list = defaultdict(dict)
            for member in guild.members:
                user = {"server": guild.name, "name": member.display_name, "tracking": True, "inactive": 0, "messages": 0, "time": 0, "last_session": 0, "voice_join": 0, "voice_leave": 0}
                server_list[guild.id][member.id] = user
                data |= server_list
            write_json(data)

    #sets a user's tracking variable to false upon bot removal from guild
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        for member in guild.members:
            self.bot.data[str(guild.id)][str(member.id)]['tracking'] = False
            write_json(self.bot.data)

    #sets a user's tracking variable to false upon member removal from guild
    @commands.Cog.listener()
    async def on_member_remove(self, member):    
        self.bot.data[str(member.guild.id)][str(member.id)]['tracking'] = False
        write_json(self.bot.data)
        date = datetime.now(ZoneInfo("America/Los_Angeles"))
        print(f'{date}:INFO: {member.name} has been removed from: {member.guild}')
    
    #checks member status in the server and changes the data file accordingly
    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = self.bot.data[str(member.guild.id)]

        #user doesn't exist in data, make new dictionary for them
        if not str(member.id) in data:
            user = {"server": member.guild.name, "name": member.display_name, "tracking": True, "inactive": 0, "messages": 0, "time": 0, "last_session": 0, "voice_join": 0, "voice_leave": 0}
            data[member.id] = user
        #user exists in data, that means they are rejoining the server
        #set tracking variable to true
        else:
            data[str(member.id)]['tracking'] = True

        write_json(self.bot.data)
        date = datetime.now(ZoneInfo("America/Los_Angeles"))
        print(f'{date}:INFO: {member.name} has joined: {member.guild}')

    #tracks a user's time spent in a voice call
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, VoiceStateBefore, VoiceStateAfter):
        user = self.bot.data[str(member.guild.id)][str(member.id)]
        date = datetime.now(ZoneInfo("America/Los_Angeles"))
        currenttime = round(time.time(), 3)
        #checks to see if a user just joined a voice call
        #set the voice_join variable to the current time if they did
        if(VoiceStateBefore.channel == None and VoiceStateAfter.channel != None):
            user['voice_join'] = currenttime

            print(f'{date}:INFO: {member.name} has joined {VoiceStateAfter.channel}')
        
        #checks to see if the user has left a channel
        #calculates and updates the time spent in a voice channel if they did
        elif(VoiceStateBefore.channel != None and VoiceStateAfter.channel == None):
            user['voice_leave'] = currenttime
            #inserts the length of the session
            user['last_session'] = round((currenttime - user['voice_join']) / 60, 3)
            #updates the total time spent in a voice channel
            user['time'] += round((currenttime - user['voice_join']) / 60, 3)

            print(f'{date}:INFO: {member.name} has left {VoiceStateBefore.channel}')

        write_json(self.bot.data)

    #increments a user's messages variable by 1 whenever a message is sent
    @commands.Cog.listener()
    async def on_message(self, message):
        self.bot.data[str(message.guild.id)][str(message.author.id)]['messages'] += 1
        write_json(self.bot.data)

def setup(bot):
    bot.add_cog(listeners(bot))