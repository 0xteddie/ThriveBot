import discord, datetime
from controllers.user_controller import get_workout_list
from controllers.user_controller import get_mock_client_plan_data

class HomeView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)
        self.data = data
        self.client_plan_collection: dict | None = None
    
    # Refractor complete: ✅ 
    @discord.ui.button(label="🏋️ Start Plan", style=discord.ButtonStyle.green)
    async def start(self, interaction, button):
        from ui.render import render  # local import
        
        # Fetching data
        local_data = await get_mock_client_plan_data()
        
        self.client_plan_collection = get_workout_list(local_data)
       
        if not self.client_plan_collection or not self.client_plan_collection.get("plans"):
            button.disabled = True
            await interaction.response.edit_message(view=self)
            return
        
        await render(interaction, "start", self.client_plan_collection)

    @discord.ui.button(label="➕ New Plan", style=discord.ButtonStyle.blurple)
    async def new_plan(self, interaction, button):
        from modals.name_modal import NamePlanModal
        await interaction.response.send_modal(NamePlanModal(self.data))

    # Refractor complete: ✅ 
    @discord.ui.button(label="✏️ Adjust", style=discord.ButtonStyle.red)
    async def adjust(self, interaction, button):
        from ui.render import render  # ✅ local import

        local_data = await get_mock_client_plan_data()
        
        self.data = get_workout_list(local_data)
        
        await render(interaction, "adjust", self.data)