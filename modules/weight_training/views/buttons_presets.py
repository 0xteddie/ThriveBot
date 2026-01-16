# views/workout_view.py
import discord
from modals.interaction_menu import ExerciseSelect
from modals.interaction_menu import WorkOutPlan
from controllers.user_controller import fetch_client_data_plans

# ---------- HOME ----------
class HomeView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        self.data = data
        self.client_plan_collection: dict | None = None
    
    @discord.ui.button(label="🏋️ Start Plan", style=discord.ButtonStyle.green)
    async def start(self, interaction, button):
        from ui.render import render  # local import
        
        self.client_plan_collection = await fetch_client_data_plans()

        # Disable button if no data is found.
        if not self.client_plan_collection or not self.client_plan_collection.get("plans"):
            button.disabled = True
            await interaction.response.edit_message(view=self)
            return
        
        await render(interaction, "start", self.client_plan_collection)

    @discord.ui.button(label="➕ New Plan", style=discord.ButtonStyle.blurple)
    async def new_plan(self, interaction, button):
        from modals.name_modal import NamePlanModal
        await interaction.response.send_modal(NamePlanModal(self.data))

    @discord.ui.button(label="✏️ Adjust", style=discord.ButtonStyle.red)
    async def adjust(self, interaction, button):
        from ui.render import render  # ✅ local import
        await render(interaction, "adjust", self.data)

class StartView(discord.ui.View):
    def __init__(self, client_plan_collection):
        super().__init__(timeout=None)
        self.client_plan_collection: dict | None = None
        self.add_item(WorkOutPlan())  # buttons can be added immediately

    @discord.ui.button(label="🏋️ Start workout", style=discord.ButtonStyle.green)
    async def start_workout(self, interaction, button):
        from ui.render import render  # local import
        await render(interaction, "start", self.client_plan_collection)
    
    @discord.ui.button(label="Back", style=discord.ButtonStyle.secondary)
    async def back(self, interaction, button):
        from ui.render import render  # ✅ local import
        await render(interaction, "home", self.client_plan_collection)

# ---------- ADJUST ----------
# Adjust a plan from the "home" screen.
class AdjustView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        self.data = data

    @discord.ui.button(label="Back", style=discord.ButtonStyle.secondary)
    async def back(self, interaction, button):
        from ui.render import render  # ✅ local import
        await render(interaction, "home", self.data)

# ---------- NEW PLAN ----------
class NewPlanView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        # This is storing the data in a object state or instance
        self.data = data

        # Disable edit button until there is data to edit.
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
        await render(interaction, "edit_plan", self.data)

    # Cancel
    @discord.ui.button(label="Exit", style=discord.ButtonStyle.danger, emoji="⛔")
    async def cancel_button(self, interaction, button):
        from ui.render import render
        await render(interaction, "exit_plan", self.data)

# ---------- EDIT EXERCISE ----------
class EditExerciseView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        self.data = data
        # Show drop down menu (Return data)
        self.add_item(ExerciseSelect(self.data, row=0))

    @discord.ui.button(label="Edit exercise", style=discord.ButtonStyle.blurple, emoji="📝", row=1)
    async def edit_exercise(self, interaction, button):
        from modals.name_modal import EditExerciseDetails
        await interaction.response.send_modal(EditExerciseDetails(self.data))

    # Delete exercise from self.data list
    @discord.ui.button(label="Delete exercise", style=discord.ButtonStyle.danger, emoji="🗑️", row=1)
    async def delete_exercise(self, interaction, button):
        from ui.render import render    
        try:
            selected_index = self.data["index_selected_value"]
            self.data["data"].pop(selected_index)
            await render(interaction, "edit_plan", self.data)
        except discord.errors.HTTPException:
            self.data["index_selected_value"] = None
            await render(interaction, "new_plan", self.data)

    # Return to NewPlanView and show updated list.
    @discord.ui.button(label="Return", style=discord.ButtonStyle.secondary, emoji="↩️", row=1)
    async def back(self, interaction, button):
        from ui.render import render
        await render(interaction, "new_plan", self.data)

# ---------- EXIT PLAN VIEW ----------
class ExitPlanView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        self.data = data

    @discord.ui.button(label="Save", style=discord.ButtonStyle.success, emoji="💾", row=1)
    async def save_plan(self, interaction: discord.Interaction, button: discord.ui.Button):
        from ui.render import render
        await render(interaction, "new_plan", self.data)

    @discord.ui.button(label="Discard", style=discord.ButtonStyle.danger, emoji="🗑️", row=1)
    async def discard_changes(self, interaction: discord.Interaction, button: discord.ui.Button):
        from ui.render import render
        await render(interaction, "new_plan", self.data)

    @discord.ui.button(label="Return", style=discord.ButtonStyle.secondary, emoji="↩️", row=1)
    async def return_back(self, interaction: discord.Interaction, button: discord.ui.Button):
        from ui.render import render
        await render(interaction, "new_plan", self.data)