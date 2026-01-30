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
def start_workout_session(workout_data):
    """
    Create an embed for the current exercise in the workout
    
    Args:
        workout_data: Dict with 'exercises', 'current_exercise_index', and 'workout_name'
    """
    exercises = workout_data["exercises"]
    current_index = workout_data["current_exercise_index"]
    
    # Get the current exercise
    data = exercises[current_index]
    
    exercise_name = data.get("exercise_name", "Unknown Exercise")
    sets = data.get("sets", [])
    now = datetime.datetime.utcnow()
    formatted_time = now.strftime("%b %d | %I:%M %p")

    # Tighter widths for mobile (iPhone)
    S_W = 3   # Set
    R_W = 4   # Reps
    W_W = 9   # Weight
    E_W = 3   # RPE
    GAP = " "

    header = f"  {'#':<{S_W}}{GAP}{'Reps':<{R_W}}{GAP}{'Weight':<{W_W}}{GAP}{'RPE'}"
    separator = "─" * 28

    rows = ""
    for i, s in enumerate(sets, start=1):
        arrow = "→" if i == data["current_set"] + 1 else " "
        w_str = f"{s['weight']}lbs"
        
        rows += (
            f"{arrow} {i:<{S_W}}{GAP}"
            f"{s['reps']:<{R_W}}{GAP}"
            f"{w_str:<{W_W}}{GAP}"
            f"{s['rpe']}\n"
        )

    exercise_progress = f"Exercise {current_index + 1}/{len(exercises)}"
    
    footer = f"{formatted_time}\n{exercise_progress}\nTotal Sets: {len(sets)}\nTip: Focus on full ROM"
    table = f"{header}\n{separator}\n{rows}{separator}\n{footer}"
    
    code_block = f"```\n{table}\n```"

    import discord
    embed = discord.Embed(
        title=f"📝 {exercise_name}",
        description=code_block,
        color=0x3498DB
    )

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
    # data is expected to be a list of exercise dicts

    if not data:
        return discord.Embed(
            title="➕ NEW PLAN",
            description="Create a new workout plan"
        )

    embed = discord.Embed(
        title="Workout Plan",
        color=0x3498DB
    )

    lines = []
    lines.append("#  Exercise        Sets  Reps   RPE")
    lines.append("────────────────────────────────")

    for index, exercise in enumerate(data, start=1):
        exercise_name = exercise["exercise_name"]
        sets_count = exercise["sets_count"]
        reps_count = exercise["reps_count"]
        rpe = exercise.get("rpe", "-")

        table_row = (
            f"{index:<2} "
            f"{exercise_name:<15} "
            f"{sets_count:<5} "
            f"{reps_count:<6} "
            f"{rpe}"
        )

        lines.append(table_row)

    embed.description = "```text\n" + "\n".join(lines) + "\n```"
    return embed
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
    "edit_plan": adjust_embed,
    "exit_plan": new_plan_embed,
    "adjust": workout_plans_list_embed,

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
