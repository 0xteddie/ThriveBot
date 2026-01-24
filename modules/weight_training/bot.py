# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from ui.embed_presets import EMBEDS, VIEWS

load_dotenv()
TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.tree.command(
    name="workout",
    description="Workout UI",
    guild=discord.Object(id=GUILD_ID)
)
async def workout(interaction: discord.Interaction):
    state = "home"
    data = {}

    embed = EMBEDS[state](data)
    view = VIEWS[state](data)

    await interaction.response.send_message(embed=embed, view=view)

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"Logged in as {bot.user}")

bot.run(TOKEN)

