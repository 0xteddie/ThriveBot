import discord
from discord.ext import commands
from weight_training import write_workout_set
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()  # Loads the .env file
TOKEN = os.getenv('TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
GUILD_ID = int(os.getenv('GUILD_ID'))


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
 
sent_once = False

# Embed that will change whenever a button is clicked.
# This embed will change from two commands.
# 1. Whenever a "skip" button is clicked
# 2. Whenever a "next" button is clicked.
# 3. A function is required for counting the total number of sets the current user is on.
def build_embed(status: str) -> discord.Embed:
    # Embed description should be mallable and changeable
    # Should be pulling information from exercise database.
    embed = discord.Embed(
        title="SET 1",
        description="Exercise: Squat\nTarget: 185 lb × 8 reps",
        color=0x1ABC9C
    )
    embed.add_field(name="Status", value=status, inline=False)
    return embed

class SetView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="▶️ Start", style=discord.ButtonStyle.primary, custom_id="set:start")
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        # change the clicked button
        button.label = "✅ Start"
        button.style = discord.ButtonStyle.success

        # show a confirmation popup with Yes/No (This is creating a new embed when it should just be updating it.)
        # I don't want a new embed to be created.
        await interaction.response.edit_message(
            embed=build_embed("Finished?"),
            view=ConfirmCompleteView(parent=self),
            
        )

    # When click move onto the next set.
    @discord.ui.button(label="⏭️ Next", style=discord.ButtonStyle.secondary, custom_id="set:next")
    async def next_set(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=build_embed("⏭️ Next Set"), view=self)


class ConfirmCompleteView(discord.ui.View):
    """Ephemeral: asks 'Completed fully?' -> Yes closes, No opens Adjust."""
    def __init__(self, parent: SetView):
        super().__init__(timeout=60)
        self.parent = parent


    @discord.ui.button(label="✅ Complete", style=discord.ButtonStyle.success, custom_id="set:complete_set")
    async def complete_set(self, interaction: discord.Interaction, button: discord.ui.Button):

        # ACK immediately (prevents "interaction failed")
        await interaction.response.defer()  # or defer(thinking=True)

        # Fetch all the right information per specific set.
        await write_workout_set(
            user_id=str(interaction.user.id),
            workout_id=1,
            workout_exercise_id=10,
            set_number=1,
            reps=8,
            weight=185.0,
            date_id="2025-12-22"
        )

        await interaction.edit_original_response(
            embed=build_embed("✅ Logged as complete. Moving onto the next one."),
            view=None
        )

    @discord.ui.button(label="🛠️ Adjust", style=discord.ButtonStyle.danger, custom_id="set:complete_no")
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            embed=build_embed("Adjusting set."),
            view=AdjustView(parent=self.parent)
        )

class AdjustView(discord.ui.View):
    """Ephemeral: Increase / Decrease buttons."""
    def __init__(self, parent: SetView):
        super().__init__(timeout=120)
        self.parent = parent
        self.delta = 0  # example adjustment value

    def _embed(self):
        # Shows the output code to the embed
        return build_embed(f"Adjust: {self.delta:+d} (example)")

    @discord.ui.button(label="➕ Increase", style=discord.ButtonStyle.primary, custom_id="set:inc")
    async def inc(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.delta += 1
        await interaction.response.edit_message(embed=self._embed(), view=self)

    @discord.ui.button(label="➖ Decrease", style=discord.ButtonStyle.secondary, custom_id="set:dec")
    async def dec(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.delta -= 1
        await interaction.response.edit_message(embed=self._embed(), view=self)

    @discord.ui.button(label="💾 Save", style=discord.ButtonStyle.success, custom_id="set:save")
    async def save(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Save self.delta to DB / apply to set here
        await interaction.response.edit_message(embed=build_embed("✅ Adjustment saved."), view=None)
        
    # To-do: Next button should prompt the user and ask if they completed all sets
    # Will work with the back-end here to save to the database.

@bot.event
async def on_ready():
    global sent_once
    if sent_once:
        return
    sent_once = True

    print(f"✅ Logged in as {bot.user}")

    channel = bot.get_channel(CHANNEL_ID)
    print(channel)
    if channel is None:
        print("❌ Channel not found. Check CHANNEL_ID and permissions.")
        return

    await channel.send(embed=build_embed("⏳ Pending"), view=SetView())

bot.run(TOKEN)
