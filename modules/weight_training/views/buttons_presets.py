# views/workout_view.py
import discord
from modals.interaction_menu import ExerciseSelect

# ---------- HOME ----------
class HomeView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        self.data = data

    @discord.ui.button(label="🏋️ Start Plan", style=discord.ButtonStyle.green)
    async def start(self, interaction, button):
        from ui.render import render  # ✅ local import
        await render(interaction, "start", self.data)

    @discord.ui.button(label="➕ New Plan", style=discord.ButtonStyle.blurple)
    async def new_plan(self, interaction, button):
        # This needs to be changed with NameplanModal instead of what it is right now 
        from modals.name_modal import NamePlanModal
        await interaction.response.send_modal(NamePlanModal(self.data))

    @discord.ui.button(label="✏️ Adjust", style=discord.ButtonStyle.red)
    async def adjust(self, interaction, button):
        from ui.render import render  # ✅ local import
        await render(interaction, "adjust", self.data)


# ---------- START ----------
class StartView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        self.data = data
    
    @discord.ui.button(label="Back", style=discord.ButtonStyle.secondary)
    async def back(self, interaction, button):
        from ui.render import render  # ✅ local import
        await render(interaction, "home", self.data)

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

    # This button should change once it's completed
    @discord.ui.button(label="Add Exercise", style=discord.ButtonStyle.blurple, emoji="💪")
    async def new_plan(self, interaction, button):
        from modals.name_modal import PlanDetails
        await interaction.response.send_modal(PlanDetails(self.data))
    
    @discord.ui.button(label="Edit", style=discord.ButtonStyle.success, emoji="📝")
    async def save_plan(self, interaction: discord.Interaction, button: discord.ui.Button):
        from ui.render import render  # ✅ local import
        # (swap this to a save action)
        await render(interaction, "edit_plan", self.data)

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger, emoji="⛔")
    async def back(self, interaction, button):
        from ui.render import render  # ✅ local import
        await render(interaction, "home", self.data)

# Edit plan
class EditExerciseView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        self.data = data

        # Show drop down menu (Return data)
        self.add_item(ExerciseSelect(self.data, row=0))

    @discord.ui.button(label="Edit exercise", style=discord.ButtonStyle.blurple, emoji="📝", row=1)
    async def edit_exercise(self, interaction, button):
        from ui.render import render
        await render(interaction, "edit_plan", self.data)

    # Delete exercise from self.data list
    @discord.ui.button(label="Delete exercise", style=discord.ButtonStyle.danger, emoji="🗑️", row=1)
    async def delete_exercise(self, interaction, button):
        from ui.render import render
        await render(interaction, "edit_plan", self.data)

    # Return to NewPlanView and show updated list.
    @discord.ui.button(label="Save", style=discord.ButtonStyle.success, emoji="💾", row=1)
    async def back(self, interaction, button):
        from ui.render import render
        await render(interaction, "edit_plan", self.data)