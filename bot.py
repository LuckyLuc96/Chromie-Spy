import discord
from discord.ext import commands
from key import TOKEN
import requests
from bs4 import BeautifulSoup


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
    upper_name = clean_name[0].upper() + clean_name[1::]
    if not clean_name:
        await ctx.send("Please try again with a valid name.")
        return
    armory_url = f"https://www.chromiecraft.com/en/armory/?character/ChromieCraft/{upper_name}"
    await ctx.send(f"The armory link for **{upper_name}**:\n<{armory_url}>")

@bot.command()
async def serverstats(ctx):
    server_status = requests.get("https://www.chromiecraft.com/en/server-status/")
    soup = BeautifulSoup(server_status.text, 'html.parser')
    player_count = soup.find('p', class_='lead h4') #All my attempts at using soup.find is returning with None objects. Needs some research
    if player_count:
        player_count = player_count.text().strip()
    faction_count = soup.find('p', class_='h4')
    if faction_count:
        faction_count = faction_count.text().strip()
    soup.prettify()

    await ctx.send(f"Quick Chromie Craft Stats:\n{player_count}\nAlliance v Horde (Online numbers)\n{faction_count}")

@bot.command()
async def stonks(ctx):
    pcheck1 = requests.get("https://www.wowauctions.net/auctionHouse/chromie-craft/chromiecraft/mergedAh/netherweave-cloth-21877")
    pcheck1_soup = BeautifulSoup(pcheck1.text, 'html.parser')
    try:
        data1 = {
            'Amount': pcheck1_soup.find('h3', string='Amount').find_next('td').get_text(strip=True),
            'AvgBuyout': pcheck1_soup.find('h3', string='Average Buyout').find_next ('table').get_text(strip=True),
            'MinBuyout': pcheck1_soup.find('h3', string='Minimum Bid').find_next('table').get_text(strip=True),
            'Monthly': pcheck1_soup.find('h3', string='Monthly Average Price').find_next('table').get_text(strip=True)
        }
        await ctx.send(f"Here's the Chromie Industrial Average (CJIA)\nAmount, Avg Buyout, Min Buyout, Monthly Avg Price\nNetherweave Cloth\n{data1}")
    except Exception as e:
        await ctx.send(f"For various possible reasons, an error occured. Error: {e}")


@bot.command()
async def echo(ctx, *, message):
    await ctx.send(message)

bot.run(TOKEN)