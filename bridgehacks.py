import os
import discord
import random
import asyncio
from discord.ext import commands
from discord.utils import get
from pymongo import MongoClient
import logging
logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

#==============================================================================#
#                               CONFIG                                         #
#==============================================================================#

# DISCORD BOT TOKEN:
TOKEN = ''
# # MONGODB CONNECTION STRING
# DBB = ""

# DB = "test"
# COLL = "users"

# DISCORD SERVER ID
DISCORD_ID = 665356573572464650

# CHANNELS
# LOG_CHANNEL = 706593175577428030        # Channel where all join and verification logs will be posted
# VERIFY_CHANNEL = 704567590680264766     # Channel where manual verification requests are sent to be approved or denied
TICKET_CHANNEL = 730645395603980299     # Channel Catergory where ticket channels will be created
ARCHIVE_CHANNEL = 730645453594689557    # Channel Catergory where closed tickets will be moved to

# ROLES
# NEW_ROLE = 701904104334688426           # The role which new users join with
# HACKER_ROLE = 694558870990749717        # Hacker role
MENTOR_ROLE = 730266905797197956        # Mentor role
# UNI_ROLE = 703643388162998332           # University role
# HS_ROLE = 695678770564300932            # Highschool role
ADMIN_ROLES = [669436635959787530,673657430353117184,695447042188771423,698220612962746408,730618294343827517]     # Roles which have admin permissions

#==============================================================================#
#                               CONFIG END                                     #
#==============================================================================#

day1 = "day1"
day2 = "day2"
day3 = "day3"

client = discord.Client()
bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def ticket(ctx, *args: discord.Member):
    flag = True
    perm_role = []
    for i in ADMIN_ROLES:
        perm_role.append(discord.utils.get(ctx.guild.roles, id=i))
    perm_role.append(discord.utils.get(ctx.guild.roles, id=MENTOR_ROLE))
    for i in perm_role:
        if i in ctx.author.roles and flag:
            num_tickets =  [line.rstrip('\n') for line in open("ticket")]

            args = list(args)
            rand = "ticket"+"-"+str(len(num_tickets))
            category = bot.get_channel(TICKET_CHANNEL)

            channel = await ctx.guild.create_text_channel(rand, category=category)
            await channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
            mentions = ""
            for i in args:
                await channel.set_permissions(i, read_messages=True, send_messages=True)
                mentions += str(i.mention) + " "
              

            await channel.send(f"Ticket has been created by {ctx.author.mention}.")
            await channel.send(f"Added {mentions}")
            f4 = open("ticket", "a")
            f4.write("1\n")
            f4.close()
            logging.warning(f'{ctx.author} - ran ticket')
            flag = False
    if flag:
        await ctx.send("Invalid permissions")

@bot.command()
async def add(ctx, *args: discord.Member):
    flag = True
    perm_role = []
    for i in ADMIN_ROLES:
        perm_role.append(discord.utils.get(ctx.guild.roles, id=i))
    perm_role.append(discord.utils.get(ctx.guild.roles, id=MENTOR_ROLE))
    for i in perm_role:
        if i in ctx.author.roles:
            if(ctx.channel.category_id == TICKET_CHANNEL):
                args = list(args)
                # print(args)
                mentions = ""
                for i in args:
                    await ctx.channel.set_permissions(i, read_messages=True, send_messages=True)
                    mentions += str(i.mention) + " "
                await ctx.send(f"{ctx.author.mention} added {mentions}")
                logging.warning(f'{ctx.author} - ran add')
                flag = False
            else:
                pass
    if flag:
        await ctx.send("Invalid permissions")

@bot.command()
async def remove(ctx, *args: discord.Member):
    flag = True
    perm_role = []
    for i in ADMIN_ROLES:
        perm_role.append(discord.utils.get(ctx.guild.roles, id=i))
    perm_role.append(discord.utils.get(ctx.guild.roles, id=MENTOR_ROLE))
    for i in perm_role:
        if i in ctx.author.roles:
            if(ctx.channel.category_id == TICKET_CHANNEL):
                args = list(args)
                # print(args)
                mentions = ""
                for i in args:
                    await ctx.channel.set_permissions(i, read_messages=False, send_messages=False)
                    mentions += str(i.mention) + " "
                await ctx.send(f"{ctx.author.mention} removed {mentions}")
                logging.warning(f'{ctx.author} - ran remove')
                flag = False
            else:
                pass
    if flag:
        await ctx.send("Invalid permissions")

@bot.command()
async def done(ctx):
    flag = True
    perm_role = []
    for i in ADMIN_ROLES:
        perm_role.append(discord.utils.get(ctx.guild.roles, id=i))
    perm_role.append(discord.utils.get(ctx.guild.roles, id=MENTOR_ROLE))
    for i in perm_role:
        if i in ctx.author.roles:
            if(ctx.channel.category_id == TICKET_CHANNEL):
                category = bot.get_channel(ARCHIVE_CHANNEL)
                await ctx.channel.edit(category=category)
                await ctx.channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
                for i in ctx.channel.members:
                    await ctx.channel.set_permissions(i, read_messages=True, send_messages=False)
                flag = False
            else:
                pass
    if flag:
        await ctx.send("Invalid permissions")


