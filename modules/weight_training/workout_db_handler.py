import aiosqlite
import uuid
import logging

# Log basic info
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
)

async def add_workout_plan(user_id: str, name: str, exercise_ids: str):
    """
    Adds a new work out plan to the 'workout_plan' table.
    
    Args:
        user_id: The ID of the user this work out plan will belong to
        name: Name of the work out plan (e.g., "Back day")
        exercise_ids: The exercies this work out plan contains
    
    Returns:
        "Done" on success
    """
    async with aiosqlite.connect("weight_training.db") as db:
        random_workout_number = str(uuid.uuid4().int)[:4]
        await db.execute(""" INSERT INTO workout_plan (workout_plan_id, user_id, name, exercise_ids) VALUES (?, ?, ?, ?)
        """, (random_workout_number, user_id, name, exercise_ids))

        await db.commit()
    
    logging.info("Entry new work-out plan added.")

    
    return random_workout_number


async def add_exercise(exercise_id: int, workout_plan_id: int, name: str, category: str, sets: int, reps: int) -> str:
    """
    Adds a new exercise to the 'exercises' table for a given workout plan.
    
    Args:
        exercise_id: The unique ID for a specific exercise
        workout_plan_id: The ID of the workout this exercise belongs to "Back-day", "Shoulder day"
        name: Name of the exercise (e.g., "Bench Press")
        category: Optional category (e.g., "Chest", "Push", "Compound")
        sets: The number of sets
        reps: The number of reps per set.
    
    Returns:
        "Done" on success
    """

    async with aiosqlite.connect("weight_training.db") as db:
        await db.execute("""
            INSERT INTO exercises (
                exercise_id, workout_plan_id, name, category, sets, reps
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (exercise_id, workout_plan_id, name, category, sets, reps))
        
        await db.commit()
    
    logging.info("Entry new exercise added.")
    
    return "Done"


# Re-write this function.
async def write_workout_set(user_id: str, workout_plan_id: int, exercise_id: int, set_number: int, reps: int, weight: float, date_id: str):
    async with aiosqlite.connect("weight_training.db") as db:
        random_number_id = str(uuid.uuid4().int)[:6]
        await db.execute("""
            INSERT INTO worked_sets (
                worked_set_id, user_id, workout_plan_id, exercise_id,
                set_number, reps, weight, completed_at, date_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), ?)
        """, (random_number_id, user_id, workout_plan_id, exercise_id, set_number, reps, weight, date_id))
        
        await db.commit()
    return "Done"


async def add_exercise_to_plan(workout_plan_id: str, ids: list[int]):
    """
    Adds one or more exercises to a specific workout plan
    
    Args:
        workout_plan_id: The unique ID of the workout plan.
        ids: The exercise IDs to attach.
    
    Returns:
        "Done" on success
    """
    async with aiosqlite.connect("weight_training.db") as db:
        await db.execute("""
            UPDATE workout_plan
            SET exercise_ids = ?
            WHERE workout_plan_id = ?
        """, (f"{ids}", workout_plan_id))

        await db.commit()

    logging.info("Work out plan updated.")

    return "Done"

# Pull set info
async def pull_set_info():
    async with aiosqlite.connect("weight_training.db") as db:
        async with db.execute("SELECT user_id FROM worked_sets") as cursor:
            rows = await cursor.fetchall()
            print(rows)  # or return rows