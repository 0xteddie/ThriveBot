async def get_mock_client_plan_data():
    """Single source of truth for all client plan data"""
    
    plan_data = {
        "Push Day": {
            "split": "Push",
            "focus": "Hypertrophy",
            "exercises": [
                {
                    "exercise_name": "Bench Press",
                    "sets_count": 4,
                    "reps_count": "6–8",
                    "rpe": 8,
                    "sets": [
                        {"weight": 185, "reps": 8, "rpe": 7},
                        {"weight": 205, "reps": 6, "rpe": 8},
                        {"weight": 205, "reps": 6, "rpe": 8},
                        {"weight": 185, "reps": 8, "rpe": 8},
                    ],
                    "current_set": 0
                },
                {
                    "exercise_name": "Overhead Press",
                    "sets_count": 3,
                    "reps_count": "8–10",
                    "rpe": 7,
                    "sets": [
                        {"weight": 95, "reps": 10, "rpe": 7},
                        {"weight": 95, "reps": 9, "rpe": 7},
                        {"weight": 95, "reps": 8, "rpe": 7},
                    ],
                    "current_set": 0
                },
                {
                    "exercise_name": "Incline Dumbbell Press",
                    "sets_count": 3,
                    "reps_count": "10–12",
                    "rpe": 7,
                    "sets": [
                        {"weight": 60, "reps": 12, "rpe": 6},
                        {"weight": 65, "reps": 11, "rpe": 7},
                        {"weight": 65, "reps": 10, "rpe": 7},
                    ],
                    "current_set": 0
                },
                {
                    "exercise_name": "Tricep Pushdowns",
                    "sets_count": 5,
                    "reps_count": "12–15",
                    "rpe": 7,
                    "sets": [
                        {"weight": 70, "reps": 12, "rpe": 6},
                        {"weight": 100, "reps": 8, "rpe": 7},
                        {"weight": 60, "reps": 14, "rpe": 8},
                        {"weight": 60, "reps": 14, "rpe": 8},
                        {"weight": 60, "reps": 14, "rpe": 8}
                    ],
                    "current_set": 0
                },
                {
                    "exercise_name": "Lateral Raises",
                    "sets_count": 3,
                    "reps_count": "12–15",
                    "rpe": 6,
                    "sets": [
                        {"weight": 20, "reps": 15, "rpe": 6},
                        {"weight": 20, "reps": 14, "rpe": 6},
                        {"weight": 20, "reps": 13, "rpe": 6},
                    ],
                    "current_set": 0
                },
                {
                    "exercise_name": "Chest Flyes",
                    "sets_count": 3,
                    "reps_count": "12–15",
                    "rpe": 6,
                    "sets": [
                        {"weight": 30, "reps": 15, "rpe": 6},
                        {"weight": 30, "reps": 14, "rpe": 6},
                        {"weight": 30, "reps": 12, "rpe": 6},
                    ],
                    "current_set": 0
                },
            ],
        },
        "Pull Day": {
            "split": "Pull",
            "focus": "Hypertrophy",
            "exercises": [
                {
                    "exercise_name": "Pull-Ups",
                    "sets_count": 4,
                    "reps_count": "AMRAP",
                    "rpe": 8,
                    "sets": [
                        {"weight": 0, "reps": 12, "rpe": 7},
                        {"weight": 0, "reps": 10, "rpe": 8},
                        {"weight": 0, "reps": 8, "rpe": 8},
                        {"weight": 0, "reps": 7, "rpe": 8},
                    ],
                    "current_set": 0
                },
                {
                    "exercise_name": "Barbell Row",
                    "sets_count": 4,
                    "reps_count": "6–8",
                    "rpe": 8,
                    "sets": [
                        {"weight": 135, "reps": 8, "rpe": 7},
                        {"weight": 155, "reps": 7, "rpe": 8},
                        {"weight": 155, "reps": 6, "rpe": 8},
                        {"weight": 135, "reps": 8, "rpe": 8},
                    ],
                    "current_set": 0
                },
                {
                    "exercise_name": "Lat Pulldown",
                    "sets_count": 3,
                    "reps_count": "10–12",
                    "rpe": 7,
                    "sets": [
                        {"weight": 120, "reps": 12, "rpe": 6},
                        {"weight": 130, "reps": 11, "rpe": 7},
                        {"weight": 130, "reps": 10, "rpe": 7},
                    ],
                    "current_set": 0
                },
                {
                    "exercise_name": "Face Pulls",
                    "sets_count": 3,
                    "reps_count": "12–15",
                    "rpe": 6,
                    "sets": [
                        {"weight": 50, "reps": 15, "rpe": 6},
                        {"weight": 50, "reps": 14, "rpe": 6},
                        {"weight": 50, "reps": 13, "rpe": 6},
                    ],
                    "current_set": 0
                },
                {
                    "exercise_name": "Bicep Curls",
                    "sets_count": 3,
                    "reps_count": "10–12",
                    "rpe": 7,
                    "sets": [
                        {"weight": 30, "reps": 12, "rpe": 6},
                        {"weight": 35, "reps": 11, "rpe": 7},
                        {"weight": 35, "reps": 10, "rpe": 7},
                    ],
                    "current_set": 0
                },
                {
                    "exercise_name": "Hammer Curls",
                    "sets_count": 3,
                    "reps_count": "10–12",
                    "rpe": 7,
                    "sets": [
                        {"weight": 30, "reps": 12, "rpe": 7},
                        {"weight": 30, "reps": 11, "rpe": 7},
                        {"weight": 30, "reps": 10, "rpe": 7},
                    ],
                    "current_set": 0
                },
            ],
        },
    }
    
    return plan_data


# Helper functions for parsing the data
def get_workout_list(plan_data: dict, chunk_size: int = 5) -> dict:
    """Get paginated workout list with metadata"""
    user_plan_list = [
        {
            "name": name,
            "split": data["split"],
            "ex": len(data["exercises"]),
            "focus": data["focus"]
        }
        for name, data in plan_data.items()
    ]
    
    return {
        "plans": [
            user_plan_list[index:index + chunk_size]
            for index in range(0, len(user_plan_list), chunk_size)
        ],
        "button_click_count": 0
    }


def get_workout_exercises(plan_data: dict, workout_name: str) -> list:
    """Get exercises for a specific workout"""
    return plan_data[workout_name]["exercises"]


def get_exercises_as_dict(plan_data: dict, workout_name: str) -> dict:
    """Get exercises as dict with exercise_name as key"""
    exercises = plan_data[workout_name]["exercises"]
    return {ex["exercise_name"]: ex for ex in exercises}

def get_workout_exercises_data(plan_data: dict, workout_name: str) -> list[dict]:
    """Get all exercises data for a workout formatted for embed"""
    workout = plan_data[workout_name]
    
    return {
        "exercises": [
            {
                "exercise_name": exercise["exercise_name"],
                "sets": exercise["sets"],
                "sets_count": exercise["sets_count"],
                "current_set": exercise["current_set"]
            }
            for exercise in workout["exercises"]
        ],
        "current_exercise_index": 0,  # Start at first exercise
        "workout_name": workout_name
    }
