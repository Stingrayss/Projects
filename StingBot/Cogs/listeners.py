import json
from datetime import datetime
import pytz
import time
from discord.ext import commands
from collections import defaultdict

#there might be a way to replace this, but the one I used caused big bugs
def read_json():
    with open('data.json', 'r') as file: 
        data = json.load(file)
        return data

def write_json(users):
    with open('data.json', 'w') as data:
        json.dump(users, data, indent = 4)

class listeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #checks servers status in the data and changes the file accordingly
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        data = read_json()
        
        #checks if the server is a key in the data
        #if so update the members data depending on if they exist in the data or not
        if str(guild.id) in data.keys():
            serverdata = data[str(guild.id)]
            for member in guild.members:
                if str(member.id) in data.keys():
                    serverdata[str(member.id)]['tracking'] = True
                else:
                    serverdata[member.id] = {"server": guild.id, "name": member.display_name, "tracking": True, "inactive": 0, "messages": 0, "time": 0, "last_session": 0, "voice_join": 0, "voice_leave": 0}
                write_json(data)
        #server was not in the data so create it's data and add to the file
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
        data = read_json()
        serverdata = data[str(guild.id)]
        for member in guild.members:
            serverdata[str(member.id)]['tracking'] = False
            write_json(data)

    #sets a user's tracking variable to false upon member removal from guild
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        data = read_json()
        serverdata = data[str(member.guild.id)]  
        serverdata[str(member.id)]['tracking'] = False
        write_json(data)
        tz = pytz.timezone("America/Los_Angeles")
        date = datetime.now(tz)
        print(f'{date}:INFO: {member.name} has been removed from: {member.guild}')
    
    #checks member status in the server and changes the data file accordingly
    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = read_json()
        serverdata = data[str(member.guild.id)]

        #user doesn't exist in data, make new dictionary for them
        if not str(member.id) in serverdata:
            user = {"server": member.guild.name, "name": member.display_name, "tracking": True, "inactive": 0, "messages": 0, "time": 0, "last_session": 0, "voice_join": 0, "voice_leave": 0}
            serverdata[member.id] = user
        #user exists in data, that means they are rejoining the server
        #set tracking variable to true
        else:
            serverdata[str(member.id)]['tracking'] = True

        write_json(data)
        tz = pytz.timezone("America/Los_Angeles")
        date = datetime.now(tz)
        print(f'{date}:INFO: {member.name} has joined: {member.guild}')

    #tracks a user's time spent in a voice call
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, VoiceStateBefore, VoiceStateAfter):
        data = read_json()
        user = data[str(member.guild.id)][str(member.id)]
        tz = pytz.timezone("America/Los_Angeles")
        date = datetime.now(tz)
        currenttime = round(time.time(), 2)

        #function to update a user's time variable in the data
        def update_time():
            user['voice_leave'] = currenttime
            #inserts the length of the session
            user['last_session'] = round((currenttime - user['voice_join']) / 60, 2)
            #updates the total time spent in a voice channel
            user['time'] += round((currenttime - user['voice_join']) / 60, 2)

        #checks to see if a user just joined a voice call
        #set the voice_join variable to the current time if they did
        if(VoiceStateBefore.channel == None and VoiceStateAfter.channel != None 
            or VoiceStateBefore.afk and VoiceStateAfter.channel != None):
            user['voice_join'] = currenttime

            print(f'{date}:INFO: {member.name} has joined {VoiceStateAfter.channel}')

        #checks to see if the user has gone afk
        #calculates and updates the time spent in a voice channel if they did
        elif(VoiceStateBefore.channel != None and VoiceStateAfter.channel != None and VoiceStateAfter.afk):
            update_time()

            print(f'{date}:INFO: {member.name} has gone afk')
        
        #checks to see if the user has left a channel
        #also updates time
        elif(VoiceStateBefore.channel != None and VoiceStateAfter.channel == None):
            if not VoiceStateBefore.afk:

                update_time()

            print(f'{date}:INFO: {member.name} has left {VoiceStateBefore.channel}')

        write_json(data)

    #increments a user's messages variable by 1 whenever a message is sent
    @commands.Cog.listener()
    async def on_message(self, message):
        data = read_json()
        user = data[str(message.guild.id)][str(message.author.id)]
        user['messages'] += 1
        write_json(data)

async def setup(bot):
    await bot.add_cog(listeners(bot))
