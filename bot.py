import discord
from discord.ext import commands
import collections, random, signal, re
import traceback, sys, asyncio

# Importing commands from ./botfunctions
from botfunctions import *

load_cogs = [ 'cogs.cmds_owner',
              'cogs.cmds_brag',
              'cogs.cmd_mrfreeze',
              'cogs.tempconverter' ]
bot = commands.Bot(command_prefix='!')

if __name__ == '__main__':
    for cog in load_cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(f'Failed to load extension {cog}.', file=sys.stderr)
            traceback.print_exc()

# This will be printed in the console once the
# bot has been connected to discord.
@bot.event
async def on_ready():
    print ('We have logged in as {0.user}'.format(bot))
    print ('User name: ' + str(bot.user.name))
    print ('User ID: ' + str(bot.user.id))
    print ('-----------')
    # Greetings message for all the servers
    for i in bot.guilds:
        try:
            bot_trash = discord.utils.get(i.channels, name='bot-trash')
            await bot_trash.send(':wave: ' + native.mrfreeze())
        except:
            print ('ERROR: No channel bot-trash in ' + i.name + '. Can\'t greet them.')

@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    # the trailing space let's us match temperatures at the end of the message.
    tempstatement = re.search('(\d+[,.]?\d+) ?(?:degrees|°?c(elcius)?|°?f(ahrenheit)?|' +
                              '°?k(elvin)?|°?r(ankine)?)[^\w]',
                              message.content.lower() + ' ')

    if message.author == bot.user:
        pass # never do anything the bot says.

    elif ctx.valid: # this is a command, we should invoke it.
        await bot.invoke(ctx)

    elif tempstatement != None:
        await temp.convert(ctx, tempstatement)

### Program ends here
# Client.run with the bots token
# Place your token in a file called 'token'
# Put the file in the same directory as the bot.
try:
    token = open('token', 'r').read().strip()
    bot.run(token, bot=True, reconnect=True)
except:
    print ('\nERROR: BOT TOKEN MISSING\n' +
           'Please put your bot\'s token in a separate text file called \'token\'.\n' +
           'This file should be located in the same directory as the bot files.\n')
    sys.exit(0)

# Graceful exit
def signal_handler(sig, frame):
        print('\n\nYou pressed Ctrl+C!\nI will now do like the tree, and get out of here.')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
signal.pause()
