import discord

class ExerciseSelect(discord.ui.Select):
    def __init__(self, data, row=0):
        self.data = data
        options = [
            discord.SelectOption(label="Option 1", value="1"),
            discord.SelectOption(label="Option 2", value="2"),
            discord.SelectOption(label="Option 3", value="3"),
        ]
        super().__init__(
            placeholder="Choose…",
            options=options,
            min_values=1,
            max_values=1,
            row=row
        )