# ui/render.py
async def render(interaction, state: str, data=None):
    data = data or {}

    from ui.new_presets import EMBEDS, BUTTONS  # safe now

    embed = EMBEDS[state](data)
    view = BUTTONS[state](data)

    await interaction.response.edit_message(embed=embed, view=view)
