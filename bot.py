import asyncio
import discord
import requests, json 
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
from datetime import timedelta, datetime
from cogs.libs import brainfuck   # BrainFu*k Interpreter
from cogs.libs import getch
from cogs.libs.JB import jbin     #JB Interpreter - JB language is in beta

#===================================== ROOT =========================================#

with open('./config.json') as f:
  data = json.load(f)
  token = data['Token']
  prefix = data['Prefix']
print(f"Prefix is {prefix}, you can change it in config.json")
client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))
client.remove_command('help')

#================================ COGS & EXTENSIONS =================================#

client.load_extension('cogs.help')
client.load_extension('cogs.emojify')
client.load_extension('cogs.counting')
client.load_extension('cogs.mod')
client.load_extension('cogs.user')
client.load_extension('cogs.Bot')
client.load_extension('cogs.modmail')
client.load_extension('cogs.error_handling')
client.load_extension('cogs.suntzu')

#===================================== EVENTS =======================================#

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="omg aspyr can code?!?!"))

#=================================== INTERPRETERS =======================================#

@client.command(name='bf', aliases=['brainfuck', 'BrainFuck'])
async def bf(ctx, *, thing: str = None):
    """Brainfuck Interpreter"""
    await ctx.trigger_typing()
    sourcecode = thing
    result = brainfuck.evaluate(sourcecode)
    if result is not None:
        embed = discord.Embed(color = discord.Color.blue())
        embed.set_author(name="Billy's BrainFuck Interpreter")
        embed.add_field(name='Output', value=f"> {result}")
    else:
        embed = discord.Embed(color = discord.Color.red())
        embed.set_author(name="Billy's BrainFuck Interpreter")
        embed.add_field(name='Syntax Error', value="> No result for you, shoo shoo")
    await ctx.send(embed=embed)

@client.command(name='jb', aliases=['jB', 'Jb', 'JB'])
async def jb(ctx, *, thing):
    """JB Interpreter"""
    await ctx.trigger_typing()
    result = jbin(thing)
    if result is not None:
        embed = discord.Embed(color = discord.Color.blue())
        embed.set_author(name="JB Interpreter")
        embed.add_field(name='Output', value=f"> {result}")
    else:
        embed = discord.Embed(color = discord.Color.red())
        embed.set_author(name="JB Interpreter")
        embed.add_field(name='Syntax Error', value="> No result for you, shoo shoo")
    await ctx.send(embed=embed)
@jb.error
async def jb_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.trigger_typing()
        embed = discord.Embed(color = discord.Color.red())
        embed.set_author(name="JB Interpreter")
        embed.add_field(name='Syntax Error', value="> I think you need to put smthn, lol")
        await ctx.send(embed=embed)

#=================================== bot start =====================================#

client.run(token)
