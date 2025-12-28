# ui/presets.py
import discord
from views.buttons_presets import HomeView, StartView, NewPlanView, AdjustView

# --------------- Home embed --------------------------------------- #
def home_embed(data):
    embed = discord.Embed(
        title="🏋️ WORKOUT CONTROL CENTER",
        color=discord.Color.green()
    )

    embed.add_field(
        name="▶️ Start Plan",
        value="Begin your workout session",
        inline=False
    )
    embed.add_field(
        name="🆕 New Plan",
        value="Create a brand-new workout plan",
        inline=False
    )
    embed.add_field(
        name="✏️ Adjust",
        value="Edit an existing workout plan",
        inline=False
    )

    embed.set_footer(text="Workout Bot • Train smarter")
    return embed
# ----------------------------------------------------------- #
def start_embed(data):
    # Show a list of workouts the user currenlty has
    return discord.Embed(title="▶️ START PLAN", description="Ready to begin?")

def adjust_embed(data):
    return discord.Embed(title="✏️ ADJUST PLAN", description="Modify an existing plan")

def new_plan_embed(data):
    # Should contain the data and values being returned by the user.
    embed_data = {
        "description": "Create a new workout plan",
        "Title": "➕ NEW PLAN"
    }

    if not data:
        return discord.Embed(title=embed_data['Title'], description="Create a new workout plan")
    else:
        return discord.Embed(title=data)

EMBEDS = {
    "home": home_embed,
    "start": start_embed,
    "new_plan": new_plan_embed,
    "adjust": adjust_embed,
}

# Views also known as buttons.
VIEWS = {
    "home": HomeView,
    "start": StartView,
    "new_plan": NewPlanView,
    "adjust": AdjustView,
}
