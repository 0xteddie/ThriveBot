# modals/name_modal.py
from .workout_utils import create_exercise, validate_exercise_inputs, create_plan, get_max_weight
from ui.render import render
import discord
import asyncio

class NamePlanModal(discord.ui.Modal, title="Name Your Workout Plan"):
    plan_name = discord.ui.TextInput(
        label="Workout name",
        placeholder="e.g. Push Day",
        max_length=25
    )

    focus = discord.ui.TextInput(
        label="Focus",
        placeholder="e.g. Hypertrophy",
        max_length=25
    )

    split = discord.ui.TextInput(
        label="Split",
        placeholder="e.g. Upper/Lower Split",
        max_length=30
    )

    def __init__(self, data):
        super().__init__()
        self.data = data

    async def on_submit(self, interaction: discord.Interaction):
        # Store the newly created plan in data, used by the "edit_plan" functionality
        self.data["plan_data"] = create_plan(
            self.plan_name.value,
            self.split.value,
            self.focus.value
        )
        
        await render(interaction, "new_plan", self.data)

class PlanDetails(discord.ui.Modal, title="Exercise details"):
    """
    Handles exercise detail submission.

    Collects user-entered exercise data (name, sets, reps, RPE), appends it to the
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
        placeholder="e.g. 4",
        max_length=5
    )
    reps_count = discord.ui.TextInput(
        label="Total Reps: ",
        placeholder="e.g. 6-8 or AMRAP",
        max_length=5
    )

    weight_count = discord.ui.TextInput(
        label="Total Weight: ",
        placeholder="e.g. 10-200 Lbs",
        max_length=5
    )

    rpe = discord.ui.TextInput(
        label="Target RPE (Rate of Perceived Exertion): ",
        placeholder="e.g. 7 or 8",
        max_length=2,
        required=False
    )

    def __init__(self, data):
        super().__init__()
        self.data = data

    async def on_submit(self, interaction: discord.Interaction):
        plan_key = next(iter(self.data['plan_data']))
        
        error = validate_exercise_inputs(
            self.sets_count.value,
            self.reps_count.value,
            self.weight_count.value
        )

        if error:
            msg = await interaction.response.send_message(error)
            await asyncio.sleep(2)
            await interaction.delete_original_response()
            return

        exercise = create_exercise(
            self.exercise_name.value,
            self.sets_count.value,
            self.reps_count.value,
            self.weight_count.value,
            self.rpe.value
        )
        
        self.data['plan_data'][plan_key]['exercises'].append(exercise)
        self.data['index_selected_value'] = 0
        
        await render(interaction, "new_plan", self.data)

class EditExerciseDetails(discord.ui.Modal, title="Edit Exercise details"):
    """
    Handles exercise edit submission.

    Updates the selected exercise entry in the existing plan data structure
    and re-renders the plan view with the modified values.
    
    """

    exercise_name = discord.ui.TextInput(
        label="Exercise Name: ",
        placeholder="e.g. Pull up, Push ups",
        max_length=25
    )
    sets_count = discord.ui.TextInput(
        label="Total Sets: ",
        max_length=5
    )
    reps_count = discord.ui.TextInput(
        label="Total Reps: ",
        max_length=5
    )

    weight_count = discord.ui.TextInput(
        label="Total Weight: ",
        placeholder="e.g. 10-200 Lbs",
        max_length=5
    )

    rpe_count = discord.ui.TextInput(
        label="Target RPE (Rate of Perceived Exertion): ",
        placeholder="e.g. 7 or 8",
        max_length=2,
        required=False
    )

    def __init__(self, data: dict):
        super().__init__()
        self.data = data

        plan_key = next(iter(self.data['plan_data']))
        edit_index = self.data["index_selected_value"]
        
        # Exercise here needs to change.
        exercise = self.data["plan_data"][plan_key]["exercises"][edit_index]
        
        # Pre-fill inputs with selector value
        self.exercise_name.default = str(exercise.get("exercise_name", ""))
        self.sets_count.default = str(exercise.get("sets_count", ""))
        self.reps_count.default = str(exercise.get("reps_count", ""))
        self.weight_count.default = str(get_max_weight(exercise['sets']))
        self.rpe_count.default = str(exercise.get("rpe"))
        
    async def on_submit(self, interaction: discord.Interaction):
        edit_index = self.data["index_selected_value"]
        plan_key = next(iter(self.data['plan_data']))

        error = validate_exercise_inputs(
            self.sets_count.value,
            self.reps_count.value,
            self.weight_count.value
        )    
        
        if error:
            msg = await interaction.response.send_message(error)
            await asyncio.sleep(2)
            await interaction.delete_original_response()
            return
        
        # Delete old item from list.
        del self.data["plan_data"][plan_key]["exercises"][edit_index]
        
        exercise = create_exercise(
            self.exercise_name.value,
            self.sets_count.value,
            self.reps_count.value,
            self.weight_count.value,
            self.rpe_count.value
        )
        
        self.data['plan_data'][plan_key]['exercises'].append(exercise)
        self.data['index_selected_value'] = 0
        
        await render(interaction, "edit_new_plan", self.data)