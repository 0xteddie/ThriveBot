import discord, datetime

def new_plan_embed(data):
    # Should contain the data and values being returned by the user.
    embed_data = {
        "description": "Create a new workout plan",
        "Title": "➕ NEW PLAN"
    }

    if not data or not data.get("data"):
        return discord.Embed(title=embed_data['Title'], description="Create a new workout plan")
    else:
        plan_name = data["plan_name"]
        plan_info = data["data"][plan_name]
        
        embed = discord.Embed(
            title=plan_name,
            color=0x3498DB
        )

        # Add split and focus info if available
        if plan_info.get("split") or plan_info.get("focus"):
            embed.add_field(
                name="Plan Info",
                value=f"Split: {plan_info.get('split', 'Not set')} | Focus: {plan_info.get('focus', 'Not set')}",
                inline=False
            )

        lines = []
        lines.append("#  Exercise           Sets  Reps      RPE")
        lines.append("──────────────────────────────────────────")

        exercises = plan_info["exercises"]
        
        if not exercises:
            lines.append("No exercises added yet.")
        else:
            for exercise_index, exercise_data in enumerate(exercises, start=1):
                exercise_name = exercise_data["exercise_name"]
                sets_count = exercise_data["sets_count"]
                reps_count = exercise_data["reps_count"]
                rpe = exercise_data.get("rpe", 7)

                table_row = (
                    f"{exercise_index:<2} "
                    f"{exercise_name:<18} "
                    f"{sets_count:<5} "
                    f"{reps_count:<9} "
                    f"{rpe}"
                )

                lines.append(table_row)

        embed.description = "```text\n" + "\n".join(lines) + "\n```"
        return embed
