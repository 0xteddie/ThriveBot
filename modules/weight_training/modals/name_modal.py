# modals/name_modal.py
import discord

class NamePlanModal(discord.ui.Modal, title="Name Your Workout Plan"):
    plan_name = discord.ui.TextInput(
        label="Workout name",
        placeholder="e.g. Push Day",
        max_length=25
    )

    def __init__(self, data):
        super().__init__()
        self.data = data

    async def on_submit(self, interaction: discord.Interaction):
        # store input (perform validation)
        self.data["plan_name"] = self.plan_name.value

        # transition state
        from ui.render import render
        await render(interaction, "new_plan", self.data)


class PlanDetails(discord.ui.Modal, title="Exercise details"):
    exercise_name = discord.ui.TextInput(
        label="Exercise Name: ",
        placeholder="e.g. Pull up, Push ups",
        max_length=25
    )
    sets_count = discord.ui.TextInput(
        label="Total Sets: ",
        max_length=3
    )
    reps_count = discord.ui.TextInput(
        label="Total Reps: ",
        max_length=3
    )

    def __init__(self, data):
        super().__init__()
        self.data = data

    # Return in a dict? 
    async def on_submit(self, interaction: discord.Interaction):
        # Used this structure for back-end writing.
        # data = []
        # I will also need the work_out_plan id for this structure.
        # {"exercise_name": name, "sets": sets, "reps": reps, "id": exercise_id}
        self.data["exercise_name"] = self.exercise_name.value
        self.data["sets_count"] = self.sets_count.value
        self.data["reps_count"] = self.reps_count.value

        # Send the info back to the embed with the new data
        from ui.render import render
        await render(interaction, "new_plan", self.data)