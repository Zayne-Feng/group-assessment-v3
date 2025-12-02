"""
Utility module for seeding the database with initial and demo data.

This script is crucial for setting up a development or testing environment
by creating the necessary database schema and populating it with realistic
sample data. It ensures a consistent starting state for the application.
"""

import random
from datetime import date, timedelta, datetime
from app.db_connection import get_db
from werkzeug.security import generate_password_hash
import sqlite3 # Explicitly import sqlite3 for specific error handling.
from flask import current_app # Used for logging within the Flask application context.

def generate_random_datetime_in_range(start_date: date, end_date: date) -> datetime:
    """
    Generates a random datetime object within a specified date range.

    This helper function is used to create realistic timestamps for demo data,
    ensuring that generated records have varied creation times.

    Args:
        start_date (date): The beginning of the date range (inclusive).
        end_date (date): The end of the date range (inclusive).

    Returns:
        datetime: A randomly generated datetime object within the given range.
    """
    # Calculate the total time difference in seconds between the start and end dates.
    time_difference = datetime.combine(end_date, datetime.max.time()) - datetime.combine(start_date, datetime.min.time())
    # Generate a random number of seconds within this difference.
    random_seconds = random.randint(0, int(time_difference.total_seconds()))
    # Add the random seconds to the start date to get a random datetime.
    return datetime.combine(start_date, datetime.min.time()) + timedelta(seconds=random_seconds)

