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
# MONGODB CONNECTION STRING
DBB = ""

DB = "test"
COLL = "users"

# DISCORD SERVER ID
DISCORD_ID = 719778731715198986

# CHANNELS
LOG_CHANNEL = 738103615067127978        # Channel where all join and verification logs will be posted
VERIFY_CHANNEL = 704567590680264766     # Channel where manual verification requests are sent to be approved or denied
TICKET_CHANNEL = 738643081540141137     # Channel Catergory where ticket channels will be created
ARCHIVE_CHANNEL = 738643120912072704    # Channel Catergory where closed tickets will be moved to

# ROLES
NEW_ROLE = 701904104334688426           # The role which new users join with
HACKER_ROLE = 694558870990749717        # Hacker role
MENTOR_ROLE = 738643229330898975        # Mentor role
UNI_ROLE = 703643388162998332           # University role
HS_ROLE = 695678770564300932            # Highschool role
ADMIN_ROLES = [738105099737628712]     # Roles which have admin permissions

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

# Commented out for now
# @bot.event
# async def on_member_join(member):
#     client = MongoClient(DBB)
#     role_new = discord.utils.get(member.guild.roles, id=NEW_ROLE)
#     await member.add_roles(role_new)
#     await member.create_dm()
#     channel = bot.get_channel(LOG_CHANNEL)
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to the Ru Hacks Discord.'
#     )
#     logging.warning(f'{member} joined')
#     db = client[DB]
#     col = db[COLL]
#     flag = False
#     for i in col.find():
#         try:
#             if str(member) in i["confirmation"]["discord"]:
#                 flag = True
#                 await member.remove_roles(role_new)
#                 roles = ""
#                 role_hacker = discord.utils.get(member.guild.roles, id=HACKER_ROLE)
#                 role_mentor = discord.utils.get(member.guild.roles, id=MENTOR_ROLE)
#                 role_uni = discord.utils.get(member.guild.roles, id=UNI_ROLE)
#                 role_hs = discord.utils.get(member.guild.roles, id=HS_ROLE)
#                 try:
#                     if (i["profile"]["hsStudent"] == True):
#                         await member.add_roles(role_hs)
#                         roles = "High School Student, "
#                     elif (i["profile"]["hsStudent"] == False):
#                         await member.add_roles(role_uni)
#                         roles = "University Student, "
#                 except:
#                     await member.dm_channel.send(
#                     f'\nERROR: Contact an organizer  '
#                     )
#                     roles += "error"
#                 try:
#                     if (i["profile"]["isMentor"] == True):
#                         await member.add_roles(role_mentor)
#                         roles += "and Mentor"
#                     elif (i["profile"]["isMentor"] == False):
#                         await member.add_roles(role_hacker)
#                         roles += "and Hacker"
#                 except:
#                     await member.dm_channel.send(
#                     f'\nERROR: Contact an organizer  '
#                     )
#                     roles += "error"
#                 try:
#                     name = i["profile"]["name"]
#                 except: 
#                     name = "NoNAME"
#                 try:
#                     email = i["email"]
#                 except:
#                     email = "NOEMAIL"

#                 fullname = name.split()
#                 if len(fullname) > 1:
#                     firstname = fullname[0]
#                     lastname = fullname[1][0]
#                     nick = firstname + " " + lastname
#                 else:
#                     firstname = fullname[0]
#                     nick = firstname
                
#                 embed = discord.Embed(title="Join Log", description=f"{str(member)}", color=0x00ffff)
#                 embed.add_field(name="Name", value=f"{name}", inline=False)
#                 embed.add_field(name="Email", value=f"{email}", inline=False)
#                 embed.add_field(name="User Roles", value=f"{roles}", inline=False)
                    
#                 await channel.send(embed=embed)
#                 await member.dm_channel.send(
#                 f'\nYou have been given the following roles:\n\n{roles}'
#                 )
                
