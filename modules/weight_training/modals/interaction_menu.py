import discord

class ExerciseSelect(discord.ui.Select):
    # Eneumerate over the data here.
    def __init__(self, data, row=0):
        self.data = data

        options = [
            discord.SelectOption(
                label=exercise["exercise_name"],
                value=str(index)
            )
            for index, exercise in enumerate(data["data"])
        ]

        super().__init__(
            placeholder="Choose…",
            options=options,
            min_values=1,
            max_values=1,
            row=row
        )