import json
from discord.utils import get
import asyncio
import os
import requests
import discord
from discord.ext import commands
token = ""
CONFIG_FILE = 'servers.json'
bot = discord.Bot()
ccid = 
def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def add_server_to_config(servername, serverip):
    config = load_config()
    config[servername] = {
        "name": servername,
        "ip": serverip,
        "top_online": None,
        "owners": [],
        "developers": [],
        "managers": [],
        "website": "",
        "discord": "",
        "channel_id": None
    }
    save_config(config)

def info_server_from_config(servername, info_type):
    config = load_config()
    if servername in config:
        if info_type in config[servername]:
            return config[servername][info_type]
        else:
            return "Invalid info type."
    else:
        return f"Server {servername} not found."
def set_channel_id(servername, channel_id):
    config = load_config()
    if servername in config:
        config[servername]["channel_id"] = channel_id
        save_config(config)
def get_server_names():
    config = load_config()
    return list(config.keys())

def delete_server(servername):
    config = load_config()
    if servername in config:
        del config[servername]
        save_config(config)
        print(f"Server {servername} deleted.")
    else:
        print(f"Server {servername} not found.")

def set_top_online(servername, top_online):
    config = load_config()
    if servername in config:
        config[servername]["top_online"] = top_online
        save_config(config)
        print(f"Top online for {servername} set to {top_online}.")
    else:
        print(f"Server {servername} not found.")

def add_owner(servername, *names):
    config = load_config()
    if servername in config:
        config[servername]["owners"].extend(names)
        save_config(config)
        print(f"Owners {', '.join(names)} added to {servername}.")
    else:
        print(f"Server {servername} not found.")

def add_developer(servername, *names):
    config = load_config()
    if servername in config:
        config[servername]["developers"].extend(names)
        save_config(config)
        print(f"Developers {', '.join(names)} added to {servername}.")
    else:
        print(f"Server {servername} not found.")

def add_manager(servername, *names):
    config = load_config()
    if servername in config:
        config[servername]["managers"].extend(names)
        save_config(config)
        print(f"Managers {', '.join(names)} added to {servername}.")
    else:
        print(f"Server {servername} not found.")

def add_website(servername, website):
    config = load_config()
    if servername in config:
        config[servername]["website"] = website
        save_config(config)
        print(f"Website for {servername} set to {website}.")
    else:
        print(f"Server {servername} not found.")

def add_discord(servername, discord_link):
    config = load_config()
    if servername in config:
        config[servername]["discord"] = discord_link
        save_config(config)
        print(f"Discord link for {servername} set to {discord_link}.")
    else:
        print(f"Server {servername} not found.")

@commands.has_permissions(administrator=True)@bot.command()
async def add_server(ctx, servername: str, serverip: str):
    add_server_to_config(servername, serverip)
    await ctx.respond(f"Server {servername} successfully added.")

@commands.has_permissions(administrator=True)
@bot.command()
async def add_info(ctx,info : discord.Option(str, choices=(["discord","site"])),link , server: str = discord.Option(choices=get_server_names())):

   if info == "discord":
       add_discord(server,"link")
       await ctx.respond(f"be Server {server} discord {link} add shod")
   elif info == "site":
       add_website(server,"link")
       await ctx.respond(f"be Server {server} website {link} add shod")
@commands.has_permissions(administrator=True)       
@bot.command()
async def add_staff(ctx,info : discord.Option(str, choices=(["owner","developer","manager"])),member : discord.Member , server: str = discord.Option(choices=get_server_names())):
   member1 = member.id
   if info == "owner" :
       add_owner(server,member1)
       await ctx.respond(f"server {server} ba owner {member.mention} add shod")
   elif info == "manager":
       add_manager(server,member1)
       await ctx.respond(f"server {server} ba manager {member.mention} add shod")
   elif info == "developer" :
       add_developer(server,member1)
       await ctx.respond(f"server {server} ba developer {member.mention} add shod")
def info_server_from_config(servername, info_type):
    config = load_config()
    if servername in config:
        return config[servername].get(info_type, "Invalid info type.")
    return f"Server {servername} not found."


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    config = load_config()
    for servername, serverdata in config.items():
        channel_id = serverdata.get("channel_id")
        if channel_id:
            channel = bot.get_channel(channel_id)
            if channel:
                await update_message(channel, servername)
def server_status(address):
    try:

        response = requests.get(f"https://eu.mc-api.net/v3/server/ping/{address}")
        data = response.json()


        if "online" in data and data["online"]:
            version = data.get("version", {}).get("name", "Unknown")
            online_players = data.get("players", {}).get("online", 0)
            max_players = data.get("players", {}).get("max", 0)
        else:
            version, online_players, max_players = "Unknown", 0, 0

        return version, online_players, max_players
    except Exception as e:
        print(f"Error fetching server status: {e}")
        return "Unknown", 0, 0
    
@commands.has_permissions(administrator=True)
@bot.command()
async def create_channel(ctx, server: str = discord.Option(choices=get_server_names())):
    guild = ctx.guild
    category = get(guild.categories, id=ccid)
    if not category:
        await ctx.respond(f"Category with ID {ccid} not found.")
        return

    channel = await guild.create_text_channel(name=server, category=category)
    set_channel_id(server, channel.id)

    await update_message(channel, server)
    await ctx.send(f"Channel created for server {server} and linked to configuration.")

async def update_message(channel, servername):
    config = load_config()
    server_data = config.get(servername, {})
    ip = server_data.get("ip")
    name = server_data.get("name")
    website = server_data.get("website", "Not set")
    discord_link = server_data.get("discord", "Not set")
    owners = server_data.get("owners", [])
    developers = server_data.get("developers", [])
    managers = server_data.get("managers", [])
    top_online = server_data.get("top_online", 0) or 0

    owners_mentions = ", ".join([f"<@{owner_id}>" for owner_id in owners])
    developers_mentions = ", ".join([f"<@{developer_id}>" for developer_id in developers])
    managers_mentions = ", ".join([f"<@{manager_id}>" for manager_id in managers])

    embed_message = await channel.send(embed=discord.Embed(title="Initializing server details...", color=discord.Color.blue()))

    while True:
        version, online_players, max_players = server_status(ip)

        if online_players > top_online:
            top_online = online_players
            server_data["top_online"] = top_online
            save_config(config)

        embed = discord.Embed(
            title="Tracker",
            description=f"💠 {name}",
            color=discord.Color.green()
        )
        embed.add_field(name="<:addres:1345097346601451620> IP Address", value=ip, inline=False)
        embed.add_field(name="<:version:1345098019011428402> Version", value=version, inline=False)  
        embed.add_field(name="<:online:1345097348480630854> Players", value=f"{online_players}/{max_players}", inline=True)
        embed.add_field(name="<:top:1345097342491295787> Top Players", value=str(top_online), inline=True)
        embed.add_field(name="👑 Owner", value=owners_mentions or "Not set", inline=False)
        embed.add_field(name="🦺 Managers", value=managers_mentions or "Not set", inline=False)
        embed.add_field(name="👨‍💻 Developers", value=developers_mentions or "Not set", inline=False)
        embed.add_field(name="🌐 Website", value=website or "Not set", inline=False)
        embed.add_field(name="<:discord:1345097344781258762> Discord", value=discord_link or "Not set", inline=False)
        embed.set_image(url=f"https://api.midline.ir/v2/minecraft/server/banner/{ip}?name={name}")



        await embed_message.edit(embed=embed)

        await asyncio.sleep(3)


bot.run(token)
