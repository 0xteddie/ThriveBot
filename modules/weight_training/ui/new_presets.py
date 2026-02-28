import discord
import datetime

# Buttons
from views.home_workout_view import HomeView
from views.start_workout_view import StartWorkOutView
from views.active_session_workout_view import WorkoutSessionView
from views.exercise_detail_workout_view import NewPlanView, EditExerciseView, ExitPlanView
from views.adjust_workout_view import StartAdjustView, AdjustView 

# Emebeds
from ui.active_embed import start_workout_session
from ui.home_workout_embed import home_embed, workout_plans_list_embed
from ui.exercise_detail_embed import create_plan_embed

# EMBEDS
EMBEDS = {
    "home": home_embed,
    "start": workout_plans_list_embed,
    "start_workout": start_workout_session,
    

    ################# EDITING SECTION ONLY
    "new_plan": create_plan_embed,
    "edit_new_plan": create_plan_embed, 
    "exit_plan": create_plan_embed,

    "adjust": workout_plans_list_embed,
    "AdjustView": create_plan_embed,
}

# BUTTONS.
BUTTONS = {
    "home": HomeView,
    "start": StartWorkOutView,
    "start_workout": WorkoutSessionView,
    
    ################# Editing only
    "new_plan": NewPlanView,
    "edit_new_plan": EditExerciseView,
    "exit_plan": ExitPlanView,

    "adjust": StartAdjustView,
    "AdjustView": AdjustView
}
