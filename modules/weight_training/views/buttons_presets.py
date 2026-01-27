# views/workout_view.py
import discord
from modals.interaction_menu import ExerciseSelect
from modals.interaction_menu import WorkOutPlan
from controllers.user_controller import get_mock_client_plan_pages
from controllers.user_controller import get_mock_workout_plan

# ---------- HOME ----------
class HomeView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        self.data = data
        self.client_plan_collection: dict | None = None
    
    @discord.ui.button(label="🏋️ Start Plan", style=discord.ButtonStyle.green)
    async def start(self, interaction, button):
        from ui.render import render  # local import
        
        self.client_plan_collection = await get_mock_client_plan_pages()

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

# ---------- View the user's workout list ----------
class StartWorkOutView(discord.ui.View):
    def __init__(self, client_plan_collection):
        super().__init__(timeout=None)
        self.client_plan_collection = client_plan_collection
        # Selector input box
        self.add_item(WorkOutPlan(self.client_plan_collection))

        self.button_click_count = 0

        # Disable at zero
        if self.client_plan_collection["button_click_count"] == 0:
            self.prev.disabled = True
    
        if self.client_plan_collection["button_click_count"] == len(self.client_plan_collection["plans"]) - 1:
             self.next.disabled = True
        

    # Use fake data here for now.
    @discord.ui.button(label="Start", style=discord.ButtonStyle.green, emoji="🏋️", row=1)
    async def start_workout(self, interaction, button):
        from ui.render import render

        data = await get_mock_workout_plan()
        
        # await render(interaction, "start_workout", self.client_plan_collection)
        await render(interaction, "start_workout", data)
    
    #  TRACK THE BUTTON CLICK AND STATUS
    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple, emoji="▶", row=1)
    async def next(self, interaction, button):
        from ui.render import render  # ✅ local import

        total_workout_plans = len(self.client_plan_collection["plans"])

        self.button_click_count = min(total_workout_plans, self.button_click_count + 1)

        self.client_plan_collection["button_click_count"] = self.button_click_count

        await render(interaction, "start", self.client_plan_collection)

    @discord.ui.button(label="Prev", style=discord.ButtonStyle.blurple, emoji="◀", row=1)
    async def prev(self, interaction, button):
        from ui.render import render  # ✅ local import
        
        self.button_click_count = max(0, self.button_click_count - 1)
        
        self.client_plan_collection["button_click_count"] = self.button_click_count
       
        await render(interaction, "start", self.client_plan_collection)

    @discord.ui.button(label="Home", style=discord.ButtonStyle.red, emoji="🔃", row=1)
    async def back(self, interaction, button):
        from ui.render import render  # ✅ local import
        await render(interaction, "home", self.client_plan_collection)

# ---------- Current workout in session view----------
class WorkoutSessionView(discord.ui.View):
    def __init__(self, client_plan_collection):
        super().__init__(timeout=None)
        
        self.data = client_plan_collection
        
        self.client_plan_collection = client_plan_collection
        
        self.completed_sets = set()

        # Disabling button logic
        self.previous_set.disabled = self.data["current_set"] == 1
        
        total_sets = len(self.data["sets"])
        
        self.next_set.disabled = self.data["current_set"] == total_sets

    # ----------------- BUTTONS -----------------
    @discord.ui.button(label="Prev", style=discord.ButtonStyle.success, emoji="⬅️")
    async def previous_set(self, interaction: discord.Interaction, button: discord.ui.Button):
        from ui.render import render

        # Prevent from it making it into a zero all together...
        self.data["current_set"] = max(0, self.data["current_set"] - 1)
    
        await render(interaction, "start_workout", self.data)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.success, emoji="➡️")
    # Pop up modal with each next button click?
    async def next_set(self, interaction: discord.Interaction, button: discord.ui.Button):
        from ui.render import render
        
        display_sets = len(self.data["sets"]) + 1
        
        # Increment but clamp at display_sets count
        self.data["current_set"] = min(self.data["current_set"] + 1, display_sets)

        # Always edit the message once
        await render(interaction, "start_workout", self.data)
    
    @discord.ui.button(label="Return", style=discord.ButtonStyle.primary, emoji="🔄")
    async def return_workout_view(self, interaction: discord.Interaction, button: discord.ui.Button):
        from ui.render import render
        
        data = await fetch_client_data_plans()
        
        await render(interaction, "start", data)

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
