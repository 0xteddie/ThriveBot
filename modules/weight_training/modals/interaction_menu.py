import discord

class ExerciseSelect(discord.ui.Select):
    # Eneumerate over the data here.
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
    def __init__(self, client_plan_collection, row=1):
        self.client_plan_collection = client_plan_collection
    
        options = []
        # Maximize at 5 total rows
        for index, workout_plan_name in enumerate(client_plan_collection["plans"]):
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
            row=row
        )
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        # Parsing the interaction payload - sent by discord.
        selected_index = int(self.values[0])
        chosen = self.workout_plan_name["plans"][selected_index]