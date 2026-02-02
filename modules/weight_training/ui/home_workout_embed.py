import discord, datetime

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