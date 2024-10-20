import discord
import random
import os
import math
import pickle
from timeit import default_timer as timer
from discord.ext import commands, tasks

#SAVED DATA
queuelist = [] #'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'
seasongames = 16
totalgames = 81
redwins = 9
bluewins = 7

if os.path.getsize('queue.txt') > 0:
    with open('queue.txt', 'rb') as fq:
        queuelist = pickle.load(fq)
if os.path.getsize('seasongames.txt') > 0:
    with open('seasongames.txt', 'rb') as fsg:
        seasongames = pickle.load(fsg)
if os.path.getsize('totalgames.txt') > 0:
    with open('totalgames.txt', 'rb') as ftg:
        totalgames = pickle.load(ftg)
if os.path.getsize('redwins.txt') > 0:
    with open('redwins.txt', 'rb') as frw:
        redwins = pickle.load(frw)
if os.path.getsize('bluewins.txt') > 0:
    with open('bluewins.txt', 'rb') as fbw:
        bluewins = pickle.load(fbw)

#UNSAVED DATA
start = 0
gamestart = False

#initalize the cog
class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    #commands
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

    @commands.command(aliases = ['j'])
    async def join(self, ctx):
        global queuelist
        member = ctx.author.name
        if len(queuelist) == 10:
            await ctx.send('The queue is currently full')
            return
        for x in range(0, len(queuelist)):
            if queuelist[x] == member:
                await ctx.send('You are already in the queue')
                return
        else:
            queuelist.append(member)
            with open('queue.txt', 'wb') as fq:
                pickle.dump(queuelist, fq)
            await ctx.send(f'{ctx.author.name}: You have joined the queue')

    @commands.command(aliases = ['a'])
    async def add(self, ctx, user):
        global queuelist
        member = user
        if len(queuelist) == 10:
            await ctx.send('The queue is currently full')
            return
        for x in range(0, len(queuelist)):
            if queuelist[x] == member:
                await ctx.send('That player is already in the queue')
                return
        else:
            queuelist.append(member)
            with open('queue.txt', 'wb') as fq:
                pickle.dump(queuelist, fq)
            await ctx.send(f'{user}: has joined the queue')

    @commands.command(aliases = ['l'])
    async def leave(self, ctx):
        global queuelist
        for x in range(0, len(queuelist)):
            if queuelist[x] == ctx.author.name:
                queuelist.remove(queuelist[x])
                await ctx.send(f'{ctx.author.name}: You have left the queue')
                return
        else:
            await ctx.send('You are not in the queue')

    @commands.command(aliases = ['rm'])
    async def remove(self, ctx, user):
        global queuelist
        for x in range(0, len(queuelist)):
            if queuelist[x] == user:
                queuelist.remove(queuelist[x])
                await ctx.send(f'{user}: has been removed from the queue')
                return
        else:
            await ctx.send('That player is not in the queue')

    @commands.command(aliases = ['r'])
    async def randomize(self, ctx):
        global queuelist
        global teamred
        global teamblue
        if len(queuelist) != 10:
            await ctx.send('There are not enough players in queue!')
            return
        else:
            teamred = []
            teamblue = []
            while len(queuelist) != 0: #splits the queuelist randomly into two teams and clears the queue in the process
                tempvar = random.choice(queuelist)
                teamred.append(tempvar)
                queuelist.remove(tempvar)
                tempvar = random.choice(queuelist)
                teamblue.append(tempvar)
                queuelist.remove(tempvar)
            embed = discord.Embed(title = f'Teams', color=discord.Colour.dark_blue())
            embed.add_field(name = '‎Team Blue', value = f'1. {teamblue[0]} \n 2. {teamblue[1]} \n 3. {teamblue[2]} \n 4. {teamblue[3]} \n 5. {teamblue[4]}')
            embed.add_field(name = 'Team Red', value = f'1. {teamred[0]} \n 2. {teamred[1]} \n 3. {teamred[2]} \n 4. {teamred[3]} \n 5. {teamred[4]}')
            await ctx.send(embed = embed)

    @commands.command(aliases = ['c'])
    async def clear(self, ctx):
        global queuelist
        queuelist.clear()
        with open('queue.txt', 'wb') as fq:
            pickle.dump(queuelist, fq)
        await ctx.send('The queue has been cleared')
        
    @commands.command(aliases = ['q'])
    async def queue(self, ctx):
        global queuelist
        if os.path.getsize('queue.txt') > 0:
            with open('queue.txt', 'rb') as fq:
                queuelist = pickle.load(fq)
        players = '‎'
        for x in range(0, len(queuelist)): #uses the player variable to put each name underneath one another
            players += f'{x + 1}. {queuelist[x]} \n'
        embed = discord.Embed(title = 'Queue', color=discord.Colour.dark_blue())
        embed.add_field(name = f'Players needed: {10 - (len(queuelist))}‎', value = players)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['s'])
    async def start(self, ctx):
        global start
        global gamestart
        global seasongames
        global totalgames
        start = timer()
        seasongames = int(seasongames) + 1
        seasongames = str(seasongames)
        totalgames = int(totalgames) + 1
        totalgames = str(totalgames)
        gamestart = True

        with open('seasongames.txt', 'wb') as fsg:
            pickle.dump(seasongames, fsg)
        with open('totalgames.txt', 'wb') as ftg:
            pickle.dump(totalgames, ftg)

        await ctx.send(f'Game {int(seasongames)} of season 4 has started')

    @commands.command(aliases = ['g'])
    async def game(self, ctx):
        if gamestart == False:
            await ctx.send('There is no game in progress')
            return
        global start
        global seasongames
        global teamred
        global teamblue
        embed = discord.Embed(title = f'Teams', description = (f'Game {int(seasongames)} of season 4 has been playing for: {math.floor((start) / 60)} minutes'), color=discord.Colour.dark_blue())
        embed.add_field(name = '‎Team Blue', value = f'1. {teamblue[0]} \n 2. {teamblue[1]} \n 3. {teamblue[2]} \n 4. {teamblue[3]} \n 5. {teamblue[4]}')
        embed.add_field(name = 'Team Red', value = f'1. {teamred[0]} \n 2. {teamred[1]} \n 3. {teamred[2]} \n 4. {teamred[3]} \n 5. {teamred[4]}')
        await ctx.send(embed = embed)

    @commands.command(aliases = ['e']) #STILL NEED TO FIGURE OUT HOW TO FIX THE RED AND BLUE TEAM ASPECT
    async def end(self, ctx, *, team):
        global gamestart
        global redwins
        global bluewins
        global start
        gamestart = True
        if gamestart == False:
            await ctx.send(f'There is no game in session')
            return
        if team == 'red':
            redwins = int(redwins) + 1
            redwins = str(redwins)
            with open('redwins.txt', 'wb') as frw:
                pickle.dump(redwins, frw)
        elif team == 'blue':
            bluewins = int(bluewins) + 1
            bluewins = str(bluewins)  
            with open('bluewins.txt', 'wb') as fbw:
                pickle.dump(bluewins, fbw)
        end = timer()
        await ctx.send(f'{team.lower()} won the game in {(end - start) / 60} minutes')

    @commands.command(aliases = ['st'])
    async def stats(self, ctx):
        teamredwinrate = math.floor((int(redwins) / int(seasongames)) * 100)
        teambluewinrate = math.floor((int(bluewins) / int(seasongames)) * 100)
        await ctx.send(f'Season 4 Stats\nTotal games played: {int(totalgames)}\nTotal games played this season: {int(seasongames)}\nTeam red has won {int(redwins)} games this season with a win rate of {teamredwinrate}%\nTeam blue has won {int(bluewins)} games this season with a win rate of {teambluewinrate}%\n')


def setup(bot):
    bot.add_cog(Commands(bot))