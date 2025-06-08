import discord
from discord.ext import commands
from key import TOKEN

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
async def echo(ctx, *, message):
    await ctx.send(message)

bot.run(TOKEN)