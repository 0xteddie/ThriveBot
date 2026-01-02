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
        self.data["data"] = []

        # transition state
        from ui.render import render
        await render(interaction, "new_plan", self.data)


class PlanDetails(discord.ui.Modal, title="Exercise details"):
    """
    Handles exercise detail submission.

    Collects user-entered exercise data (name, sets, reps), appends it to the
    existing plan data structure, and triggers a UI re-render to display the
    updated plan.
    
    """

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
        self.details = {}

    async def on_submit(self, interaction: discord.Interaction):
        # Fetch the data from the user input
        self.details["exercise_name"] = self.exercise_name.value
        self.details["sets_count"] = self.sets_count.value
        self.details["reps_count"] = self.reps_count.value
        
        # Add into list
        self.data['data'].append(self.details)
        self.data['index_selected_value'] = 0
        
        # Send the info back to the embed with the new data
        from ui.render import render
        await render(interaction, "new_plan", self.data)

class EditExerciseDetails(discord.ui.Modal, title="Edit Exercise details"):
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

    def __init__(self, data: dict):
        super().__init__()
        self.data = data
        
        edit_index = data["index_selected_value"]
        
        exercise = data["data"][edit_index]
    
        # Pre-fill inputs with selector value
        self.exercise_name.default = str(exercise.get("exercise_name", ""))
        self.sets_count.default = str(exercise.get("sets_count", ""))
        self.reps_count.default = str(exercise.get("reps_count", ""))
    
