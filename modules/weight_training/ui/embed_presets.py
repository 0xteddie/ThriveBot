# ui/presets.py
import discord
import datetime
from views.buttons_presets import HomeView, StartWorkOutView, NewPlanView, AdjustView
from views.buttons_presets import EditExerciseView, ExitPlanView, WorkoutSessionView

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

# -----------------------------MOCK UP------------------------------ #
def start_workout_session(data):
    data = {
        "exercise_name": "Tricep Pushdowns",
        "sets": [
            {"weight": 70, "reps": 12, "rpe": 6},
            {"weight": 100, "reps": 8, "rpe": 7},
            {"weight": 60, "reps": 14, "rpe": 8}
        ]
    }

    exercise_name = data.get("exercise_name", "Unknown Exercise")
    sets = data.get("sets", [])

    # Capture current date/time
    now = datetime.datetime.utcnow()
    formatted_time = now.strftime("%m/%d/%y %I:%M %p")

    # Determine max widths for alignment
    col_set_width = max(len(str(len(sets))), 3)
    col_reps_width = max(max(len(str(s['reps'])) for s in sets), 4)
    col_weight_width = max(max(len(str(s['weight']) + " lbs") for s in sets), 6)
    col_rpe_width = max(max(len(str(s['rpe'])) for s in sets), 3)

    # Build header
    header = f"{'Set':<{col_set_width}}  X  {'Reps':<{col_reps_width}}  {'Weight':<{col_weight_width}}  {'RPE':<{col_rpe_width}}"
    separator = "─" * len(header)

    # Build rows
    rows = ""
    for i, s in enumerate(sets, start=1):
        weight_str = f"{s['weight']} lbs"
        rows += f"{i:<{col_set_width}}  X  {s['reps']:<{col_reps_width}}  {weight_str:<{col_weight_width}}  {s['rpe']:<{col_rpe_width}}\n"

    # Build summary for the bottom of the code block
    Date = f"{formatted_time}"

    Total_sets = f"Total Sets: {len(sets)}"
    
    tip = "Tip: Focus on full range of motion"

    table = f"{header}\n{separator}\n{rows}{separator}\n{Date}\n{Total_sets}\n{tip}"

    # Wrap in code block
    code_block = f"```\n{table}\n```"

    # Create embed
    embed = discord.Embed(
        title=f"📝 {exercise_name}",
        description=code_block,
        color=0x3498DB
    )

    # Thumbnail (replace with actual image URL)
    embed.set_thumbnail(url="https://i.shgcdn.com/c39f9e9e-8e0a-4fa9-9ead-7ab7c3415c9d/-/format/auto/-/preview/3000x3000/-/quality/lighter/")

    return embed


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

    
    current_button_value = data["button_click_count"]

     
    for plan_index, plan in enumerate(data["plans"][current_button_value], start=1):
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
    "start_workout": start_workout_session,
    "new_plan": new_plan_embed,
    "edit_plan": new_plan_embed,
    "exit_plan": new_plan_embed,
    "adjust": adjust_embed,
}

# BUTTONS.
VIEWS = {
    "home": HomeView,
    "start": StartWorkOutView,
    "start_workout": WorkoutSessionView,
    "new_plan": NewPlanView,
    "edit_plan": EditExerciseView,
    "exit_plan": ExitPlanView,
    "adjust": AdjustView,
}
