from controllers.user_controller import get_mock_client_plan_data
from modals.interaction_menu import WorkOutPlan
from modals.workout_utils import delete_workout_plan, format_plan_for_edit
from modals.interaction_menu import ExerciseEdit
from modals.name_modal import NamePlanModal
from ui.render import render
import discord

class StartAdjustView(discord.ui.View):
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
        
    @discord.ui.button(label="Edit", style=discord.ButtonStyle.green, emoji="🏋️", row=1)
    async def edit_workout(self, interaction, button):
        # Push the selected data here
        plan_data = await get_mock_client_plan_data()

        plan_name = self.client_plan_collection['picked_option']
    
        workout_data = plan_data.get(str(plan_name))
        
        restructured_data = format_plan_for_edit(str(plan_name), workout_data)

        await render(interaction, "new_plan", restructured_data)

    #  TRACK THE BUTTON CLICK AND STATUS
    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple, emoji="▶", row=1)
    async def next(self, interaction, button):
        total_workout_plans = len(self.client_plan_collection["plans"])

        self.button_click_count = min(total_workout_plans, self.button_click_count + 1)

        self.client_plan_collection["button_click_count"] = self.button_click_count

        await render(interaction, "start", self.client_plan_collection)

    @discord.ui.button(label="Prev", style=discord.ButtonStyle.blurple, emoji="◀", row=1)
    async def prev(self, interaction, button):
        self.button_click_count = max(0, self.button_click_count - 1)
        
        self.client_plan_collection["button_click_count"] = self.button_click_count
       
        await render(interaction, "start", self.client_plan_collection)

    @discord.ui.button(label="Home", style=discord.ButtonStyle.red, emoji="🔃", row=1)
    async def back(self, interaction, button):
        data = None
        await render(interaction, "home", data)


class AdjustView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        self.data: dict | data = data 
        
        self.add_item(ExerciseEdit(self.data))
        
        # If zero plans found disable buttons
        self.edit_plan.disabled = not self.data['plans'][0]
        self.delete_plan.disabled = not self.data['plans'][0]

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
    async def Exit(self, interaction, button):
        await render(interaction, "adjust", self.data)