#                 await member.edit(nick=nick)
#                 logging.warning(f'{member} - join event, {roles}, {name}, {email}')
#                 break
#         except:
#             print("Error in join event")
#             logging.warning(f'{member} - join event error')
#     if flag == False:
#         await member.dm_channel.send(
#         f'Your discord has not been found in our database. But do not worry! I got your back!\n This just means I need your email to verify you, by using the following command.\n\n$check <email> \n Example: $check ahmad@ryerson.ca'
#         )
#         logging.warning(f'{member} - join event not found')
            

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
            rand = "ticket"+"-"+str(len(num_tickets))+"-"+str(ctx.author.name)
            category = bot.get_channel(TICKET_CHANNEL)

            channel = await ctx.guild.create_text_channel(rand, category=category)
            await channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
            mentions = ""
            hacker_names = ""
            for i in args:
                await channel.set_permissions(i, read_messages=True, send_messages=True)
                mentions += str(i.mention) + " "
                hacker_names += str(i.name) + " "

            await channel.edit(topic = f"Mentor: {ctx.author.name} || Hackers: {hacker_names}")

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
async def check(ctx, email):
    client = MongoClient(DBB)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send("Private command only")
    else:
        db = client[DB]
        col = db[COLL]
        channel = bot.get_channel(LOG_CHANNEL)
        flag = False
        for i in col.find():
            if email == i["email"]:
                if(i["confirmation"]["discord"] == ""):
                    flag = True
                    roles = ""
                    ctx1 = bot.get_guild(DISCORD_ID)
                    member = ctx1.get_member(ctx.message.author.id)
                    role_new = discord.utils.get(ctx1.roles, id=NEW_ROLE)
                    role_hacker = discord.utils.get(ctx1.roles, id=HACKER_ROLE)
                    role_mentor = discord.utils.get(ctx1.roles, id=MENTOR_ROLE)
                    role_uni = discord.utils.get(ctx1.roles, id=UNI_ROLE)
                    role_hs = discord.utils.get(ctx1.roles, id=HS_ROLE)
                    col.update_one({"email": i["email"]}, {"$set": {"confirmation": {"discord": str(ctx.author)}}})
                    await member.remove_roles(role_new)
                    try:
                        if (i["profile"]["hsStudent"] == True):
                            await member.add_roles(role_hs)
                            roles = "High School Student, "
                        elif (i["profile"]["hsStudent"] == False):
                            await member.add_roles(role_uni)
                            roles = "University Student, "
                    except:
                        await ctx.send(
                        f'\nError: Contact an organizer'
                        )
                        roles += "error"
                    try:
                        if (i["profile"]["isMentor"] == True):
                            await member.add_roles(role_mentor)
                            roles += "and Mentor"
                        elif (i["profile"]["isMentor"] == False):
                            await member.add_roles(role_hacker)
                            roles += "and Hacker"
                    except:
                        await ctx.send(
                        f'\nError: Contact an organizer'
                        )
                        roles += "error"
                    try:
                        name = i["profile"]["name"]
                    except: 
                        name = "NoNAME"
                    fullname = name.split()
                    if len(fullname) > 1:
                        firstname = fullname[0]
                        lastname = fullname[1][0]
                        nick = firstname + " " + lastname
                    else:
                        firstname = fullname[0]
                        nick = firstname
                    
                    embed = discord.Embed(title="Join Log", description=f"{str(ctx.author)}", color=0x00ffff)
                    embed.add_field(name="Name", value=f"{name}", inline=False)
                    embed.add_field(name="Email", value=f"{email}", inline=False)
                    embed.add_field(name="User Roles", value=f"{roles}", inline=False)
                    
                    await channel.send(embed=embed)
                    await ctx.send(
                    f'\nYou have been given the following roles:\n\n{roles}'
                    )
                    await member.edit(nick=nick)
                    logging.warning(f'{ctx.author} - check success, {name},{email},{roles}')
                    break
                else:
                    flag = True
                    await ctx.send("The discord under this email does not match the discord you have joined with. Do not worry though!\nPlease use the following command\n\n$request <EMAIL: required> <REASON: optional>\nExample: $request ahmad@ryerson.ca I have changed my discord name")
                    logging.warning(f'{ctx.author} - check failed wrong discord')
        if flag == False:
            await ctx.send("Email not found in our database, please contact an organizer directly in the welcome channel, thanks!")
            logging.warning(f'{ctx.author} - check failed email not found in DB')