@bot.command()
async def stream(ctx):
    embed=discord.Embed(title="Stream", url="https://www.bridgehacks.com", color=0xff40ff)
    embed.set_author(name="BridgeHacks", url="https://www.bridgehacks.com")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/730870402880110693/733478662690570310/bridgehacks-logo.png")
    embed.add_field(name="Link", value="https://youtu.be/2T7ZUBcpYyI", inline=False)
    embed.set_footer(text="Ru Hacks Bot, :)")
    await ctx.send(embed=embed)

@bot.command()
async def addschedule(ctx, *args):
    perm_role = []
    for i in ADMIN_ROLES:
        perm_role.append(discord.utils.get(ctx.guild.roles, id=i))
    for i in perm_role:
        if i in ctx.author.roles:
            if len(args) > 1:
                arg = " ".join(args[1:])
                argtest = arg.split("|")
                if len(argtest) > 1:
                    with open(args[0], "a+") as f:
                        f.write(arg + "\n")
                    await ctx.send("Added Successfully")
                else:
                    await ctx.send("Wrong Usage")
            else:
                await ctx.send("Wrong Usage")
    

@bot.command()
async def delschedule(ctx, *args):
    perm_role = []
    for i in ADMIN_ROLES:
        perm_role.append(discord.utils.get(ctx.guild.roles, id=i))
    for i in perm_role:
        if i in ctx.author.roles:
            if len(args) == 2 and int(args[1]) > 0 and int(args[1]) < 4:
                numdel = int(args[1])
                with open(args[0]) as f:
                    lines = [line.rstrip() for line in f]
                del lines[numdel - 1]
                with open(args[0], 'w') as f:
                    for item in lines:
                        f.write(item + "\n")
                await ctx.send("Removed Successfully")
            else:
                await ctx.send("Wrong Usage")
    

@bot.command()
async def schedule(ctx):
    with open(day1) as f:
        lines1 = [line.rstrip() for line in f]
    with open(day2) as f:
        lines2 = [line.rstrip() for line in f]  
    with open(day3) as f:
        lines3 = [line.rstrip() for line in f]   
    page1 = discord.Embed(title="Day 1 - July 17", url="https://www.ruhacks.com", color=0xff40ff)
    page1.set_author(name="BridgeHacks", url="https://www.bridgehacks.com")
    page1.set_thumbnail(url="https://media.discordapp.net/attachments/730870402880110693/733478662690570310/bridgehacks-logo.png")
    for i in lines1:
        i = i.split("|")
        page1.add_field(name=i[1], value=i[0], inline=False)
    page1.set_footer(text="Ru Hacks Bot, :)")

    page2 = discord.Embed(title="Day 2 - July 18", url="https://www.ruhacks.com", color=0xff40ff)
    page2.set_author(name="BridgeHacks", url="https://www.bridgehacks.com")
    page2.set_thumbnail(url="https://media.discordapp.net/attachments/730870402880110693/733478662690570310/bridgehacks-logo.png")
    for i in lines2:
        i = i.split("|")
        page2.add_field(name=i[1], value=i[0], inline=False)
    page2.set_footer(text="Ru Hacks Bot, :)")

    page3 = discord.Embed(title="Day 3 - July 19", url="https://www.ruhacks.com", color=0xff40ff)
    page3.set_author(name="BridgeHacks", url="https://www.bridgehacks.com")
    page3.set_thumbnail(url="https://media.discordapp.net/attachments/730870402880110693/733478662690570310/bridgehacks-logo.png")
    for i in lines3:
        i = i.split("|")
        page3.add_field(name=i[1], value=i[0], inline=False)
    page3.set_footer(text="Ru Hacks Bot, :)")

    pages = [page1, page2, page3]
    message = await ctx.send(embed=page1)

    
    await message.add_reaction('\u25c0')
    await message.add_reaction('\u25b6')
    await message.add_reaction('\u23ed')

    i = 0
    emoji = ''

    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0) 
            if user == ctx.author: 
                emoji = str(reaction.emoji)
                if emoji == '\u25c0':
                    if i > 0:
                        i -= 1
                        await message.edit(embed=pages[i])
                elif emoji == '\u25b6':
                    if i < 2:
                        i += 1
                        await message.edit(embed=pages[i]) 
            if client.user != user:
                await message.remove_reaction(reaction, user) 
        except asyncio.TimeoutError:
            break
    await message.clear_reactions()
    

# @bot.command()
# async def message_role(ctx, message):
#     for member in ctx.guild.members:
#         role_new = discord.utils.get(member.guild.roles, id=NEW_ROLE)
#         if role_new in member.roles:
#             try:
#                 channel = await member.create_dm()
#                 await channel.send("Your discord has not been found in our database. But do not worry! I got your back!\n This just means I need your email to verify you, by using the following command.\n\n$check <email> \n Example: $check ahmad@ryerson.ca")
#             except:
#                 print(1111)

bot.run(TOKEN)
