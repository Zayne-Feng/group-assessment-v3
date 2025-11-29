import random
from datetime import date, timedelta, datetime
from app.db_connection import get_db
from werkzeug.security import generate_password_hash

def generate_random_datetime_in_range(start_date, end_date):
    """Generates a random datetime within a given range."""
    time_difference = end_date - start_date
    random_seconds = random.randint(0, int(time_difference.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

def seed_data():
    db = get_db()
    cursor = db.cursor()

    # ================
    # Drop existing tables
    # ================
    drop_statements = [
        "DROP TABLE IF EXISTS stress_events;", "DROP TABLE IF EXISTS alerts;", "DROP TABLE IF EXISTS grades;",
        "DROP TABLE IF EXISTS submission_records;", "DROP TABLE IF EXISTS attendance_records;",
        "DROP TABLE IF EXISTS survey_responses;", "DROP TABLE IF EXISTS enrolments;", "DROP TABLE IF EXISTS modules;",
        "DROP TABLE IF EXISTS users;", "DROP TABLE IF EXISTS students;",
    ]
    for stmt in drop_statements:
        cursor.execute(stmt)
    db.commit()

    # ================
    # Create Tables (Schema remains the same)
    # ================
    # (Assuming the schema creation part is correct from previous steps)
    cursor.execute("CREATE TABLE students (id INTEGER PRIMARY KEY AUTOINCREMENT, student_number TEXT NOT NULL UNIQUE, full_name TEXT NOT NULL, email TEXT, course_name TEXT, year_of_study INTEGER, is_active INTEGER NOT NULL DEFAULT 1);")
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, role TEXT NOT NULL, student_id INTEGER, created_at TEXT, is_active INTEGER NOT NULL DEFAULT 1, FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE SET NULL);")
    cursor.execute("CREATE TABLE modules (id INTEGER PRIMARY KEY AUTOINCREMENT, module_code TEXT NOT NULL UNIQUE, module_title TEXT NOT NULL, credit INTEGER, academic_year TEXT, is_active INTEGER NOT NULL DEFAULT 1);")
    cursor.execute("CREATE TABLE enrolments (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL, module_id INTEGER NOT NULL, enrol_date TEXT, is_active INTEGER NOT NULL DEFAULT 1, FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE, FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE);")
    cursor.execute("CREATE TABLE attendance_records (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL, module_id INTEGER NOT NULL, week_number INTEGER NOT NULL, attended_sessions INTEGER, total_sessions INTEGER, attendance_rate REAL, is_active INTEGER NOT NULL DEFAULT 1, FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE, FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE);")
    cursor.execute("CREATE TABLE submission_records (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL, module_id INTEGER NOT NULL, assessment_name TEXT NOT NULL, due_date TEXT, submitted_date TEXT, is_submitted INTEGER NOT NULL DEFAULT 0, is_late INTEGER NOT NULL DEFAULT 0, is_active INTEGER NOT NULL DEFAULT 1, FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE, FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE);")
    cursor.execute("CREATE TABLE survey_responses (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL, module_id INTEGER, week_number INTEGER NOT NULL, stress_level INTEGER NOT NULL, hours_slept REAL, mood_comment TEXT, created_at TEXT, is_active INTEGER NOT NULL DEFAULT 1, FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE, FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE SET NULL);")
    cursor.execute("CREATE TABLE grades (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL, module_id INTEGER NOT NULL, assessment_name TEXT NOT NULL, grade REAL, is_active INTEGER NOT NULL DEFAULT 1, FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE, FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE);")
    cursor.execute("CREATE TABLE alerts (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL, module_id INTEGER, week_number INTEGER, reason TEXT NOT NULL, created_at TEXT, resolved INTEGER NOT NULL DEFAULT 0, is_active INTEGER NOT NULL DEFAULT 1, FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE, FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE SET NULL);")
    cursor.execute("CREATE TABLE stress_events (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL, module_id INTEGER, survey_response_id INTEGER, week_number INTEGER, stress_level INTEGER NOT NULL, cause_category TEXT NOT NULL, description TEXT, source TEXT NOT NULL, created_at TEXT, is_active INTEGER NOT NULL DEFAULT 1, FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE, FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE SET NULL, FOREIGN KEY (survey_response_id) REFERENCES survey_responses(id) ON DELETE SET NULL);")
    db.commit()

    # ================
    # Insert Demo Data with Realistic Timelines
    # ================
    random.seed(42)
    
    # 1. Define Core Time Anchors
    term_start_date = date(2025, 2, 3)
    registration_period_end = term_start_date - timedelta(days=10)
    registration_period_start = registration_period_end - timedelta(days=60)
    
    # 2. Staff Users
    staff_creation_start = registration_period_start - timedelta(days=30)
    users_data = [
        ("admin", generate_password_hash("admin"), "admin", None, generate_random_datetime_in_range(staff_creation_start, registration_period_start).isoformat(), 1),
        ("course_director", generate_password_hash("password"), "course_director", None, generate_random_datetime_in_range(staff_creation_start, registration_period_start).isoformat(), 1),
        ("wellbeing_officer", generate_password_hash("password"), "wellbeing_officer", None, generate_random_datetime_in_range(staff_creation_start, registration_period_start).isoformat(), 1),
    ]
    cursor.executemany("INSERT INTO users (username, password_hash, role, student_id, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?)", users_data)

    # 3. Modules
    cursor.executemany("INSERT INTO modules (module_code, module_title, credit, academic_year, is_active) VALUES (?, ?, ?, ?, ?)", [ (f"MOD10{i}", title, 15, "2025/2026", 1) for i, title in enumerate([ "Introduction to Programming", "Data Structures and Algorithms", "Database Systems", "Machine Learning Fundamentals", "Deep Learning Basics", "Data Visualisation", "Software Engineering", "AI Ethics and Society", ], start=1) ])
    db.commit()
    cursor.execute("SELECT id FROM modules")
    module_ids = [row[0] for row in cursor.fetchall()]

    # 4. Students, Users (student role), and Enrolments
    student_creation_dates = {}
    course_options = ["MSc Applied AI", "MSc Data Science", "MSc Cyber Security"]
    for i in range(1, 51):
        # A. Generate the student's "birth" date in the system
        user_created_at = generate_random_datetime_in_range(registration_period_start, registration_period_end)
        student_creation_dates[i] = user_created_at # Store for later use

        # B. Create Student Record
        cursor.execute("INSERT INTO students (student_number, full_name, email, course_name, year_of_study, is_active) VALUES (?, ?, ?, ?, ?, 1)", (f"S{i:04d}", f"Student {i}", f"student{i}@example.com", random.choice(course_options), random.randint(1, 2)))
        student_id = cursor.lastrowid
        
        # C. Create Linked User Record with the "birth" date
        cursor.execute("INSERT INTO users (username, password_hash, role, student_id, created_at, is_active) VALUES (?, ?, ?, ?, ?, 1)", (f"student{i}@example.com", generate_password_hash("password"), "student", student_id, user_created_at.isoformat()))

        # D. Create Enrolments for this student, ensuring enrol_date is AFTER user_created_at
        enrol_date = (user_created_at + timedelta(days=random.randint(1, 7))).isoformat() # Removed extra .date()
        chosen_modules = random.sample(module_ids, random.randint(3, 5))
        for mid in chosen_modules:
            cursor.execute("INSERT INTO enrolments (student_id, module_id, enrol_date, is_active) VALUES (?, ?, ?, 1)", (student_id, mid, enrol_date))
    db.commit()

    # 5. Weekly Activities (Attendance, Surveys, etc.)
    cursor.execute("SELECT id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]
    weeks = list(range(1, 11))
    assessment_names = ["Assignment 1", "Assignment 2"]

    for sid in student_ids:
        cursor.execute("SELECT module_id FROM enrolments WHERE student_id = ?", (sid,))
        enrolled_mids = [row[0] for row in cursor.fetchall()]

        for mid in enrolled_mids:
            for w in weeks:
                # A. Attendance
                total_sessions = 2
                attended_sessions = random.randint(0, total_sessions)
                attendance_rate = attended_sessions / total_sessions if total_sessions > 0 else 0.0
                cursor.execute("INSERT INTO attendance_records (student_id, module_id, week_number, attended_sessions, total_sessions, attendance_rate, is_active) VALUES (?, ?, ?, ?, ?, ?, 1);", (sid, mid, w, attended_sessions, total_sessions, attendance_rate))

                # B. Survey (created_at is relative to the week)
                week_date = term_start_date + timedelta(weeks=w - 1)
                created_at_dt = datetime.combine(week_date, datetime.min.time()).replace(hour=random.randint(9, 22), minute=random.randint(0, 59))
                stress_level = int(round(max(1, min(5, random.gauss(3 + (1 - attendance_rate) * 2, 0.8)))))
                hours_slept = max(3.0, min(10.0, random.gauss(7 + attendance_rate, 1.0)))
                cursor.execute("INSERT INTO survey_responses (student_id, module_id, week_number, stress_level, hours_slept, mood_comment, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, 1);", (sid, mid, w, stress_level, hours_slept, None, created_at_dt.isoformat()))
            db.commit()

            # C. Submissions & Grades (relative to due dates)
            for idx, aname in enumerate(assessment_names, start=1):
                due_date = term_start_date + timedelta(weeks=(4 if idx == 1 else 8) - 1)
                is_submitted = 1 if random.random() < 0.9 else 0
                submitted_date_str = None
                if is_submitted:
                    delta_days = -random.randint(0, 2) if random.random() < 0.8 else random.randint(1, 5)
                    submitted_date = due_date + timedelta(days=delta_days)
                    submitted_date_str = datetime.combine(submitted_date, datetime.min.time()).replace(hour=random.randint(9, 17)).isoformat()
                cursor.execute("INSERT INTO submission_records (student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, 1);", (sid, mid, aname, due_date.isoformat(), submitted_date_str, is_submitted, 1 if is_submitted and (submitted_date > due_date) else 0))
                
                grade_value = random.uniform(40.0, 95.0) if is_submitted else random.uniform(0, 35)
                if is_submitted and (submitted_date > due_date): grade_value = max(0.0, grade_value - random.uniform(5, 15))
                cursor.execute("INSERT INTO grades (student_id, module_id, assessment_name, grade, is_active) VALUES (?, ?, ?, ?, 1);", (sid, mid, aname, grade_value))
            db.commit()

    # 6. Stress Events and Alerts (chronologically after surveys)
    cursor.execute("SELECT id, student_id, module_id, week_number, stress_level, created_at FROM survey_responses WHERE is_active = 1 ORDER BY created_at")
    all_surveys = cursor.fetchall()
    
    for survey_row in all_surveys:
        survey_time = datetime.fromisoformat(survey_row['created_at'])
        if survey_row['stress_level'] >= 4:
            event_time = survey_time + timedelta(minutes=random.randint(5, 120))
            cursor.execute("INSERT OR IGNORE INTO stress_events (student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1);", (survey_row['student_id'], survey_row['module_id'], survey_row['id'], survey_row['week_number'], survey_row['stress_level'], random.choice(["academic", "personal"]), f"High stress reported (level {survey_row['stress_level']}).", "system", event_time.isoformat()))
    db.commit()

    # Re-fetch surveys to check for consecutive stress
    cursor.execute("SELECT student_id, module_id, week_number, stress_level, created_at FROM survey_responses WHERE stress_level >= 4 AND is_active = 1 ORDER BY student_id, module_id, week_number")
    high_stress_surveys = cursor.fetchall()
    for i in range(1, len(high_stress_surveys)):
        current = high_stress_surveys[i]
        prev = high_stress_surveys[i-1]
        if current['student_id'] == prev['student_id'] and current['module_id'] == prev['module_id'] and current['week_number'] == prev['week_number'] + 1:
            alert_time = datetime.fromisoformat(current['created_at']) + timedelta(hours=random.randint(1, 5))
            reason = f"Stress level >= 4 for two consecutive weeks ({prev['week_number']} and {current['week_number']}) in module_id={current['module_id']}."
            cursor.execute("INSERT OR IGNORE INTO alerts (student_id, module_id, week_number, reason, created_at, resolved, is_active) VALUES (?, ?, ?, ?, ?, 0, 1);", (current['student_id'], current['module_id'], current['week_number'], reason, alert_time.isoformat()))
    db.commit()
