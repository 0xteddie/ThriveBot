import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv("DATABASE_URL")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Workout plans table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS workout_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        split TEXT NOT NULL,
        focus TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")

# Exercises table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plan_id INTEGER NOT NULL,
        exercise_name TEXT NOT NULL,
        sets_count INTEGER NOT NULL,
        reps_count TEXT NOT NULL,
        rpe INTEGER NOT NULL,
        current_set INTEGER DEFAULT 0,
        FOREIGN KEY (plan_id) REFERENCES workout_plans(id)
    )
""")

# Sets table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise_id INTEGER NOT NULL,
        set_number INTEGER NOT NULL,
        weight REAL NOT NULL,
        reps INTEGER NOT NULL,
        rpe INTEGER NOT NULL,
        FOREIGN KEY (exercise_id) REFERENCES exercises(id)
    )
""")

conn.commit()
conn.close()

print("Database and tables created successfully!")
