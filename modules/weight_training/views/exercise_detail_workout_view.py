import asyncio
import discord

from controllers.insert_data import insert_full_workout_plan
from modals.interaction_menu import ExerciseEdit
from modals.name_modal import EditExerciseDetails, PlanDetails
from modals.workout_utils import delete_exercise_item, validate_exercises
from ui.render import render

# ---------- NEW PLAN ----------
class NewPlanView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        self.data = data
        
        # Disable edit button
        plan_key = next(iter(self.data['plan_data']))
        self.edit_button.disabled = not self.data['plan_data'][plan_key]['exercises']

    # This button should change once it's completed
    @discord.ui.button(label="Add Exercise", style=discord.ButtonStyle.blurple, emoji="💪")
    async def new_exercise_button(self, interaction, button):
        await interaction.response.send_modal(PlanDetails(self.data))
    
    # Disable this button if it's not showing a selected value
    @discord.ui.button(label="Edit", style=discord.ButtonStyle.success, emoji="📝")
    async def edit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await render(interaction, "edit_new_plan", self.data)

    @discord.ui.button(label="Exit", style=discord.ButtonStyle.danger, emoji="⛔")
    async def cancel_button(self, interaction, button):
        await render(interaction, "exit_plan", self.data)

# ---------- EDIT EXERCISE ----------
class EditExerciseView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        self.data = data
        
        self.add_item(ExerciseEdit(self.data))

    # Edit button here
    @discord.ui.button(label="Edit", style=discord.ButtonStyle.blurple, emoji="📝", row=1)
    async def edit_exercise(self, interaction, button):
        await interaction.response.send_modal(EditExerciseDetails(self.data))
    
    @discord.ui.button(label="Del", style=discord.ButtonStyle.blurple, emoji="⛔", row=1)
    async def del_exercise(self, interaction, button):
        """Remove the currently selected exercise from the plan."""
        plan_key = next(iter(self.data['plan_data']))
        selected_index =  self.data['selected_index']
        exercise_data = self.data['plan_data'][plan_key]['exercises']
        
        exercise = delete_exercise_item(exercise_data, selected_index)

        self.data['plan_data'][plan_key]['exercise'] = exercise

        await render(interaction, "edit_new_plan", self.data)

    @discord.ui.button(label="Return", style=discord.ButtonStyle.blurple, emoji="🔄", row=1)
    async def return_home(self, interaction, button):
        await render(interaction, "new_plan", self.data)


# ---------- EXIT PLAN VIEW ----------
class ExitPlanView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        self.data = data

    @discord.ui.button(label="Save", style=discord.ButtonStyle.success, emoji="💾", row=1)
    async def save_plan(self, interaction: discord.Interaction, button: discord.ui.Button):
       
        plan_key = next(iter(self.data['plan_data']))
        exercise = self.data['plan_data'][plan_key]['exercises']

        error = validate_exercises(workout_plan_exercise=exercise)
        
        if error:
            await interaction.response.send_message(str(error), ephemeral=True)
            await asyncio.sleep(4)
            await interaction.delete_original_response()
            return
        
        self.data = dict()
        self.data['message_return'] = 'Plan saved!'
        await render(interaction, "home", self.data)

    @discord.ui.button(label="Discard", style=discord.ButtonStyle.danger, emoji="🗑️", row=1)
    async def discard_changes(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.data = None
        await render(interaction, "home", self.data)