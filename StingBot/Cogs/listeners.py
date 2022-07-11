import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import time
from discord.ext import commands
from collections import defaultdict

def read_json():
    with open('data.json', 'r') as data: 
        users = json.load(data)
        return users

def write_json(users):
    with open('data.json', 'w') as data:
        json.dump(users, data, indent = 4)

class listeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #THIS NEEDS TO ACCOUNT FOR WHEN BOT LEAVES AND REJOINS
    #BUT NEW USERS JOINED INBETWEEN THAT TIME, ALSO DON'T
    #APPEND DATA IF A USER ALREADY EXISTED, JUST REMOVE 
    #THE "- removed"

    #Maybe make a update function that looks to see if a user exists
    #so that it can just add to the list of servers or if they are
    #new to the data, create a new list for them

    #@commands.Cog.listener()
    #async def on_guild_join(self, guild):
        #stole code from users commands
        #user_list = defaultdict(list)
        #user = {}

        #for member in guild.members:
            #user = {"id": member.id, "name": member.name, "tracking": True, "messages": 0, "time": 0, "last_session": 0, "voice_join": 0, "voice_leave": 0}
            #user_list[member.id].append(user)

        #users = read_json()

        #with open('data.json', 'w') as data:
            #users.update(user_list)
            #json.dump(users, data, indent = 4)

    #sets a user's tracking variable to false upon bot removal from guild
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        data = read_json()

        for member in guild.members:
            data[str(guild.id)][str(member.id)]['tracking'] = False
            write_json(data)

    #sets a user's tracking variable to false upon member removal from guild
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        data = read_json()
        
        data[str(member.guild.id)][str(member.id)]['tracking'] = False
        write_json(data)
        date = datetime.now(ZoneInfo("America/Los_Angeles"))
        print(f'{date}:INFO: {member.name} has been removed from: {member.guild}')
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = read_json()

        print(not member.id in data[str(member.guild.id)].keys())
        #user doesn't exist in data, make new dictionary for them
        if not str(member.id) in data[str(member.guild.id)]:
            user = {"server": member.guild.name, "name": member.name, "tracking": True, "inactive": 0, "messages": 0, "time": 0, "last_session": 0, "voice_join": 0, "voice_leave": 0}
            data[str(member.guild.id)][str(member.id)] = user
        else:
            data[str(member.guild.id)][str(member.id)]['tracking'] = True

        write_json(data)
        date = datetime.now(ZoneInfo("America/Los_Angeles"))
        print(f'{date}:INFO: {member.name} has joined: {member.guild}')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, VoiceStateBefore, VoiceStateAfter):
        data = read_json()
        user = data[str(member.guild.id)][str(member.id)]
        date = datetime.now(ZoneInfo("America/Los_Angeles"))
        #checks to see if a user is currently in a channel
        if(VoiceStateBefore.channel == None and VoiceStateAfter.channel != None):
            user['voice_join'] = round(time.time(), 3)

            print(f'{date}:INFO: {member.name} has joined {VoiceStateAfter.channel}')
        
        #checks to see if the user has left a channel
        elif(VoiceStateBefore.channel != None and VoiceStateAfter.channel == None):
            user['voice_leave'] = round(time.time(), 3)
            #inserts the time spent in a voice channel in minute notation
            user['last_session'] = round((user['voice_leave'] - user['voice_join']) / 60, 3)
            #updates the total time spent in a voice channel in minute notation
            user['time'] += round((user['voice_leave'] - user['voice_join']) / 60, 3)

            print(f'{date}:INFO: {member.name} has left {VoiceStateBefore.channel}')

        write_json(data)

    #increments a user's messages variable by 1 whenever a message is sent
    @commands.Cog.listener()
    async def on_message(self, message):
        data = read_json()

        data[str(message.guild.id)][str(message.author.id)]['messages'] += 1
        write_json(data)

def setup(bot):
    bot.add_cog(listeners(bot))