import discord
import random
import os
import requests
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import Member
from discord.ext.commands import Bot
from discord import Status
from riotwatcher import LolWatcher, ApiError

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '.', intents=intents)
client.remove_command('help')
word = []


api_key = 'RGAPI-bf4625a5-37ca-498b-8a02-786a227a0d2b'
watcher = LolWatcher(api_key)
my_region = 'na1'




def numsort(str):
    numbers = ''
    for i in range(len(str)):
        if str[i].isdigit():
            numbers = numbers + str[i]
    return(numbers)
def lettersort(str):
    capital = ''
    for i in range(len(str)):
        if str[i].isupper():
            capital = capital + str[i]
    return(capital)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Use .help for a list of commands"))
    print('Bot is ready.')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server!')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server :(')

@client.event
async def on_message(message):
    if 'retard' in message.content:
        await message.add_reaction('<:RWORD:733563581454483476>')

    await client.process_commands(message)

#commands-------------------------------------------------------------------------------------------------------------

@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')

@client.command(aliases = ['ppsize', 'num', 'penis_size', 'dndroll', 'iq'])
async def roll(ctx, *, question = None):
    randint = random.randint(1, 101)
    await ctx.send(randint)
   
#clear
@client.command(aliases = ['purge'])
@has_permissions(manage_messages=True)
async def clear(ctx, amount=0):
        await ctx.channel.purge(limit= amount+1)
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry you are not allowed to use this command.')

#kick
@client.command(aliases = ['boot', 'delete'])
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.channel.purge(limit= 1)
        await ctx.send(f'User {member} has been kicked')
        await ctx.send(f'Reason: {reason}')
        if reason == None:
            await member.send(f'You have been kicked for No Reason Specified')
        else:
            await member.send(f'You have been kicked for {reason}.')
@kick.error
async def kick_error(ctx, error):
   if isinstance(error, commands.MissingPermissions):
       await ctx.send("You don't have permission to do that!")
#ban
@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.channel.purge(limit= 1)
        await ctx.send(f'User {member} has been banned')
        await ctx.send(f'Reason: {reason}')
        if reason == None:
            await member.send(f'You have been banned for No Reason Specified')
        else:
            await member.send(f'You have been banned for {reason}.')
@ban.error
async def ban_error(ctx, error):
   if isinstance(error, commands.MissingPermissions):
       await ctx.send("You don't have permission to do that!")

#unban
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.channel.purge(limit= 1)
            await ctx.send(f'Unbanned {user.name}!')
            return

#help
@client.command(aliases = ['help'])
async def support(ctx):
    embed = discord.Embed(
        title = 'List of commands for Cygbot.', 
        description = 'My prefix is "."',
        colour = discord.Colour.blue()
    )

    embed.set_footer(text='Note, this bot is still being tested, so some commands may not work!')
    #embed.set_image(url='')
    embed.set_thumbnail(url='https://cdn2.iconfinder.com/data/icons/seo-cartoon/512/sim4013-512.png')
    #embed.set_author(name = 'Author Name')#, icon_url='')
    embed.add_field(name = 'help', value='Displays this text!.', inline=False)
    embed.add_field(name = 'roll', value='Rolls for a random number between 1 and 100! You may add a question after the command.', inline=False)
    embed.add_field(name = 'ping', value='Returns the current ping for the bot.', inline=False)
    embed.add_field(name = 'kick', value='kicks the user specified.', inline=False)
    embed.add_field(name = 'ban', value='bans the user specified.', inline=False)
    embed.add_field(name = 'clear', value='Clears the number of previously specified messages.', inline=False)
    embed.add_field(name = 'unban', value='Unbans a specified user. This requires you to input their whole username and tag.', inline=False)
    embed.add_field(name = 'info', value='userinfo, channelinfo, guildinfo, leagueinfo', inline=False)
    embed.add_field(name = 'Fun Commands:', value='kill, slap, hug, punch, pog', inline=False)
    

    await ctx.send(embed=embed)

@client.command(aliases = ['ui'])
async def userinfo(ctx, member: Member):
    pfp = member.avatar_url
    created = member.created_at.strftime("%b, %d, %Y")      
    if member.status == discord.Status.online:
        embed = discord.Embed(
            title = 'User info for {}'.format(member), 
            #description = 'Current User status {}'.format(member.activity),
            colour = discord.Colour.green()
        )
    elif member.status == discord.Status.dnd:
        embed = discord.Embed(
            title = 'User info for {}'.format(member), 
            colour = discord.Colour.red()
        )
    elif member.status == discord.Status.offline:
        embed = discord.Embed(
            title = 'User info for {}'.format(member), 
            colour = discord.Colour.greyple()
        )
    else:
        embed = discord.Embed(
            title = 'User info for {}'.format(member), 
            colour = discord.Colour.gold()
        )   
   
    embed.add_field(name = 'Current User Presence', value=f'{member.status}', inline=False)
    embed.add_field(name = 'Current User Status', value=f'{member.activity}', inline=False)
    embed.add_field(name = 'Server nickname (if applicable)', value=f'{member.display_name}', inline=False)
    embed.add_field(name = 'User join date', value=f'{created}', inline=False)
    if member.is_on_mobile():
        embed.set_footer(text='This user is currently on a mobile device.')
    else:
        embed.set_footer(text='This user is not currently on a mobile device.')
    embed.set_thumbnail(url=pfp)
    await ctx.send(embed=embed)