@bot.command()
async def request(ctx, *args):
    client = MongoClient(DBB)
    db = client[DB]
    col = db[COLL]
    email = args[0]
    reason = ""
    channel = bot.get_channel(VERIFY_CHANNEL)
    print(len(args))
    if len(args) > 1:
        reason = " ".join(args[1:])
    flag = False
    for i in col.find():
        if email == i["email"]:
            flag = True
            try:
                if (i["profile"]["hsStudent"] == True):
                    roles = "High School Student, "
                elif (i["profile"]["hsStudent"] == False):
                    roles = "University Student, "
            except:
                await ctx.send("ERROR: Contact an organizer")
                roles = "error"
            try:
                if (i["profile"]["isMentor"] == True):
                    roles += "and Mentor"
                elif (i["profile"]["isMentor"] == False):
                    roles += "and Hacker"
            except:
                await ctx.send("ERROR: Contact an organizer")
                roles = "error"
            try:
                name = i["profile"]["name"]
            except: 
                name = "NoNAME"
            discord_id = i["confirmation"]["discord"]
            
            embed = discord.Embed(title="Verification Request", description=f"{ctx.author}", color=0x00ffff)
            embed.add_field(name="Name", value=f"{name}", inline=False)
            embed.add_field(name="Email", value=f"{email}", inline=False)
            if len(discord_id) > 0:
                embed.add_field(name="Discord", value=f"{discord_id}", inline=False)
            else:
                embed.add_field(name="Discord", value=f"No Discord found in the database", inline=False)
            embed.add_field(name="User Roles", value=f"{roles}", inline=False)
            if len(reason) > 0:
                embed.add_field(name="Reason Given", value=f"{reason}", inline=False)
            else:
                embed.add_field(name="Reason Given", value=f"No reason given", inline=False)
            await channel.send(embed=embed)
            await ctx.send("Your request has been sent to our admins, please stay tight, we got you")
            logging.warning(f'{ctx.author} - request, {name}, {email}, {roles}')
            break
    if flag == False:
        await ctx.send("Email not found in our database, please contact an organizer directly, thanks!")
        logging.warning(f'{ctx.author} - request email not found')

@bot.command()
async def verify(ctx, i: discord.Member, *args):
    flag = True
    perm_role = []
    for i in ADMIN_ROLES:
        perm_role.append(discord.utils.get(ctx.guild.roles, id=i))
    for i in perm_role:
        if i in ctx.author.roles:
            if(ctx.channel.id == VERIFY_CHANNEL):
                role_new = discord.utils.get(ctx.guild.roles, id=NEW_ROLE)
                await i.remove_roles(role_new)
                roles = []
                role_hacker = discord.utils.get(ctx.guild.roles, id=HACKER_ROLE)
                role_mentor = discord.utils.get(ctx.guild.roles, id=MENTOR_ROLE)
                role_uni = discord.utils.get(ctx.guild.roles, id=UNI_ROLE)
                role_hs = discord.utils.get(ctx.guild.roles, id=HS_ROLE)
                for j in args:
                    if (j == "hs"):
                        await i.add_roles(role_hs)
                        roles.append("High School Student")
                    if (j == "uni"):
                        await i.add_roles(role_uni)
                        roles.append("University Student")
                    if (j == "mentor"):
                        await i.add_roles(role_mentor)
                        roles.append("Mentor")
                    if (j == "hacker"):
                        await i.add_roles(role_hacker)
                        roles.append("Hacker")
                        
                await ctx.send(
                f'\nUser has been given the following roles:\n{" | ".join(roles)}'
                )
                await i.create_dm()
                await i.dm_channel.send(
                    f'\n\nHi {i.name}, your request has been verified, you have been given the following roles:\n{" | ".join(roles)}\n\n Please change your name to first name and the first letter of your last name'
                )
                logging.warning(f'{ctx.author} - verify, {i.name}, {" | ".join(roles)}')
                flag = False
            else:
                pass
    if flag:
        await ctx.send("Invalid permissions")

@bot.command()
async def stream(ctx):
    embed=discord.Embed(title="Stream", url="https://www.ruhacks.com", color=0xff40ff)
    embed.set_author(name="RU Hacks", url="https://www.ruhacks.com")
    embed.set_thumbnail(url="https://www.ruhacks.com/images/RU_White_RU.png")
    embed.add_field(name="Link", value="https://www.twitch.tv/ryersonuhacks", inline=False)
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
    page1 = discord.Embed(title="Day 1 - May 15", url="https://www.ruhacks.com", color=0xff40ff)
    page1.set_author(name="RU Hacks", url="https://www.ruhacks.com")
    page1.set_thumbnail(url="https://www.ruhacks.com/images/RU_White_RU.png")
    for i in lines1:
        i = i.split("|")
        page1.add_field(name=i[1], value=i[0], inline=False)
    page1.set_footer(text="Ru Hacks Bot, :)")

    page2 = discord.Embed(title="Day 2 - May 16", url="https://www.ruhacks.com", color=0xff40ff)
    page2.set_author(name="RU Hacks", url="https://www.ruhacks.com")
    page2.set_thumbnail(url="https://www.ruhacks.com/images/RU_White_RU.png")
    for i in lines2:
        i = i.split("|")
        page2.add_field(name=i[1], value=i[0], inline=False)
    page2.set_footer(text="Ru Hacks Bot, :)")

    page3 = discord.Embed(title="Day 3 - May 17", url="https://www.ruhacks.com", color=0xff40ff)
    page3.set_author(name="RU Hacks", url="https://www.ruhacks.com")
    page3.set_thumbnail(url="https://www.ruhacks.com/images/RU_White_RU.png")
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