def seed_data():
    """
    Initializes and populates the database with schema and demo data.

    This function performs a series of critical database operations:
    1. Drops all existing tables to ensure a clean slate.
    2. Creates all necessary tables with their defined schemas.
    3. Inserts a comprehensive set of demo data for users, students, modules,
       enrolments, attendance, submissions, survey responses, grades, alerts,
       and stress events.
    4. Integrates error handling and transaction management to ensure data
       integrity and provide informative logging.

    The entire process is wrapped in a transaction; if any step fails,
    all changes are rolled back.

    Raises:
        ConnectionError: If there's a critical failure to connect to the database.
        sqlite3.Error: If any SQL execution or database operation fails.
        Exception: For any other unexpected errors during the seeding process.
    """
    db = None # Initialize db to None to safely handle rollback in case get_db() fails.
    try:
        db = get_db() # Obtain the database connection from the Flask application context.
        cursor = db.cursor() # Get a cursor object to execute SQL commands.

        current_app.logger.info("Starting database seeding process...")

        # ======================================================================
        # Phase 1: Drop existing tables to ensure a clean database state.
        # This is crucial for repeatable seeding in development/testing.
        # ======================================================================
        current_app.logger.info("Dropping existing tables...")
        drop_statements = [
            "DROP TABLE IF EXISTS stress_events;",
            "DROP TABLE IF EXISTS alerts;",
            "DROP TABLE IF EXISTS grades;",
            "DROP TABLE IF EXISTS submission_records;",
            "DROP TABLE IF EXISTS attendance_records;",
            "DROP TABLE IF EXISTS survey_responses;",
            "DROP TABLE IF EXISTS enrolments;",
            "DROP TABLE IF EXISTS modules;",
            "DROP TABLE IF EXISTS users;",
            "DROP TABLE IF EXISTS students;",
        ]
        for stmt in drop_statements:
            cursor.execute(stmt)
        db.commit() # Commit changes after dropping tables.
        current_app.logger.info("Existing tables dropped successfully.")

        # ======================================================================
        # Phase 2: Create all necessary tables with their defined schemas.
        # This establishes the database structure for the application.
        # ======================================================================
        current_app.logger.info("Creating tables...")
        cursor.execute("""
            CREATE TABLE students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_number TEXT NOT NULL UNIQUE,
                full_name TEXT NOT NULL,
                email TEXT,
                course_name TEXT,
                year_of_study INTEGER,
                is_active INTEGER NOT NULL DEFAULT 1
            );
        """)
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                student_id INTEGER,
                created_at TEXT,
                is_active INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE SET NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_code TEXT NOT NULL UNIQUE,
                module_title TEXT NOT NULL,
                credit INTEGER,
                academic_year TEXT,
                is_active INTEGER NOT NULL DEFAULT 1
            );
        """)
        cursor.execute("""
            CREATE TABLE enrolments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                module_id INTEGER NOT NULL,
                enrol_date TEXT,
                is_active INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
            );
        """)
        cursor.execute("""
            CREATE TABLE attendance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                module_id INTEGER NOT NULL,
                week_number INTEGER NOT NULL,
                attended_sessions INTEGER,
                total_sessions INTEGER,
                attendance_rate REAL,
                is_active INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
            );
        """)
        cursor.execute("""
            CREATE TABLE submission_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                module_id INTEGER NOT NULL,
                assessment_name TEXT NOT NULL,
                due_date TEXT,
                submitted_date TEXT,
                is_submitted INTEGER NOT NULL DEFAULT 0,
                is_late INTEGER NOT NULL DEFAULT 0,
                is_active INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
            );
        """)
        cursor.execute("""
            CREATE TABLE survey_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                module_id INTEGER,
                week_number INTEGER NOT NULL,
                stress_level INTEGER NOT NULL,
                hours_slept REAL,
                mood_comment TEXT,
                created_at TEXT,
                is_active INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE SET NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                module_id INTEGER NOT NULL,
                assessment_name TEXT NOT NULL,
                grade REAL,
                is_active INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
            );
        """)
        cursor.execute("""
            CREATE TABLE alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                module_id INTEGER,
                week_number INTEGER,
                reason TEXT NOT NULL,
                created_at TEXT,
                resolved INTEGER NOT NULL DEFAULT 0,
                is_active INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE SET NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE stress_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                module_id INTEGER,
                survey_response_id INTEGER,
                week_number INTEGER,
                stress_level INTEGER NOT NULL,
                cause_category TEXT NOT NULL,
                description TEXT,
                source TEXT NOT NULL,
                created_at TEXT,
                is_active INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE SET NULL,
                FOREIGN KEY (survey_response_id) REFERENCES survey_responses(id) ON DELETE SET NULL
            );
        """)
        db.commit() # Commit changes after creating all tables.
        current_app.logger.info("Tables created successfully.")

        # ======================================================================
        # Phase 3: Insert comprehensive demo data for various entities.
        # This populates the tables with realistic data for testing and demonstration.
        # ======================================================================
        current_app.logger.info("Inserting demo data...")
        random.seed(42) # Seed the random number generator for reproducible demo data.
        
        # 1. Define Core Time Anchors for data generation.
        term_start_date = date(2025, 2, 3)
        registration_period_end = term_start_date - timedelta(days=10)
        registration_period_start = registration_period_end - timedelta(days=60)
        
        # 2. Staff Users (Admin, Course Director, Wellbeing Officer).
        staff_creation_start = registration_period_start - timedelta(days=30)
        users_data = [
            ("admin", generate_password_hash("admin"), "admin", None, generate_random_datetime_in_range(staff_creation_start, registration_period_start).isoformat(), 1),
            ("course_director", generate_password_hash("password"), "course_director", None, generate_random_datetime_in_range(staff_creation_start, registration_period_start).isoformat(), 1),
            ("wellbeing_officer", generate_password_hash("password"), "wellbeing_officer", None, generate_random_datetime_in_range(staff_creation_start, registration_period_start).isoformat(), 1),
        ]
        cursor.executemany("INSERT INTO users (username, password_hash, role, student_id, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?)", users_data)

        # 3. Modules.
        module_titles = [
            "Introduction to Programming", "Data Structures and Algorithms", "Database Systems",
            "Machine Learning Fundamentals", "Deep Learning Basics", "Data Visualisation",
            "Software Engineering", "AI Ethics and Society",
        ]
        module_insert_data = [
            (f"MOD10{i}", title, 15, "2025/2026", 1)
            for i, title in enumerate(module_titles, start=1)
        ]
        cursor.executemany("INSERT INTO modules (module_code, module_title, credit, academic_year, is_active) VALUES (?, ?, ?, ?, ?)", module_insert_data)
        db.commit()
        # Retrieve generated module IDs for linking with enrolments.
        cursor.execute("SELECT id FROM modules")
        module_ids = [row[0] for row in cursor.fetchall()]

        # 4. Students, linked User accounts (student role), and Enrolments.
        student_creation_dates = {} # Store creation dates to ensure enrolment is after user creation.
        course_options = ["MSc Applied AI", "MSc Data Science", "MSc Cyber Security"]
        for i in range(1, 51): # Generate 50 students.
            # A. Generate a realistic "birth" date for the student's system entry.
            user_created_at = generate_random_datetime_in_range(registration_period_start, registration_period_end)
            student_creation_dates[i] = user_created_at # Store for later use.

            # B. Create Student Record.
            student_number = f"S{i:04d}"
            full_name = f"Student {i}"
            email = f"student{i}@example.com"
            course_name = random.choice(course_options)
            year_of_study = random.randint(1, 2)
            cursor.execute("INSERT INTO students (student_number, full_name, email, course_name, year_of_study, is_active) VALUES (?, ?, ?, ?, ?, 1)",
                           (student_number, full_name, email, course_name, year_of_study))
            student_id = cursor.lastrowid
            
            # C. Create Linked User Record with 'student' role.
            cursor.execute("INSERT INTO users (username, password_hash, role, student_id, created_at, is_active) VALUES (?, ?, ?, ?, ?, 1)",
                           (email, generate_password_hash("password"), "student", student_id, user_created_at.isoformat()))

            # D. Create Enrolments for this student, ensuring enrol_date is after user_created_at.
            enrol_date = (user_created_at + timedelta(days=random.randint(1, 7))).isoformat()
            chosen_modules = random.sample(module_ids, random.randint(3, 5)) # Each student enrolls in 3-5 modules.
            for mid in chosen_modules:
                cursor.execute("INSERT INTO enrolments (student_id, module_id, enrol_date, is_active) VALUES (?, ?, ?, 1)",
                               (student_id, mid, enrol_date))
        db.commit()

        # 5. Weekly Activities (Attendance, Surveys, Submissions, Grades).
        cursor.execute("SELECT id FROM students")
        student_ids = [row[0] for row in cursor.fetchall()]
        weeks = list(range(1, 11)) # Simulate 10 academic weeks.
        assessment_names = ["Assignment 1", "Assignment 2"]

        for sid in student_ids:
            # Get modules each student is enrolled in.
            cursor.execute("SELECT module_id FROM enrolments WHERE student_id = ?", (sid,))
            enrolled_mids = [row[0] for row in cursor.fetchall()]

            for mid in enrolled_mids:
                for w in weeks:
                    # A. Attendance Records.
                    total_sessions = 2 # Assume 2 sessions per module per week.
                    attended_sessions = random.randint(0, total_sessions)
                    attendance_rate = attended_sessions / total_sessions if total_sessions > 0 else 0.0
                    cursor.execute("INSERT INTO attendance_records (student_id, module_id, week_number, attended_sessions, total_sessions, attendance_rate, is_active) VALUES (?, ?, ?, ?, ?, ?, 1);",
                                   (sid, mid, w, attended_sessions, total_sessions, attendance_rate))

                    # B. Survey Responses (stress levels, sleep, mood).
                    week_date = term_start_date + timedelta(weeks=w - 1)
                    created_at_dt = datetime.combine(week_date, datetime.min.time()).replace(hour=random.randint(9, 22), minute=random.randint(0, 59))
                    # Stress level influenced by attendance rate for realism.
                    stress_level = int(round(max(1, min(5, random.gauss(3 + (1 - attendance_rate) * 2, 0.8)))))
                    hours_slept = max(3.0, min(10.0, random.gauss(7 + attendance_rate, 1.0)))
                    cursor.execute("INSERT INTO survey_responses (student_id, module_id, week_number, stress_level, hours_slept, mood_comment, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, 1);",
                                   (sid, mid, w, stress_level, hours_slept, None, created_at_dt.isoformat()))
                db.commit() # Commit weekly activities per student per module.

            # C. Submissions & Grades (relative to due dates).
            for idx, aname in enumerate(assessment_names, start=1):
                due_date = term_start_date + timedelta(weeks=(4 if idx == 1 else 8) - 1) # Due dates for Assignment 1 (Week 4) and 2 (Week 8).
                is_submitted = 1 if random.random() < 0.9 else 0 # 90% chance of submission.
                submitted_date_str = None
                is_late = 0
                if is_submitted:
                    # Simulate submission date: mostly on time, some late.
                    delta_days = -random.randint(0, 2) if random.random() < 0.8 else random.randint(1, 5)
                    submitted_date = due_date + timedelta(days=delta_days)
                    submitted_date_str = datetime.combine(submitted_date, datetime.min.time()).replace(hour=random.randint(9, 17)).isoformat()
                    if submitted_date > due_date:
                        is_late = 1

                cursor.execute("INSERT INTO submission_records (student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, 1);",
                               (sid, mid, aname, due_date.isoformat(), submitted_date_str, is_submitted, is_late))
                
                # Assign grades: higher for submitted, lower for not submitted/late.
                grade_value = random.uniform(40.0, 95.0) if is_submitted else random.uniform(0, 35)
                if is_submitted and is_late: # Penalty for late submission.
                    grade_value = max(0.0, grade_value - random.uniform(5, 15))
                cursor.execute("INSERT INTO grades (student_id, module_id, assessment_name, grade, is_active) VALUES (?, ?, ?, ?, 1);",
                               (sid, mid, aname, grade_value))
            db.commit() # Commit submissions and grades per student per module.

        # 6. Stress Events and Alerts (generated chronologically after surveys).
        # Retrieve all survey responses to process for events and alerts.
        cursor.execute("SELECT id, student_id, module_id, week_number, stress_level, created_at FROM survey_responses WHERE is_active = 1 ORDER BY created_at")
        all_surveys = cursor.fetchall()
        
        for survey_row in all_surveys:
            survey_time = datetime.fromisoformat(survey_row['created_at'])
            # A. Create Stress Events for high stress levels.
            if survey_row['stress_level'] >= 4: # Threshold for high stress.
                event_time = survey_time + timedelta(minutes=random.randint(5, 120)) # Event occurs shortly after survey.
                cursor.execute("INSERT OR IGNORE INTO stress_events (student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1);",
                               (survey_row['student_id'], survey_row['module_id'], survey_row['id'], survey_row['week_number'], survey_row['stress_level'], random.choice(["academic", "personal"]), f"High stress reported (level {survey_row['stress_level']}).", "survey_response_system", event_time.isoformat()))
        db.commit() # Commit all generated stress events.

        # B. Create Alerts for consecutive high stress.
        # Re-fetch survey responses filtered for high stress to check for patterns.
        cursor.execute("SELECT student_id, module_id, week_number, stress_level, created_at FROM survey_responses WHERE stress_level >= 4 AND is_active = 1 ORDER BY student_id, module_id, week_number")
        high_stress_surveys = cursor.fetchall()
        for i in range(1, len(high_stress_surveys)):
            current = high_stress_surveys[i]
            prev = high_stress_surveys[i-1]
            # Check for consecutive weeks of high stress for the same student in the same module.
            if current['student_id'] == prev['student_id'] and \
               current['module_id'] == prev['module_id'] and \
               current['week_number'] == prev['week_number'] + 1:
                
                alert_time = datetime.fromisoformat(current['created_at']) + timedelta(hours=random.randint(1, 5)) # Alert generated shortly after second high-stress survey.
                reason = (f"Stress level >= 4 for two consecutive weeks ({prev['week_number']} and {current['week_number']}) "
                          f"in module_id={current['module_id']} for student_id={current['student_id']}.")
                cursor.execute("INSERT OR IGNORE INTO alerts (student_id, module_id, week_number, reason, created_at, resolved, is_active) VALUES (?, ?, ?, ?, ?, 0, 1);",
                               (current['student_id'], current['module_id'], current['week_number'], reason, alert_time.isoformat()))
        db.commit() # Commit all generated alerts.

        current_app.logger.info("Database seeding completed successfully.")

    except ConnectionError as e:
        # Handle critical database connection errors during seeding.
        current_app.logger.critical(f"Database connection error during seeding: {e}")
        if db:
            db.rollback() # Ensure transaction is rolled back if connection fails after starting.
        raise # Re-raise to propagate the error to the calling CLI command.
    except sqlite3.Error as e:
        # Handle specific SQLite database errors during seeding.
        current_app.logger.error(f"Database error during seeding: {e}", exc_info=True)
        if db:
            db.rollback() # Rollback the transaction on any SQL execution error.
        raise # Re-raise to propagate the error.
    except Exception as e:
        # Catch any other unexpected errors during the seeding process.
        current_app.logger.error(f"An unexpected error occurred during seeding: {e}", exc_info=True)
        if db:
            db.rollback() # Rollback for any other unexpected errors.
        raise # Re-raise to propagate the error.
