from pathlib import Path
from dotenv import load_dotenv
import aiosqlite
import os

load_dotenv()

# Always resolves to controllers/workout.sqlite no matter where bot.py runs from
BASE_DIR = Path(__file__).resolve().parent
db_path = BASE_DIR / os.getenv("DATABASE_URL")

async def insert_plan(cursor, user_id: int, plan_name: str, split: str, focus: str) -> int:
    """Insert a workout plan and return the plan id"""
    await cursor.execute("""
        INSERT INTO workout_plans (user_id, name, split, focus)
        VALUES (?, ?, ?, ?)
    """, (user_id, plan_name, split, focus))
    return cursor.lastrowid


async def insert_exercise(cursor, plan_id: int, exercise: dict) -> int:
    """Insert an exercise and return the exercise id"""
    await cursor.execute("""
        INSERT INTO exercises (plan_id, exercise_name, sets_count, reps_count, rpe)
        VALUES (?, ?, ?, ?, ?)
    """, (plan_id, exercise["exercise_name"], exercise["sets_count"], exercise["reps_count"], exercise["rpe"]))
    return cursor.lastrowid


async def insert_sets(cursor, exercise_id: int, sets: list) -> None:
    """Insert all sets for an exercise"""
    for index, s in enumerate(sets):
        await cursor.execute("""
            INSERT INTO sets (exercise_id, set_number, weight, reps, rpe)
            VALUES (?, ?, ?, ?, ?)
        """, (exercise_id, index + 1, s["weight"], int(s["reps"]), s["rpe"]))


async def insert_full_workout_plan(user_id: int, data: dict) -> None:
    """
    Insert a full workout plan with exercises and sets.
    Accepts the raw data structure from the bot.
    """
    plan_data = data["plan_data"]

    async with aiosqlite.connect(db_path) as conn:
        cursor = await conn.cursor()

        for plan_name, plan_details in plan_data.items():
            # Insert the plan
            plan_id = await insert_plan(
                cursor,
                user_id,
                plan_name,
                plan_details["split"],
                plan_details["focus"]
            )

            # Insert each exercise and its sets
            for exercise in plan_details["exercises"]:
                exercise_id = await insert_exercise(cursor, plan_id, exercise)
                await insert_sets(cursor, exercise_id, exercise["sets"])

        await conn.commit()

    print(f"Workout plan inserted successfully for user {user_id}!")