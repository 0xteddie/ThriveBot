from controllers.user_controller import get_workout_exercises_data
from controllers.user_controller import get_mock_client_plan_data
from modals.interaction_menu import WorkOutPlan
import discord

# ---------- View the user's workout list ----------
class StartWorkOutView(discord.ui.View):
    def __init__(self, client_plan_collection):
        super().__init__(timeout=None)
        self.client_plan_collection = client_plan_collection
        
        # Selector Input box (Data is being passed into the selector box)
        self.add_item(WorkOutPlan(self.client_plan_collection))
 
        self.button_click_count = 0

        # [Disable buttons] - Disable button at zero
        if self.client_plan_collection["button_click_count"] == 0:
            self.prev.disabled = True
    
        if self.client_plan_collection["button_click_count"] == len(self.client_plan_collection["plans"]) - 1:
             self.next.disabled = True
        
    @discord.ui.button(label="Start", style=discord.ButtonStyle.green, emoji="🏋️", row=1)
    async def start_workout(self, interaction, button):
        from ui.render import render

        # Show push day here from the selector box
        local_data = await get_mock_client_plan_data()
        
        workout_name = self.client_plan_collection['picked_option']
        
        data = get_workout_exercises_data(local_data, workout_name)
        
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