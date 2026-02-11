import discord

class ExerciseEdit(discord.ui.Select):
    def __init__(self, data):
        self.data = data
        
        plan_name = list(data['plan_data'])[0]
        exercises = data["plan_data"][plan_name]["exercises"]
        
        # Build options from exercise names
        options = []
        for index, exercise in enumerate(exercises):
            options.append(
                discord.SelectOption(
                    label=exercise["exercise_name"],
                    value=str(index),  # Use index as the value to identify which exercise was selected
                    description=f"{exercise['sets_count']} sets × {exercise['reps_count']} reps"
                )
            )
        
        # If no exercises, add a placeholder
        if not options:
            options.append(
                discord.SelectOption(
                    label="No exercises yet",
                    value="none",
                    description="Add an exercise first"
                )
            )
        
        super().__init__(
            placeholder="Select an exercise to edit",
            options=options,
            min_values=1,
            max_values=1
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        selected_index = int(self.values[0])
        
        self.data['selected_index'] = selected_index


class ExerciseSelect(discord.ui.Select):
    def __init__(self, data, row=0):
        self.data = data

        options = []
        
        for index, exercise in enumerate(data["data"]):
            option = discord.SelectOption(
                label=exercise["exercise_name"],
                value=str(index)
            )
            options.append(option)

        super().__init__(
            placeholder="Choose…",
            options=options,
            min_values=1,
            max_values=1,
            row=row
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        # Parsing the interaction payload - sent by discord.
        selected_index = int(self.values[0])
        chosen = self.data["data"][selected_index]

class WorkOutPlan(discord.ui.Select):
    def __init__(self, client_plan_collection):
        self.client_plan_collection = client_plan_collection
    
        options = []
        # Maximize at 5 total rows
        
        current_plan_view = client_plan_collection["button_click_count"]
        for index, workout_plan_name in enumerate(client_plan_collection["plans"][current_plan_view]):
            option = discord.SelectOption(
                label=workout_plan_name["name"],
                value=str(index)
            )
            
            options.append(option)
        
        super().__init__(
            placeholder="Choose…",
            options=options,
            min_values=1,
            max_values=1,
            row=0
        )
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        selected_index = int(self.values[0])
        
        current_plan_view = self.client_plan_collection["button_click_count"]
        
        # This will update the data to contain the new value
        chosen = self.client_plan_collection["plans"][current_plan_view][selected_index]
            
        self.client_plan_collection['picked_option'] = chosen['name']
        