@client.command(aliases = ['li'])
async def leagueinfo(ctx, user):
    i = -1
    level = ''
    rankplay = True
    try:
        me = watcher.summoner.by_name(my_region, user)
        my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
    except:
        await ctx.send('User could not be found or invalid API key (ask Cygnus to regenerate)')
    
    me = str(me)
    if my_ranked_stats == []:
        rankf = 'This user has not played ranked this season!'
        rankplay = False
    else:
        my_ranked_stats = str(my_ranked_stats)
        rank = my_ranked_stats.split(",")
        rankf = lettersort(rank[2]) + ' ' + lettersort(rank[3])
        rankw = rank[7]
        rankl = rank[8]
        rankstreak = rank[12] 
    level = me.split(",")
    embed = discord.Embed(
        title = f'Player info for {user}', 
        colour = discord.Colour.gold()
    )   
    profilenum = numsort(level[4])
    profilenum = str(profilenum)
    embed.set_thumbnail(url='http://ddragon.leagueoflegends.com/cdn/11.9.1/img/profileicon/' + profilenum + '.png')
    embed.add_field(name = 'User Level', value=f'{numsort(str(level[6][:-1]))}', inline=False)
    embed.add_field(name = 'Rank', value=rankf, inline=False)   
    if rankplay:
        embed.add_field(name = 'Ranked Wins', value=numsort(str(rankw)), inline=True)
        embed.add_field(name = 'Ranked Losses', value=numsort(str(rankl)), inline=True)
        embed.add_field(name = 'Winning Streak (T/F)', value=lettersort(str(rankstreak))[1], inline=False)     
    embed.add_field(name = 'OP.GG stats', value=f'[profile](https://na.op.gg/summoner/userName={user})', inline=False)   
    await ctx.send(embed=embed)

@client.command(aliases = ['hr'])
async def hyrank(ctx, player):
    data = requests.get(
    url = "https://api.hypixel.net/player",
    params = {
        "key": "7b547f0d-efc7-4e9e-9fdd-7e0f5b68f9ca",
        "name": f'{player}'
    }
    ).json()
    try:
        if "rank" in data["player"] and not data["player"]["rank"] == "NORMAL":
            rank = data["player"]["rank"]
        elif "monthlyPackageRank" in data["player"] and not data["player"]["monthlyPackageRank"] == "NONE":
            rank = data["player"]["monthlyPackageRank"]
        elif "newPackageRank" in data["player"]:
            rank = data["player"]["newPackageRank"]
        elif "packageRank" in data["player"]:
            rank = data["player"]["packageRank"]
        else:
            rank = "No Rank"
        await ctx.send(rank)
    except:
        await ctx.send("API on Cooldown, please wait one minute")

@client.command(aliases = ['ci'])
async def channelinfo(ctx):
    #icon_url = ctx.guild.icon_url
    embed = discord.Embed(
        title = f'Displaying info for {ctx.channel.name}', 
        colour = discord.Colour.green()
    )
    #embed.set_image(url=icon_url)
    embed.set_footer(text=f'Channel Id {ctx.channel.mention}')
    embed.add_field(name = 'Server', value=f'{ctx.channel.guild}', inline=False)
    embed.add_field(name = 'Channel Pos', value=f'{ctx.channel.position + 1}', inline=False)
    embed.add_field(name = 'Category', value=f'{ctx.channel.category}', inline=False)
    embed.add_field(name = 'Created On', value=f'{ctx.channel.created_at.strftime("%b, %d, %Y")}', inline=False)
    await ctx.send(embed=embed)

@client.command(aliases = ['gi'])
async def guildinfo(ctx):
    embed = discord.Embed(
        title = f'Displaying info for server {ctx.guild.name}', 
        colour = discord.Colour.red()
    )
    icon_url = ctx.guild.icon_url
    embed.set_thumbnail(url=icon_url)
    embed.set_footer(text=f'Guild Id: {ctx.guild.id},  Guild Owner Id {ctx.guild.owner_id}')
    embed.add_field(name = 'Region', value=f'{ctx.guild.region}', inline=False)
    embed.add_field(name = 'AFK Timer', value=f'{ctx.guild.afk_timeout} seconds', inline=True)
    embed.add_field(name = 'AFK Channel', value=f'{ctx.guild.afk_channel}', inline=True)
    embed.add_field(name = 'Verification level', value=f'{ctx.guild.verification_level}', inline=False)
    embed.add_field(name = 'Nitro Tier', value=f'{ctx.guild.premium_tier}', inline=True)
    embed.add_field(name = 'Number of boosts', value=f'{ctx.guild.premium_subscription_count}', inline=True)
    embed.add_field(name = 'Created on', value=f'{ctx.guild.created_at.strftime("%b, %d, %Y")}', inline=False)

    await ctx.send(embed=embed)



#@client.command()
#async def coherent(ctx):
    #embed = discord.Embed(
        #title = 'Dont do it!', 
        #description = 'dont check neils oldest message in the bruh moment group chat',
        #colour = discord.Colour.gold()
    #)
    #await ctx.send(embed=embed)

#cogs :skull: -------------------------------------------------------------------------------------------------------------



@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3 ]}')

client.run('ODEyNDI2Njk2MDE0OTU0NDk2.YDAlUg.JMiuaHRs6Fw4LolCzdX_Hrm5vhM')