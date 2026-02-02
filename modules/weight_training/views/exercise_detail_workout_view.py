from controllers.user_controller import get_mock_client_plan_data
from modals.interaction_menu import ExerciseEdit
import discord

# ---------- NEW PLAN ----------
class NewPlanView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        # This is storing the data in a object state or instance
        self.data = data

        # Disable edit button until there is data to edit.
        # This needs to contain the new data structure
        self.edit_button.disabled = not bool(self.data["data"])

    # This button should change once it's completed
    @discord.ui.button(label="Add Exercise", style=discord.ButtonStyle.blurple, emoji="💪")
    async def new_exercise_button(self, interaction, button):
        from modals.name_modal import PlanDetails
        await interaction.response.send_modal(PlanDetails(self.data))
    
    # Disable this button if self.data['data'] contains zero data.
    @discord.ui.button(label="Edit", style=discord.ButtonStyle.success, emoji="📝")
    async def edit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from ui.render import render  # ✅ local import
        # Now whe this button is clicked refresh but with 
        await render(interaction, "edit_new_plan", self.data)

    @discord.ui.button(label="Exit", style=discord.ButtonStyle.danger, emoji="⛔")
    async def cancel_button(self, interaction, button):
        from ui.render import render
        await render(interaction, "exit_plan", self.data)

# ---------- EDIT EXERCISE ----------
class EditExerciseView(discord.ui.View):
    # Todo: Drop down menu is not showing
    # Drop down menu is now showing here
    def __init__(self, data):
        super().__init__(timeout=None)
        self.data = data
    
        # Menu select to make changes
        self.add_item(ExerciseEdit(self.data, row=0))

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.blurple, emoji="📝", row=1)
    async def edit_exercise(self, interaction, button):
        from modals.name_modal import EditExerciseDetails
        await interaction.response.send_modal(EditExerciseDetails(self.data))
    
    @discord.ui.button(label="Del", style=discord.ButtonStyle.blurple, emoji="📝", row=1)
    async def del_exercise(self, interaction, button):
        from modals.name_modal import EditExerciseDetails
        print('Deletin the following value')
    
    @discord.ui.button(label="Return", style=discord.ButtonStyle.blurple, emoji="📝", row=1)
    async def return_home(self, interaction, button):
        from modals.name_modal import EditExerciseDetails
        await interaction.response.send_modal(EditExerciseDetails(self.data))

# ---------- EXIT PLAN VIEW ----------
class ExitPlanView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        self.data = data
    # Add modal to select specific exercise to delete or keep.
    @discord.ui.button(label="Save", style=discord.ButtonStyle.success, emoji="💾", row=1)
    async def save_plan(self, interaction: discord.Interaction, button: discord.ui.Button):
        from ui.render import render
        print('Todo: Save the data to the back-end and return home')
        await render(interaction, "home", self.data)

    @discord.ui.button(label="Discard", style=discord.ButtonStyle.danger, emoji="🗑️", row=1)
    async def discard_changes(self, interaction: discord.Interaction, button: discord.ui.Button):
        from ui.render import render
        self.data = None
        await render(interaction, "home", self.data)