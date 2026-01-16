

# Check to see if the user has any existing plans
async def fetch_client_data_plans():
    user_plan_data = {
        "plans": [
            {
                "name": "Push Day",
                "split": "Push",
                "ex": 6,
                "focus": "Hypertrophy"
            },
            {
                "name": "Pull Day",
                "split": "Pull",
                "ex": 6,
                "focus": "Hypertrophy"
            },
            {
                "name": "Legs Day",
                "split": "Legs",
                "ex": 5,
                "focus": "Strength"
            },
            {
                "name": "Upper A",
                "split": "Upper",
                "ex": 7,
                "focus": "Volume"
            }
        ]
    }

    return None