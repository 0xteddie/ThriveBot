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
    def __init__(self, row=1):
        options = [
            discord.SelectOption(
                label="Select 1",
                value="select_1"
            ),
            discord.SelectOption(
                label="Select 2",
                value="select_2"
            )
        ]

        super().__init__(
            placeholder="Choose…",
            options=options,
            min_values=1,
            max_values=1,
            row=row
        )
