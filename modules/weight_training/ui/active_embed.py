import discord, datetime

# -----------------------------MOCK UP------------------------------ #
# This is the current active session running of exercise.
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