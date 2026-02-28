from collections import Counter
import asyncio

def create_plan(plan_name, split, focus):
    """Initialize a new workout plan structure"""
    return {
        plan_name: {
            "split": split,
            "focus": focus,
            "exercises": []
        }
    }
    
def create_exercise(exercise_name, sets_count, reps_count, weight, rpe=7):
    """Create and validate an exercise with all its sets"""
    
    sets_count = int(sets_count)
    reps_count = str(reps_count)
    weight = int(weight)
    rpe = int(rpe) if rpe else 7
    
    exercise = {
        "exercise_name": exercise_name,
        "sets_count": sets_count,
        "reps_count": reps_count,
        "rpe": rpe,
        "sets": [], 
        "current_set": 0  
    }
    
    # Create individual sets
    for _ in range(sets_count):
        exercise['sets'].append({
            'weight': weight,
            'reps': reps_count,
            'rpe': rpe
        })
    
    return exercise

def format_plan_for_edit(plan_name, data):
    return {
        "plan_data": {
            plan_name: {
                "split": data["split"],
                "focus": data["focus"],
                "exercises": data["exercises"]
            }
        },
        "index_selected_value": 0
    }


def is_valid_reps(reps: str) -> bool:
    if '-' in reps:
        parts = reps.split('-')
        return len(parts) == 2 and all(p.isdigit() for p in parts)
    return reps.isdigit()


def validate_exercise_inputs(sets, reps, weight) -> str | None:
    """Returns an error message if invalid, None if valid."""

    fields = [
        (sets.isdigit(),                        "Sets must be a number."),
        (is_valid_reps(reps),                   "Reps must be a number or range (e.g. 10-12)."),
        (weight.replace('.', '', 1).isdigit(),  "Weight must be a number."),
    ]

    for is_valid, error_message in fields:
        if not is_valid:
            return error_message

    return None


def get_max_weight(sets: list):    
    weight_list = []
    
    for weight in range(len(sets)):
        weight_list.append(sets[weight]['weight'])
    
    max_weight = max(weight_list)
        
    return max_weight

def delete_exercise_item(exercise: list, index_selected_value: int):
    del exercise[index_selected_value]

def parse_highest_number(value):
    numbers = [int(n) for n in str(value).split("–") if n.strip().isdigit()]
    return max(numbers) if numbers else int(value)

def delete_workout_plan(workout_plan: list, index_selected_value: int):
    # 1. Grab workout name ✅
    # 2. Delete from database - In progress
    del workout_plan[index_selected_value]
    