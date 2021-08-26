import discord
import random
from discord.ext import commands
from discord import Member

class Example(commands.Cog):

    def __init__(self, client):
        self.client = client

    #@commands.Cog.listener()

    @commands.command()
    async def pong(self, ctx):
        await ctx.send('Ping! (This is a super secret command!)')
    
    @commands.command()
    async def kill(self, ctx, member: Member):
        author = ctx.message.author
        imagerand = random.randint(0,2)
        if imagerand == 1:
            url = 'https://media.giphy.com/media/l4FGvTL3rGuoo1Oy4/giphy.gif'
        else:
            url = 'https://media1.tenor.com/images/df70844e3665473e5961837723d5d18f/tenor.gif?itemid=15781857' 
        embed = discord.Embed(
            title = 'Oh No!', 
            description = '{} killed {}!'.format(author.mention, member.mention),
            colour = discord.Colour.red()
        )
        embed.set_image(url=url)

        await ctx.send(embed=embed)

    @commands.command()
    async def hug(self, ctx, member: Member):
        author = ctx.message.author
        imagerand = random.randint(0,2)
        if imagerand == 1:
            url = 'https://media.giphy.com/media/3oEdv4hwWTzBhWvaU0/giphy.gif'
        else:
            url = 'https://media.giphy.com/media/f6y4qvdxwEDx6/giphy.gif' 
        embed = discord.Embed(
            title = 'Awww', 
            description = '{} hugged {}!'.format(author.mention, member.mention),
            colour = discord.Colour.red()
        )
        embed.set_image(url=url)

        await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, member: Member):
        author = ctx.message.author
        imagerand = random.randint(0,2)
        if imagerand == 1:
            url = 'https://media.giphy.com/media/uG3lKkAuh53wc/giphy.gif'
        else:
            url = 'https://media.giphy.com/media/uqSU9IEYEKAbS/giphy.gif' 
        embed = discord.Embed(
            title = 'Ouch!', 
            description = '{} slapped {}!'.format(author.mention, member.mention),
            colour = discord.Colour.red()
        )
        embed.set_image(url=url)

        await ctx.send(embed=embed)

    @commands.command()
    async def punch(self, ctx, member: Member):
        author = ctx.message.author
        imagerand = random.randint(0,2)
        if imagerand == 1:
            url = 'https://media.giphy.com/media/l1J3G5lf06vi58EIE/giphy.gif'
        else:
            url = 'https://media.giphy.com/media/x6I3pGtblFtDO/giphy.gif' 
        embed = discord.Embed(
            title = 'Ouch!', 
            description = '{} punched {}!'.format(author.mention, member.mention),
            colour = discord.Colour.red()
        )
        embed.set_image(url=url)

        await ctx.send(embed=embed)

    @commands.command()
    async def pog(self, ctx, member: Member):
        await ctx.channel.purge(limit= 1)
        await ctx.send(f'<:PagChomp:733560691738279966> {member.mention}')
    

def setup(client):
    client.add_cog(Example(client))