import discord, sys, os
from subprocess import run, PIPE
from discord.ext import commands
from botfunctions import checks

# This cog is for commands restricted to the owner of the bot (me!).
# It has features like !restart and !gitupdate.

class OwnerCmdsCog:
    def __init__(self, bot):
        self.bot = bot

    ####### restart #######
    ### RESTART THE Bot ###
    #######################
    @commands.command(name='restart')
    @commands.check(checks.is_owner)
    async def _restart(self, ctx, *args):
        await ctx.send(ctx.author.mention + " Yes Dear Leader... I will restart now.")
        print ('\n') # extra new line after the commandlog() output
        os.execl(sys.executable, sys.executable, *sys.argv)

    @commands.command(name='gitupdate', aliases=['git'])
    @commands.check(checks.is_owner)
    async def _gitupdate(self, ctx, *args):
        # git fetch returns nothing if no updates were found
        # for some reason the output of git fetch is posted to stderr
        gitfetch = str(run(['git', 'fetch'], stderr=PIPE, encoding='utf_8').stderr)
        gitpull = str(run(['git', 'pull'], stdout=PIPE, encoding='utf_8').stdout)
        output = str()

        if gitfetch == '':
            gitfetch = 'No output.'

        output += '**git fetch:**\n'
        output += gitfetch + '\n\n'
        output += '**git pull:**\n'
        output += gitpull

        await ctx.author.send(output)

def setup(bot):
    bot.add_cog(OwnerCmdsCog(bot))
