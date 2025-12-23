import discord
import sqlite3
import aiosqlite

# Back-end script for when buttons are clicked.
# User.id is vital here for button clicks.
# User.id will be used for determining who clicked a button and fetching information for that specific user.

# For now we're going to write a script that will save information into a database based on button click.
async def write_workout_set(user_id: str, workout_id: int, workout_exercise_id: int, set_number: int, reps: int, weight: float, date_id: str):
    async with aiosqlite.connect("weight_training.db") as db:
        await db.execute("""
            INSERT INTO worked_sets (
                user_id, workout_id, workout_exercise_id,
                set_number, reps, weight, completed_at, date_id
            ) VALUES (?, ?, ?, ?, ?, ?, datetime('now'), ?)
        """, (user_id, workout_id, workout_exercise_id, set_number, reps, weight, date_id))
        await db.commit()
    return "Done"


# Create exercises


def add_total_reps():
    # Add the total reps entered by the user with button click.
    pass

def complete_workout():
    # Complete a specific task for the day.
    # Completes an entire workout, and save progress.
    pass

write_workout_set(
    user_id="1234567890",
    workout_id=1,
    workout_exercise_id=10,
    set_number=1,
    reps=8,
    weight=185.0,
    date_id="2025-12-22"
)