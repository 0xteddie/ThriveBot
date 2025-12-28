# ui/render.py
async def render(interaction, state: str, data=None):
    data = data or {}

    from ui.embed_presets import EMBEDS, VIEWS  # safe now

    embed = EMBEDS[state](data)
    view = VIEWS[state](data)

    await interaction.response.edit_message(embed=embed, view=view)
