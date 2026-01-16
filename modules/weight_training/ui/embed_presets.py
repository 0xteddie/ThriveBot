# ui/presets.py
import discord
from views.buttons_presets import HomeView, StartView, NewPlanView, AdjustView
from views.buttons_presets import EditExerciseView, ExitPlanView

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

# ---------------Existing plan--------------------------------------------#
def workout_plans_list_embed(data):
    """
        Builds and returns a Discord embed displaying a fixed-width list of
        the user's saved workout plans.
    """
    embed_data = {
        "description": "Your saved workout plans",
        "title": "📋 EXISTING PLANS"
    }

    # Empty state
    if not data or not data.get("plans"):
        return discord.Embed(
            title=embed_data["title"],
            description="No workout plans found."
        )

    embed = discord.Embed(
        title=embed_data["title"],
        color=0x5865F2
    )

    # Column widths
    PLAN_WIDTH  = 14
    SPLIT_WIDTH = 10
    EX_WIDTH    = 3
    FOCUS_WIDTH = 12

    def format_cell(value, width):
        text = str(value)
        return text[:width].ljust(width)

    lines = []
    lines.append(
        "#  "
        f"{'Plan Name'.ljust(PLAN_WIDTH)} "
        f"{'Split'.ljust(SPLIT_WIDTH)} "
        f"{'Ex'.ljust(EX_WIDTH)} "
        f"{'Focus'.ljust(FOCUS_WIDTH)}"
    )
    lines.append("────────────────────────────────────────")

    for plan_index, plan in enumerate(data["plans"], start=1):
        row = (
            f"{plan_index:<2} "
            f"{format_cell(plan['name'], PLAN_WIDTH)} "
            f"{format_cell(plan['split'], SPLIT_WIDTH)} "
            f"{str(plan['ex']).ljust(EX_WIDTH)} "
            f"{format_cell(plan['focus'], FOCUS_WIDTH)}"
        )
        lines.append(row)

    embed.description = "```text\n" + "\n".join(lines) + "\n```"
    return embed

# ----------------------------------------------------------- #
def adjust_embed(data):
    return discord.Embed(title="✏️ ADJUST PLAN", description="Modify an existing plan")

# ----------------------------------------------------------- #
def new_plan_embed(data):
    # Should contain the data and values being returned by the user.
    embed_data = {
        "description": "Create a new workout plan",
        "Title": "➕ NEW PLAN"
    }

    if not data:
        return discord.Embed(title=embed_data['Title'], description="Create a new workout plan")
    else:
        embed = discord.Embed(
            title=data["plan_name"],
            color=0x3498DB
        )

        lines = []
        lines.append("#  Exercise      Sets  Reps")
        lines.append("──────────────────────────")

        for exercise_index, exercise_data in enumerate(data["data"], start=1):
            exercise_name = exercise_data["exercise_name"]
            sets_count = exercise_data["sets_count"]
            reps_count = exercise_data["reps_count"]

            table_row = (
                f"{exercise_index:<2} "
                f"{exercise_name:<13} "
                f"{sets_count:<5} "
                f"{reps_count}"
            )

            lines.append(table_row)

        embed.description = "```text\n" + "\n".join(lines) + "\n```"
        return embed

# EMBEDS
EMBEDS = {
    "home": home_embed,
    "start": workout_plans_list_embed,
    "new_plan": new_plan_embed,
    "edit_plan": new_plan_embed,
    "exit_plan": new_plan_embed,
    "adjust": adjust_embed,
}

# BUTTONS.
VIEWS = {
    "home": HomeView,
    "start": StartView,
    "new_plan": NewPlanView,
    "edit_plan": EditExerciseView,
    "exit_plan": ExitPlanView,
    "adjust": AdjustView,
}
