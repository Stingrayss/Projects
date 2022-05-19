import discord
import json
from datetime import datetime, timedelta
from discord.ext import commands, tasks

class listeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.last_timeStamp = datetime.utcfromtimestamp(0)

    @commands.Cog.listener()
    async def on_voice_state_update(self, Member, VoiceStateBefore, VoiceStateAfter):
        #print(f'{VoiceStateBefore.channel}, {VoiceStateAfter.channel}')
        if(VoiceStateBefore.channel == None and VoiceStateAfter.channel != None):
            time_difference = (datetime.utcnow() - self.last_timeStamp).total_seconds()
            #print(len(self.bot.get_channel(VoiceStateAfter.channel.id).members))
            if(time_difference > 120 and len(self.bot.get_channel(VoiceStateAfter.channel.id).members) == 1):
                await Member.guild.system_channel.send("☎️Ring Ring☎️", tts= True)
            self.last_timeStamp = datetime.utcnow()
            #need to have the user store time in variables

            print(f'{Member.name} has joined {VoiceStateAfter.channel}')

        if(VoiceStateBefore.channel != None and VoiceStateAfter.channel == None):
            print(f'{Member.name} has left {VoiceStateBefore.channel}')
            #might not need time out variable

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        print(message.author.name)

def setup(bot):
    bot.add_cog(listeners(bot))

