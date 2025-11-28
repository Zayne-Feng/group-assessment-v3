import random
from datetime import date, timedelta, datetime
from app.db_connection import get_db
from werkzeug.security import generate_password_hash

def seed_data():
    db = get_db()
    cursor = db.cursor()

    # ================
    # Drop existing tables to ensure a clean slate
    # ================
    drop_statements = [
        "DROP TABLE IF EXISTS stress_events;",
        "DROP TABLE IF EXISTS alerts;",
        "DROP TABLE IF EXISTS grades;",
        "DROP TABLE IF EXISTS submission_records;",
        "DROP TABLE IF EXISTS attendance_records;",
        "DROP TABLE IF EXISTS survey_responses;",
        "DROP TABLE IF EXISTS enrolments;",
        "DROP TABLE IF EXISTS modules;",
        "DROP TABLE IF EXISTS students;",
        "DROP TABLE IF EXISTS users;",
    ]
    for stmt in drop_statements:
        cursor.execute(stmt)
    db.commit()

    # ================
    # Create Tables
    # ================
    # User table
    cursor.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT,
            is_active INTEGER NOT NULL DEFAULT 1
        );
        """
    )

    # Student table
    cursor.execute(
        """
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_number TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL,
            email TEXT,
            course_name TEXT,
            year_of_study INTEGER,
            is_active INTEGER NOT NULL DEFAULT 1
        );
        """
    )

    # Module table
    cursor.execute(
        """
        CREATE TABLE modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_code TEXT NOT NULL UNIQUE,
            module_title TEXT NOT NULL,
            credit INTEGER,
            academic_year TEXT,
            is_active INTEGER NOT NULL DEFAULT 1
        );
        """
    )

    # Enrolment table
    cursor.execute(
        """
        CREATE TABLE enrolments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            module_id INTEGER NOT NULL,
            enrol_date TEXT,
            is_active INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
            FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
        );
        """
    )

    # Attendance Records table
    cursor.execute(
        """
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
        """
    )

    # Submission Records table
    cursor.execute(
        """
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
        """
    )

    # Survey Responses table
    cursor.execute(
        """
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
        """
    )

    # Grades table
    cursor.execute(
        """
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
        """
    )

    # Alerts table
    cursor.execute(
        """
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
        """
    )

    # Stress Events table
    cursor.execute(
        """
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
        """
    )
    db.commit()

    # ================
    # Insert Demo Data
    # ================
    random.seed(42)

    # 1. Users
    users_data = [
        ("admin", generate_password_hash("admin"), "admin", datetime.utcnow().isoformat(), 1),
        ("course_director", generate_password_hash("password"), "course_director", datetime.utcnow().isoformat(), 1),
        ("wellbeing_officer", generate_password_hash("password"), "wellbeing_officer", datetime.utcnow().isoformat(), 1),
    ]
    cursor.executemany(
        "INSERT INTO users (username, password_hash, role, created_at, is_active) VALUES (?, ?, ?, ?, ?)",
        users_data
    )

    # 2. Modules
    module_codes = [f"MOD10{i}" for i in range(1, 9)]
    module_titles = [
        "Introduction to Programming", "Data Structures and Algorithms", "Database Systems",
        "Machine Learning Fundamentals", "Deep Learning Basics", "Data Visualisation",
        "Software Engineering", "AI Ethics and Society",
    ]
    modules_to_insert = []
    for code, title in zip(module_codes, module_titles):
        modules_to_insert.append((code, title, 15, "2025/2026", 1))
    cursor.executemany(
        "INSERT INTO modules (module_code, module_title, credit, academic_year, is_active) VALUES (?, ?, ?, ?, ?)",
        modules_to_insert
    )
    db.commit() # Commit to get module IDs

    cursor.execute("SELECT id FROM modules")
    module_ids = [row[0] for row in cursor.fetchall()]

    # 3. Students
    course_options = ["MSc Applied AI", "MSc Data Science", "MSc Cyber Security"]
    students_to_insert = []
    for i in range(1, 51):
        student_number = f"S{i:04d}"
        full_name = f"Student {i}"
        email = f"student{i}@example.com"
        course_name = random.choice(course_options)
        year_of_study = random.randint(1, 2)
        students_to_insert.append((student_number, full_name, email, course_name, year_of_study, 1))
    cursor.executemany(
        "INSERT INTO students (student_number, full_name, email, course_name, year_of_study, is_active) VALUES (?, ?, ?, ?, ?, ?)",
        students_to_insert
    )
    db.commit() # Commit to get student IDs

    cursor.execute("SELECT id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]

    # 4. Enrolments
    enrolments_to_insert = []
    base_enrol_date = date(2025, 1, 10)
    for sid in student_ids:
        k = random.randint(3, 5)
        chosen_modules = random.sample(module_ids, k)
        for mid in chosen_modules:
            enrol_date = (base_enrol_date + timedelta(days=random.randint(0, 10))).isoformat()
            enrolments_to_insert.append((sid, mid, enrol_date, 1))
    cursor.executemany(
        "INSERT INTO enrolments (student_id, module_id, enrol_date, is_active) VALUES (?, ?, ?, ?)",
        enrolments_to_insert
    )
    db.commit()

    # 5. Attendance, Surveys, Submissions, Grades
    weeks = list(range(1, 11))
    base_week_date = date(2025, 2, 3)
    assessment_names = ["Assignment 1", "Assignment 2"]

    for sid in student_ids:
        # Get modules student is enrolled in
        cursor.execute("SELECT module_id FROM enrolments WHERE student_id = ?", (sid,))
        enrolled_mids = [row[0] for row in cursor.fetchall()]

        for mid in enrolled_mids:
            for w in weeks:
                # Attendance
                total_sessions = 2
                attended_sessions = random.randint(0, total_sessions)
                attendance_rate = attended_sessions / total_sessions if total_sessions > 0 else 0.0
                cursor.execute(
                    """
                    INSERT INTO attendance_records (student_id, module_id, week_number, attended_sessions, total_sessions, attendance_rate, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, 1);
                    """,
                    (sid, mid, w, attended_sessions, total_sessions, attendance_rate),
                )

                # Survey
                base_stress = 3 + (1 - attendance_rate) * 2
                stress_level = int(round(max(1, min(5, random.gauss(base_stress, 0.8)))))
                base_sleep = 7 + attendance_rate
                hours_slept = max(3.0, min(10.0, random.gauss(base_sleep, 1.0)))
                week_date = base_week_date + timedelta(weeks=w - 1)
                created_at = f"{week_date.isoformat()}T21:00:00"

                cursor.execute(
                    """
                    INSERT INTO survey_responses (student_id, module_id, week_number, stress_level, hours_slept, mood_comment, created_at, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 1);
                    """,
                    (sid, mid, w, stress_level, hours_slept, None, created_at),
                )
            db.commit() # Commit surveys and attendance to get IDs

            # Submissions & Grades
            for idx, aname in enumerate(assessment_names, start=1):
                due_week = 4 if idx == 1 else 8
                due_date = (base_week_date + timedelta(weeks=due_week - 1)).isoformat()

                is_submitted = 1 if random.random() < 0.9 else 0
                is_late = 0
                submitted_date_str = None

                if is_submitted:
                    if random.random() < 0.8:
                        delta_days = -random.randint(0, 2)
                        is_late = 0
                    else:
                        delta_days = random.randint(1, 5)
                        is_late = 1
                    submitted_date_str = (datetime.fromisoformat(due_date) + timedelta(days=delta_days)).isoformat()

                cursor.execute(
                    """
                    INSERT INTO submission_records (student_id, module_id, assessment_name, due_date, submitted_date, is_submitted, is_late, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 1);
                    """,
                    (sid, mid, aname, due_date, submitted_date_str, is_submitted, is_late),
                )

                grade_value = random.uniform(40.0, 95.0) if is_submitted else random.uniform(0, 35)
                if is_late:
                    grade_value = max(0.0, grade_value - random.uniform(5, 15))

                cursor.execute(
                    """
                    INSERT INTO grades (student_id, module_id, assessment_name, grade, is_active)
                    VALUES (?, ?, ?, ?, 1);
                    """,
                    (sid, mid, aname, grade_value),
                )
            db.commit() # Commit submissions and grades

    # 6. Stress Events and Alerts (based on generated survey data)
    cursor.execute("SELECT id, student_id, module_id, week_number, stress_level, created_at FROM survey_responses WHERE is_active = 1 ORDER BY student_id, module_id, week_number")
    all_surveys = cursor.fetchall()
    
    survey_map = {}
    for s_row in all_surveys:
        key = (s_row['student_id'], s_row['module_id'])
        if key not in survey_map:
            survey_map[key] = []
        survey_map[key].append(s_row)

    for (sid, mid), surveys_for_student_module in survey_map.items():
        surveys_for_student_module.sort(key=lambda x: x['week_number'])
        
        for i, current_survey_row in enumerate(surveys_for_student_module):
            # Stress Event
            if current_survey_row['stress_level'] >= 4:
                cursor.execute("SELECT id FROM stress_events WHERE survey_response_id = ?", (current_survey_row['id'],))
                existing_event = cursor.fetchone()
                if not existing_event:
                    cause_category = random.choice(["academic", "personal", "health", "financial", "other"])
                    description = f"High stress reported (level {current_survey_row['stress_level']}) in week {current_survey_row['week_number']}."
                    source = "system"
                    cursor.execute(
                        """
                        INSERT INTO stress_events (student_id, module_id, survey_response_id, week_number, stress_level, cause_category, description, source, created_at, is_active)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1);
                        """,
                        (sid, mid, current_survey_row['id'], current_survey_row['week_number'], current_survey_row['stress_level'], cause_category, description, source, current_survey_row['created_at']),
                    )
            
            # Alert (consecutive high stress)
            if i > 0:
                prev_survey_row = surveys_for_student_module[i-1]
                if prev_survey_row['week_number'] == current_survey_row['week_number'] - 1 and \
                   prev_survey_row['stress_level'] >= 4 and \
                   current_survey_row['stress_level'] >= 4:
                    
                    cursor.execute("SELECT id FROM alerts WHERE student_id = ? AND week_number = ? AND is_active = 1", (sid, current_survey_row['week_number'],))
                    existing_alert = cursor.fetchone()
                    if not existing_alert:
                        reason = f"Stress level >= 4 for two consecutive weeks ({prev_survey_row['week_number']} and {current_survey_row['week_number']}) in module_id={mid}."
                        created_at = datetime.utcnow().isoformat(timespec="seconds")
                        cursor.execute(
                            """
                            INSERT INTO alerts (student_id, module_id, week_number, reason, created_at, resolved, is_active)
                            VALUES (?, ?, ?, ?, ?, 0, 1);
                            """,
                            (sid, mid, current_survey_row['week_number'], reason, created_at),
                        )
    db.commit()
