from controllers.user_controller import get_workout_list
from controllers.user_controller import get_mock_client_plan_data
import discord

# This is used for viewing the active workout session
class WorkoutSessionView(discord.ui.View):
    def __init__(self, client_plan_collection):
        super().__init__(timeout=None)
        
        self.client_plan_collection = client_plan_collection
        
        self.completed_sets = set()

        # Track which exercise the user is currently working on
        self.active_exercise_index = self.client_plan_collection['current_exercise_index']
    
        active_exercise = self.client_plan_collection['exercises'][self.active_exercise_index]
        max_set_index = active_exercise['sets_count'] - 1
        current_set_index = active_exercise['current_set']
        
        # Disable previous button if on first set
        self.previous_set.disabled = current_set_index == 0
        
        # Disable next button if on last set
        self.next_set.disabled = current_set_index == max_set_index

    # ----------------- BUTTONS -----------------
    @discord.ui.button(label="Prev", style=discord.ButtonStyle.success, emoji="⬅️")
    async def previous_set(self, interaction: discord.Interaction, button: discord.ui.Button):
        from ui.render import render

        active_exercise = self.client_plan_collection['exercises'][self.active_exercise_index]
        active_exercise['current_set'] = max(0, active_exercise['current_set'] - 1)
    
        await render(interaction, "start_workout", self.client_plan_collection)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.success, emoji="➡️")
    async def next_set(self, interaction: discord.Interaction, button: discord.ui.Button):
        from ui.render import render
        
        active_exercise = self.client_plan_collection['exercises'][self.active_exercise_index]
        max_set_index = active_exercise['sets_count'] - 1
        
        # Increment but clamp at max set index
        active_exercise['current_set'] = min(active_exercise['current_set'] + 1, max_set_index)

        await render(interaction, "start_workout", self.client_plan_collection)
    
    @discord.ui.button(label="Return", style=discord.ButtonStyle.primary, emoji="🔄")
    async def return_workout_view(self, interaction: discord.Interaction, button: discord.ui.Button):
        from ui.render import render
        
        local_data = await get_mock_client_plan_data()
        self.client_plan_collection = get_workout_list(local_data)
        
        await render(interaction, "start", self.client_plan_collection)