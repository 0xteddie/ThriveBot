

# Check to see if the user has any existing plans
async def fetch_client_data_plans():
    user_plan_data = [
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
    },
    {
        "name": "Split back",
        "split": "Upper",
        "ex": 7,
        "focus": "Volume"
    },
    {
        "name": "Upper Torso",
        "split": "Upper",
        "ex": 7,
        "focus": "Volume"
    },
    {
        "name": "Upper Back",
        "split": "Upper",
        "ex": 7,
        "focus": "Volume"
    },
    {
        "name": "Lower back",
        "split": "Upper",
        "ex": 7,
        "focus": "Volume"
    },
    {
        "name": "Shoulders",
        "split": "Upper",
        "ex": 7,
        "focus": "Volume"
    },
    {
        "name": "Forearms",
        "split": "Upper",
        "ex": 7,
        "focus": "Volume"
    }
    ]

    chunked_plans = [] 
    chunk_size = 5

    result = {
        "plans": [
            user_plan_data[index:index + chunk_size]
            for index in range(0, len(user_plan_data), chunk_size)
        ]
    }
    result["button_click_count"] = 0
    #print(result["plans"])
    
    return result
