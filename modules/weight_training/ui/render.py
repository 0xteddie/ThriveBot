# ui/render.py
import asyncio

async def render(interaction, state: str, data=None):
    from ui.new_presets import EMBEDS, BUTTONS

    data = data or {}
    
    embed = EMBEDS[state](data)
    view = BUTTONS[state](data)

    message = data.get("message_return")

    await interaction.response.edit_message(embed=embed, view=view)

    if message:
        msg = await interaction.followup.send(str(message), ephemeral=True)
        await asyncio.sleep(4)
        await msg.delete()