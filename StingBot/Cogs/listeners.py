import discord
import json
from datetime import datetime, timedelta
from discord.ext import commands, tasks

class listeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, Member, VoiceStateBefore, VoiceStateAfter):
        #print(f'{VoiceStateBefore.channel}, {VoiceStateAfter.channel}')
        if(VoiceStateBefore.channel == None and VoiceStateAfter.channel != None):
            print(f'{Member.name} has joined {VoiceStateAfter.channel}')
            time = datetime.now()
            seconds = time.timestamp()
            print(seconds)
        if(VoiceStateBefore.channel != None and VoiceStateAfter.channel == None):
            print(f'{Member.name} has left {VoiceStateBefore.channel}')
            time = datetime.now()
            seconds = time.timestamp()
            print(seconds)

def setup(bot):
    bot.add_cog(listeners(bot))

