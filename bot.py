import discord
from discord.ext import commands
from key import TOKEN
import requests
import json
from bs4 import BeautifulSoup
import re

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = '!', intents = intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    await bot.change_presence(
        activity=discord.Game(name="!help"),
        status=discord.Status.online
    )
    print(f"Bot is online: {bot.user}")
    print('------')

@bot.command()
async def armory(ctx, *, character_name):
    clean_name = ''.join(char for char in character_name.strip() if char.isalpha())
    if not clean_name:
        await ctx.send("Please try again with a valid name.")
        return
    else:
        upper_name = clean_name[0].upper() + clean_name[1::]
        armory_url = f"https://www.chromiecraft.com/en/armory/?character/ChromieCraft/{upper_name}"
        await ctx.send(f"The armory link for **{upper_name}**:\n<{armory_url}>")

''' TBD
@bot.command()
async def serverstats(ctx):
    server_status = requests.get("https://www.chromiecraft.com/en/server-status/")
    soup = BeautifulSoup(server_status.text, 'html.parser')
    player_count = soup.find('p', class_='lead h4')
    if player_count:
        player_count = player_count.text().strip()
    faction_count = soup.find('p', class_='h4')
    if faction_count:
        faction_count = faction_count.text().strip()
    soup.prettify()

    await ctx.send(f"Quick Chromie Craft Stats:\n{player_count}\nAlliance v Horde (Online numbers)\n{faction_count}")
'''
@bot.command()
async def stonks(ctx):
    items = ["Netherweave-Cloth-21877", "Void-Crystal-22450", "Khorium-Bar-23449"]
    answer = ""
    for item in items:
        try:
            #This is so I can have the above item names work inside both the url and for the user to see in the output.
            item_renamed = "".join(char for char in item.strip().replace('-', ' ') if char)
            pattern = r'[0-9]' #regex to remove numbers
            item_renamed = re.sub(pattern, '', item_renamed)
            pcheck = requests.get(f"https://www.wowauctions.net/auctionHouse/chromie-craft/chromiecraft/mergedAh/{item}")
            pcheck_soup = BeautifulSoup(pcheck.text, 'html.parser')
            script_tag = pcheck_soup.find('script', id='__NEXT_DATA__')
            if script_tag:
                data = json.loads(script_tag.string)
                stats = data['props']['pageProps']['item']['stats']

                gold = 0
                silver = stats['avg_price'] // 100
                copper = stats['avg_price'] % 100
                item_amount = stats['item_count']
                if silver > 100:
                    gold = silver // 100
                    silver = silver % 100

                answer += (f"{item_renamed} - Number: {item_amount} Average Price: {gold}g {silver}s {copper}c\n")
        except Exception as e:
            print(f"Stonks pcheck error: {e}")
            await ctx.send("An error has occured.")

    await ctx.send("Here's the Chromie Industrial Average (CIA)")
    await ctx.send(answer)
    await ctx.send("Source: https://www.wowauctions.net/")

@bot.command()
async def echo(ctx, *, message):
    await ctx.send(message)

bot.run(TOKEN)