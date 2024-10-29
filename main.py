import disnake
from disnake.ext import commands, tasks
import json
from flask import Flask
from threading import Thread
import os
import asyncio
import random

intents = disnake.Intents.default()
bot = commands.Bot(command_prefix='c+', intents=intents, help_command=None)
authorized_user_id = 723256412674719795
json_file = "uuids.json"
user_stats = {}

app = Flask('')

@app.route('/')
def main():
    return f"Logged in as {bot.user}."

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

keep_alive()

if not os.path.exists(json_file):
    with open(json_file, "w") as f:
        json.dump([], f)

def load_uuids():
    with open(json_file, "r") as f:
        return json.load(f)

def save_uuids(data):
    with open(json_file, "w") as f:
        json.dump(data, f, indent=4)

def save_stats():
    with open('user_stats.json', 'w') as f:
        json.dump(user_stats, f, indent=4)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")
    statut.start()
    
    for guild in bot.guilds:
        for channel in guild.text_channels:
            async for message in channel.history(limit=None): 
                if message.author.bot:
                    continue
                
                if message.author.id not in user_stats:
                    user_stats[message.author.id] = {
                        "messages": 0,
                        "voice_time": 0
                    }

                user_stats[message.author.id]["messages"] += 1
    
    save_stats()

@tasks.loop(seconds=3)
async def statut():
    activity_list = ["discord.gg/miyakofr", "c+help", "Made By Mxtsouko"]
    selected = random.choice(activity_list)
    status_list = [disnake.Status.idle, disnake.Status.do_not_disturb, disnake.Status.online]
    selected_status = random.choice(status_list)

    await bot.change_presence(
        status=selected_status,
        activity=disnake.Activity(
            type=disnake.ActivityType.streaming,
            name=selected,
            url='https://www.twitch.tv/mxtsouko'
        )
    )

embed_color = 0x383d53

@bot.command()
async def add(ctx, uuid: str):
    if ctx.author.id != authorized_user_id:
        return
    uuids = load_uuids()
    uuids.append(uuid)
    save_uuids(uuids)
    embed = disnake.Embed(title="UUID Added", description=f"L'UUID `{uuid}` a été ajouté.", color=embed_color)
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)

@bot.command()
async def delete(ctx, uuid: str):
    if ctx.author.id != authorized_user_id:
        return
    uuids = load_uuids()
    if uuid in uuids:
        uuids.remove(uuid)
        save_uuids(uuids)
        embed = disnake.Embed(title="UUID Deleted", description=f"L'UUID `{uuid}` a été supprimé.", color=embed_color)
    else:
        embed = disnake.Embed(title="Error", description=f"L'UUID `{uuid}` n'existe pas.", color=embed_color)
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)

@bot.command()
async def tempdel(ctx, uuid: str):
    if ctx.author.id != authorized_user_id:
        return
    uuids = load_uuids()
    if uuid in uuids:
        uuids.remove(uuid)
        save_uuids(uuids)
        embed = disnake.Embed(title="UUID Temporarily Deleted", description=f"L'UUID `{uuid}` a été supprimé temporairement.", color=embed_color)
    else:
        embed = disnake.Embed(title="Error", description=f"L'UUID `{uuid}` n'existe pas.", color=embed_color)
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)
    await asyncio.sleep(300)
    uuids.append(uuid)
    save_uuids(uuids)

@bot.command()
async def show(ctx):
    if ctx.author.id != authorized_user_id:
        return
    uuids = load_uuids()
    embed = disnake.Embed(title="UUID List", description="Voici les UUID stockés dans le fichier JSON:", color=embed_color)
    embed.add_field(name="UUIDs", value="\n".join(uuids) if uuids else "Aucun UUID enregistré.", inline=False)
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    if ctx.author.id != authorized_user_id:
        return
    embed = disnake.Embed(title="ChimeraWL Help", color=embed_color)
    embed.add_field(name="+c add <uuid>", value="Ajoute un UUID dans le fichier JSON.", inline=False)
    embed.add_field(name="+c del <uuid>", value="Supprime un UUID spécifique du fichier JSON.", inline=False)
    embed.add_field(name="+c tempdel <uuid>", value="Supprime temporairement un UUID (5 minutes) du fichier JSON.", inline=False)
    embed.add_field(name="+c show", value="Affiche tous les UUID stockés dans le fichier JSON.", inline=False)
    embed.add_field(name="+c help", value="Affiche ce message d'aide.", inline=False)
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    await ctx.send(embed=embed)


bot.run(os.getenv('TOKEN'))
