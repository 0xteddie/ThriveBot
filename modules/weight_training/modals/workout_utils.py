from collections import Counter

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
    
    # Convert to proper types
    sets_count = int(sets_count)
    reps_count = int(reps_count)
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

def get_max_weight(sets: list):    
    weight_list = []
    
    for weight in range(len(sets)):
        weight_list.append(sets[weight]['weight'])
    
    max_weight = max(weight_list)
        
    return max_weight

def delete_exercise_item(exercise: list, index_selected_value: int):
    del exercise[index_selected_value]