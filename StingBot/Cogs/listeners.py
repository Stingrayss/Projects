import discord
import json
import time
from discord.ext import commands, tasks
import random

class listeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, Member, VoiceStateBefore, VoiceStateAfter):
        #checks to see if a user is currently in a channel
        if(VoiceStateAfter.channel != None):
            #opens json file for reading to bring in data
            data = open('data.json', 'r')
            users = json.loads(data.read())
            user_list = users[f"{Member.id}"]
            data.close()
            #checks which server the user joined
            #then finds that location in the data and updates it 
            for dict in user_list:
                if(str(dict['server']) == str(Member.guild)):
                    dict['voice_join'] = time.time()
                    data = open('data.json', 'w')
                    json.dump(users, data, indent = 6)
                    data.close()

            print(f'{Member.name} has joined {VoiceStateAfter.channel}')
        
        #checks to see if the user has left a channel
        if(VoiceStateAfter.channel == None):
            #opens json file for reading to bring in data
            data = open('data.json', 'r')
            users = json.loads(data.read())
            user_list = users[f"{Member.id}"]
            data.close()
            #checks which server the user joined
            #then finds that location in the data and updates it
            for dict in user_list:
                if(str(dict['server']) == str(Member.guild)):
                    dict['voice_leave'] = time.time()
                    #inserts the time spent in a voice channel in minute notation
                    dict['last_session'] = (dict['voice_leave'] - dict['voice_join']) / 60
                    #updates the total time spent in a voice channel in minute notation
                    dict['time'] += (dict['voice_leave'] - dict['voice_join']) / 60
                    data = open('data.json', 'w')
                    json.dump(users, data, indent = 6)
                    data.close()
            print(f'{Member.name} has left {VoiceStateBefore.channel}')

    @commands.Cog.listener()
    async def on_message(self, message):
        data = open('data.json', 'r')
        users = json.loads(data.read())
        user_list = users[f"{message.author.id}"]
        data.close()

        for dict in user_list:
            if(str(dict['server']) == str(message.author.guild)):
                dict['messages'] += 1
                data = open('data.json', 'w')
                json.dump(users, data, indent = 6)
                data.close()


def setup(bot):
    bot.add_cog(listeners(bot))

