# modals/name_modal.py
import discord

class NamePlanModal(discord.ui.Modal, title="Name Your Workout Plan"):
    plan_name = discord.ui.TextInput(
        label="Workout name",
        placeholder="e.g. Push Day",
        max_length=25
    )

    def __init__(self, data):
        super().__init__()
        self.data = data

    async def on_submit(self, interaction: discord.Interaction):
        plan_name = self.plan_name.value
        
        self.data["plan_name"] = plan_name
        self.data["data"] = {
            plan_name: {
                "split": "",
                "focus": "",
                "exercises": []
            }
        }

        # Transition state
        from ui.render import render
        await render(interaction, "new_plan", self.data)


class PlanDetails(discord.ui.Modal, title="Exercise details"):
    """
    Handles exercise detail submission.

    Collects user-entered exercise data (name, sets, reps, RPE), appends it to the
    existing plan data structure, and triggers a UI re-render to display the
    updated plan.
    
    """

    exercise_name = discord.ui.TextInput(
        label="Exercise Name: ",
        placeholder="e.g. Pull up, Push ups",
        max_length=25
    )
    sets_count = discord.ui.TextInput(
        label="Total Sets: ",
        placeholder="e.g. 4",
        max_length=3
    )
    reps_count = discord.ui.TextInput(
        label="Total Reps: ",
        placeholder="e.g. 6-8 or AMRAP",
        max_length=10
    )
    rpe = discord.ui.TextInput(
        label="Target RPE (Rate of Perceived Exertion): ",
        placeholder="e.g. 7 or 8",
        max_length=2,
        required=False
    )

    def __init__(self, data):
        super().__init__()
        self.data = data

    async def on_submit(self, interaction: discord.Interaction):
        # Changed the structure into a dict instead of a list.
        plan_name = self.data["plan_name"]
        
        # Create exercise object matching your data structure
        exercise = {
            "exercise_name": self.exercise_name.value,
            "sets_count": int(self.sets_count.value),
            "reps_count": self.reps_count.value,
            "rpe": int(self.rpe.value) if self.rpe.value else 7,  # Default to 7 if not provided
            "sets": [], 
            "current_set": 0  
        }
        
        self.data['data'][plan_name]['exercises'].append(exercise)
        self.data['index_selected_value'] = 0
        
        # Send the info back to the embed with the new data
        from ui.render import render
        await render(interaction, "new_plan", self.data)

class EditExerciseDetails(discord.ui.Modal, title="Edit Exercise details"):
    """
    Handles exercise edit submission.

    Updates the selected exercise entry in the existing plan data structure
    and re-renders the plan view with the modified values.
    
    """

    exercise_name = discord.ui.TextInput(
        label="Exercise Name: ",
        placeholder="e.g. Pull up, Push ups",
        max_length=25
    )
    sets_count = discord.ui.TextInput(
        label="Total Sets: ",
        max_length=3
    )
    reps_count = discord.ui.TextInput(
        label="Total Reps: ",
        max_length=3
    )

    def __init__(self, data: dict):
        super().__init__()
        self.data = data
        
        edit_index = data["index_selected_value"]
        
        exercise = data["data"][edit_index]
    
        # Pre-fill inputs with selector value
        self.exercise_name.default = str(exercise.get("exercise_name", ""))
        self.sets_count.default = str(exercise.get("sets_count", ""))
        self.reps_count.default = str(exercise.get("reps_count", ""))

    async def on_submit(self, interaction: discord.Interaction):
        edit_index = self.data["index_selected_value"]
        exercise = self.data["data"][edit_index]

        exercise["exercise_name"] = self.exercise_name.value
        exercise["sets_count"] = self.sets_count.value
        exercise["reps_count"] = self.reps_count.value
        
        from ui.render import render
        await render(interaction, "edit_plan", self.data)