import json
import datetime
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
            #user = {"name": member.name, "server": f'{member.guild}', "tracking": True, "messages": 0, "time": 0, "last_session": 0, "voice_join": 0, "voice_leave": 0}
            #user_list[member.id].append(user)

        #users = read_json()

        #with open('data.json', 'w') as data:
            #users.update(user_list)
            #json.dump(users, data, indent = 4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        #grabs all of the users from the data file
        users = read_json()

        #gets every user that was in the guild
        #so that it may be accessed from the json file
        for member in guild.members:
            #this grabs a user with a specific key from the json file
            user = users[f"{member.id}"]
            #if the user had a server that matched
            #update it to mark that it is no longer being tracked
            for dict in user:
                if(str(dict['server']) == str(guild)):
                    dict['tracking'] = False
                    write_json(users)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        users = read_json()

        #if the member is found in the data,
        #and they had a server that matches the one they left
        #set tracking to false
        if str(member.id) in users:   
            user = users[f"{member.id}"]
            for dict in user:
                if(str(dict['server']) == str(member.guild)):
                    dict['tracking'] = False
                    write_json(users)
            
        print(f'{datetime.datetime.now()}:INFO: {member.name} has been removed from: {member.guild}')
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        users = read_json()
        #if the user doesn't exist in the data, make a list of objects for them
        if not str(member.id) in users:
            user_list = defaultdict(list)
            user = {"name": member.name, "server": f'{member.guild}', "tracking": True, "messages": 0, "time": 0, "last_session": 0, "voice_join": 0, "voice_leave": 0}
            user_list[member.id].append(user)
            users.update(user_list)
            write_json(users)
        else:
            user = users[f"{member.id}"]
            #if they did exist, check if they used to be in the server
            #if they were set tracking back to true
            for dict in user:
                if(str(dict['server']) == str(member.guild)):
                    dict['tracking'] = True
                    write_json(users)
                    return
            #the user existed, but not in this server, so make a new data object 
            #and push it back into their list
            user_add = {"name": member.name, "server": f'{member.guild}', "tracking": True, "messages": 0, "time": 0, "last_session": 0, "voice_join": 0, "voice_leave": 0}
            user.append(user_add)
            write_json(users)

        print(f'{datetime.datetime.now()}:INFO: {member.name} has joined: {member.guild}')

    @commands.Cog.listener()
    async def on_voice_state_update(self, Member, VoiceStateBefore, VoiceStateAfter):
        #checks to see if a user is currently in a channel
        if(VoiceStateBefore.channel == None and VoiceStateAfter.channel != None):
            users = read_json()
            user = users[f"{Member.id}"]
            #makes sure that the variable being changed is the one for the correct server
            for dict in user:
                if(str(dict['server']) == str(Member.guild)):
                    dict['voice_join'] = round(time.time(), 3)
                    write_json(users)

            print(f'{datetime.datetime.now()}:INFO: {Member.name} has joined {VoiceStateAfter.channel}')
        
        #checks to see if the user has left a channel
        if(VoiceStateBefore.channel != None and VoiceStateAfter.channel == None):
            users = read_json()
            user = users[f"{Member.id}"]

            for dict in user:
                if(str(dict['server']) == str(Member.guild)):
                    dict['voice_leave'] = round(time.time(), 3)
                    #inserts the time spent in a voice channel in minute notation
                    dict['last_session'] = round((dict['voice_leave'] - dict['voice_join']) / 60, 3)
                    #updates the total time spent in a voice channel in minute notation
                    dict['time'] += round((dict['voice_leave'] - dict['voice_join']) / 60, 3)
                    write_json(users)

            print(f'{datetime.datetime.now()}:INFO: {Member.name} has left {VoiceStateBefore.channel}')

    @commands.Cog.listener()
    async def on_message(self, message):
        users = read_json()
        user = users[f"{message.author.id}"]

        for dict in user:
            if(str(dict['server']) == str(message.author.guild)):
                dict['messages'] += 1
                write_json(users)

def setup(bot):
    bot.add_cog(listeners(bot))