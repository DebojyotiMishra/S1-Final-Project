from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import matplotlib
matplotlib.use('agg')  # Use the Agg backend
import matplotlib.pyplot as plt


app = Flask(__name__)
db = mysql.connector.connect(host="localhost", user="root", passwd="", database="db")


@app.route("/")
def index():
    cursor = db.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM students\
                    WHERE student_population_code_ref = 'AIs' AND student_population_year_ref = '2021';"
    )
    count_ais = cursor.fetchall()

    cursor2 = db.cursor()
    cursor2.execute(
        "SELECT COUNT(*) FROM students\
                    WHERE student_population_code_ref = 'CS' AND student_population_year_ref = '2021';"
    )
    count_cs = cursor2.fetchall()

    cursor3 = db.cursor()
    cursor3.execute(
        "SELECT COUNT(*) FROM students\
                    WHERE student_population_code_ref = 'DSA' AND student_population_year_ref = '2021';"
    )
    count_dsa = cursor3.fetchall()
    
    cursor4 = db.cursor()
    cursor4.execute(
        "SELECT COUNT(*) FROM students\
                    WHERE student_population_code_ref = 'ISM' AND student_population_year_ref = '2021';"
    )
    count_ism = cursor4.fetchall()
    
    cursor5 = db.cursor()
    cursor5.execute(
        "SELECT COUNT(*) FROM students\
                    WHERE student_population_code_ref = 'SE' AND student_population_year_ref = '2021';"
    )
    count_se = cursor5.fetchall()

    students = (count_ais, count_cs, count_dsa, count_ism, count_se)
    
    # ------------ Attendance ------------
    # ----- AIs -----
    cursor6 = db.cursor()
    cursor6.execute("SELECT\
                        s.student_population_code_ref,\
                        COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) AS total_presences,\
                        COUNT(*) AS total_records,\
                        ROUND((COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) * 100.0 / COUNT(*)), 2) AS presence_percentage\
                    FROM\
                        students s\
                    LEFT JOIN\
                        attendance a ON s.student_epita_email = a.attendance_student_ref\
                    WHERE\
                        s.student_population_code_ref = 'AIs'\
                        AND a.attendance_population_year_ref = 2021\
                    GROUP BY\
                        s.student_population_code_ref;")
    attendance_ais = cursor6.fetchall()
    
    # ----- CS -----
    cursor7 = db.cursor()
    cursor7.execute("SELECT\
                        s.student_population_code_ref,\
                        COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) AS total_presences,\
                        COUNT(*) AS total_records,\
                        ROUND((COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) * 100.0 / COUNT(*)), 2) AS presence_percentage\
                    FROM\
                        students s\
                    LEFT JOIN\
                        attendance a ON s.student_epita_email = a.attendance_student_ref\
                    WHERE\
                        s.student_population_code_ref = 'CS'\
                        AND a.attendance_population_year_ref = 2021\
                    GROUP BY\
                        s.student_population_code_ref;")
    attendance_cs = cursor7.fetchall()
    
    # ----- DSA -----
    cursor8 = db.cursor()
    cursor8.execute("SELECT\
                        s.student_population_code_ref,\
                        COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) AS total_presences,\
                        COUNT(*) AS total_records,\
                        ROUND((COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) * 100.0 / COUNT(*)), 2) AS presence_percentage\
                    FROM\
                        students s\
                    LEFT JOIN\
                        attendance a ON s.student_epita_email = a.attendance_student_ref\
                    WHERE\
                        s.student_population_code_ref = 'DSA'\
                        AND a.attendance_population_year_ref = 2021\
                    GROUP BY\
                        s.student_population_code_ref;")
    attendance_dsa = cursor8.fetchall()
    
    # ----- ISM -----
    cursor9 = db.cursor()
    cursor9.execute("SELECT\
                        s.student_population_code_ref,\
                        COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) AS total_presences,\
                        COUNT(*) AS total_records,\
                        ROUND((COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) * 100.0 / COUNT(*)), 2) AS presence_percentage\
                    FROM\
                        students s\
                    LEFT JOIN\
                        attendance a ON s.student_epita_email = a.attendance_student_ref\
                    WHERE\
                        s.student_population_code_ref = 'ISM'\
                        AND a.attendance_population_year_ref = 2021\
                    GROUP BY\
                        s.student_population_code_ref;")
    attendance_ism = cursor9.fetchall()
    
    # ----- SE -----
    cursor10 = db.cursor()
    cursor10.execute("SELECT\
                        s.student_population_code_ref,\
                        COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) AS total_presences,\
                        COUNT(*) AS total_records,\
                        ROUND((COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) * 100.0 / COUNT(*)), 2) AS presence_percentage\
                    FROM\
                        students s\
                    LEFT JOIN\
                        attendance a ON s.student_epita_email = a.attendance_student_ref\
                    WHERE\
                        s.student_population_code_ref = 'SE'\
                        AND a.attendance_population_year_ref = 2021\
                    GROUP BY\
                        s.student_population_code_ref;")
    attendance_se = cursor10.fetchall()
    
    
    attendance = (attendance_ais, attendance_cs, attendance_dsa, attendance_ism, attendance_se)
    return render_template("index.html", students=students, attendance=attendance)

@app.route("/populations/ais")
def populations_ais():
    cursor = db.cursor()
    # cursor.execute("SELECT students.student_epita_email, contacts.contact_first_name, contacts.contact_last_name\
    #                FROM students\
    #                JOIN contacts ON students.student_contact_ref = contacts.contact_email\
    #                WHERE student_population_code_ref = 'AIs'")
    cursor.execute("SELECT\
                        s.student_epita_email AS email,\
                        c.contact_first_name AS first_name,\
                        c.contact_last_name AS last_name,\
                        CONCAT(\
                            COALESCE(passed_classes.passed_count, 0),\
                            '/',\
                            COALESCE(total_classes.total_count, 0)\
                        ) AS passed_classes_over_total\
                    FROM\
                        students s\
                    JOIN\
                        contacts c ON s.student_contact_ref = c.contact_email\
                    LEFT JOIN\
                        (SELECT\
                            grade_student_epita_email_ref,\
                            COUNT(*) AS passed_count\
                        FROM\
                            (SELECT\
                                grade_student_epita_email_ref,\
                                grade_course_code_ref,\
                                AVG(grade_score) AS avg_grade\
                            FROM\
                                grades\
                            GROUP BY\
                                grade_student_epita_email_ref, grade_course_code_ref\
                            ) AS avg_grades\
                        WHERE\
                            avg_grade >= 10\
                        GROUP BY\
                            grade_student_epita_email_ref\
                        ) AS passed_classes\
                    ON\
                        s.student_epita_email = passed_classes.grade_student_epita_email_ref\
                    LEFT JOIN\
                        (SELECT\
                            grade_student_epita_email_ref,\
                            COUNT(*) AS total_count\
                        FROM\
                            (SELECT\
                                grade_student_epita_email_ref,\
                                grade_course_code_ref\
                            FROM\
                                grades\
                            GROUP BY\
                                grade_student_epita_email_ref, grade_course_code_ref\
                            ) AS distinct_courses\
                        GROUP BY\
                            grade_student_epita_email_ref\
                        ) AS total_classes\
                    ON\
                        s.student_epita_email = total_classes.grade_student_epita_email_ref\
                    WHERE\
                        s.student_population_code_ref = 'AIs' AND student_population_year_ref = '2021';\
                    ")
                            
    students = cursor.fetchall()
    
    cursor2 = db.cursor()
    cursor2.execute("SELECT DISTINCT c.course_code, c.course_name, c.duration\
                    FROM students s\
                    JOIN grades g ON s.student_epita_email = g.grade_student_epita_email_ref\
                    JOIN courses c ON g.grade_course_code_ref = c.course_code\
                    WHERE s.student_population_code_ref = 'AIs';")
    courses = cursor2.fetchall()
    return render_template("populations/msc-ai.html", students=students, courses=courses)


@app.route("/populations/cs")
def populations_cs():
    cursor = db.cursor()
    # cursor.execute("SELECT students.student_epita_email, contacts.contact_first_name, contacts.contact_last_name\
    #                FROM students\
    #                JOIN contacts ON students.student_contact_ref = contacts.contact_email\
    #                WHERE student_population_code_ref = 'AIs'")
    cursor.execute("SELECT\
                        s.student_epita_email AS email,\
                        c.contact_first_name AS first_name,\
                        c.contact_last_name AS last_name,\
                        CONCAT(\
                            COALESCE(passed_classes.passed_count, 0),\
                            '/',\
                            COALESCE(total_classes.total_count, 0)\
                        ) AS passed_classes_over_total\
                    FROM\
                        students s\
                    JOIN\
                        contacts c ON s.student_contact_ref = c.contact_email\
                    LEFT JOIN\
                        (SELECT\
                            grade_student_epita_email_ref,\
                            COUNT(*) AS passed_count\
                        FROM\
                            (SELECT\
                                grade_student_epita_email_ref,\
                                grade_course_code_ref,\
                                AVG(grade_score) AS avg_grade\
                            FROM\
                                grades\
                            GROUP BY\
                                grade_student_epita_email_ref, grade_course_code_ref\
                            ) AS avg_grades\
                        WHERE\
                            avg_grade >= 10\
                        GROUP BY\
                            grade_student_epita_email_ref\
                        ) AS passed_classes\
                    ON\
                        s.student_epita_email = passed_classes.grade_student_epita_email_ref\
                    LEFT JOIN\
                        (SELECT\
                            grade_student_epita_email_ref,\
                            COUNT(*) AS total_count\
                        FROM\
                            (SELECT\
                                grade_student_epita_email_ref,\
                                grade_course_code_ref\
                            FROM\
                                grades\
                            GROUP BY\
                                grade_student_epita_email_ref, grade_course_code_ref\
                            ) AS distinct_courses\
                        GROUP BY\
                            grade_student_epita_email_ref\
                        ) AS total_classes\
                    ON\
                        s.student_epita_email = total_classes.grade_student_epita_email_ref\
                    WHERE\
                        s.student_population_code_ref = 'CS' AND student_population_year_ref = '2021';")
                            
    students = cursor.fetchall()
    
    cursor2 = db.cursor()
    cursor2.execute("SELECT DISTINCT c.course_code, c.course_name, c.duration\
                    FROM students s\
                    JOIN grades g ON s.student_epita_email = g.grade_student_epita_email_ref\
                    JOIN courses c ON g.grade_course_code_ref = c.course_code\
                    WHERE s.student_population_code_ref = 'CS';")
    courses = cursor2.fetchall()
    return render_template("populations/msc-cs.html", students=students, courses=courses)


@app.route("/populations/dsa")
def populations_dsa():
    cursor = db.cursor()
    # cursor.execute("SELECT students.student_epita_email, contacts.contact_first_name, contacts.contact_last_name\
    #                FROM students\
    #                JOIN contacts ON students.student_contact_ref = contacts.contact_email\
    #                WHERE student_population_code_ref = 'AIs'")
    cursor.execute("SELECT\
                        s.student_epita_email AS email,\
                        c.contact_first_name AS first_name,\
                        c.contact_last_name AS last_name,\
                        CONCAT(\
                            COALESCE(passed_classes.passed_count, 0),\
                            '/',\
                            COALESCE(total_classes.total_count, 0)\
                        ) AS passed_classes_over_total\
                    FROM\
                        students s\
                    JOIN\
                        contacts c ON s.student_contact_ref = c.contact_email\
                    LEFT JOIN\
                        (SELECT\
                            grade_student_epita_email_ref,\
                            COUNT(*) AS passed_count\
                        FROM\
                            (SELECT\
                                grade_student_epita_email_ref,\
                                grade_course_code_ref,\
                                AVG(grade_score) AS avg_grade\
                            FROM\
                                grades\
                            GROUP BY\
                                grade_student_epita_email_ref, grade_course_code_ref\
                            ) AS avg_grades\
                        WHERE\
                            avg_grade >= 10\
                        GROUP BY\
                            grade_student_epita_email_ref\
                        ) AS passed_classes\
                    ON\
                        s.student_epita_email = passed_classes.grade_student_epita_email_ref\
                    LEFT JOIN\
                        (SELECT\
                            grade_student_epita_email_ref,\
                            COUNT(*) AS total_count\
                        FROM\
                            (SELECT\
                                grade_student_epita_email_ref,\
                                grade_course_code_ref\
                            FROM\
                                grades\
                            GROUP BY\
                                grade_student_epita_email_ref, grade_course_code_ref\
                            ) AS distinct_courses\
                        GROUP BY\
                            grade_student_epita_email_ref\
                        ) AS total_classes\
                    ON\
                        s.student_epita_email = total_classes.grade_student_epita_email_ref\
                    WHERE\
                        s.student_population_code_ref = 'DSA' AND student_population_year_ref = '2021';")
                            
    students = cursor.fetchall()
    
    cursor2 = db.cursor()
    cursor2.execute("SELECT DISTINCT c.course_code, c.course_name, c.duration\
                    FROM students s\
                    JOIN grades g ON s.student_epita_email = g.grade_student_epita_email_ref\
                    JOIN courses c ON g.grade_course_code_ref = c.course_code\
                    WHERE s.student_population_code_ref = 'DSA';")
    courses = cursor2.fetchall()
    return render_template("populations/msc-dsa.html", students=students, courses=courses)


@app.route("/populations/ism")
def populations_ism():
    cursor = db.cursor()
    # cursor.execute("SELECT students.student_epita_email, contacts.contact_first_name, contacts.contact_last_name\
    #                FROM students\
    #                JOIN contacts ON students.student_contact_ref = contacts.contact_email\
    #                WHERE student_population_code_ref = 'AIs'")
    cursor.execute("SELECT\
                        s.student_epita_email AS email,\
                        c.contact_first_name AS first_name,\
                        c.contact_last_name AS last_name,\
                        CONCAT(\
                            COALESCE(passed_classes.passed_count, 0),\
                            '/',\
                            COALESCE(total_classes.total_count, 0)\
                        ) AS passed_classes_over_total\
                    FROM\
                        students s\
                    JOIN\
                        contacts c ON s.student_contact_ref = c.contact_email\
                    LEFT JOIN\
                        (SELECT\
                            grade_student_epita_email_ref,\
                            COUNT(*) AS passed_count\
                        FROM\
                            (SELECT\
                                grade_student_epita_email_ref,\
                                grade_course_code_ref,\
                                AVG(grade_score) AS avg_grade\
                            FROM\
                                grades\
                            GROUP BY\
                                grade_student_epita_email_ref, grade_course_code_ref\
                            ) AS avg_grades\
                        WHERE\
                            avg_grade >= 10\
                        GROUP BY\
                            grade_student_epita_email_ref\
                        ) AS passed_classes\
                    ON\
                        s.student_epita_email = passed_classes.grade_student_epita_email_ref\
                    LEFT JOIN\
                        (SELECT\
                            grade_student_epita_email_ref,\
                            COUNT(*) AS total_count\
                        FROM\
                            (SELECT\
                                grade_student_epita_email_ref,\
                                grade_course_code_ref\
                            FROM\
                                grades\
                            GROUP BY\
                                grade_student_epita_email_ref, grade_course_code_ref\
                            ) AS distinct_courses\
                        GROUP BY\
                            grade_student_epita_email_ref\
                        ) AS total_classes\
                    ON\
                        s.student_epita_email = total_classes.grade_student_epita_email_ref\
                    WHERE\
                        s.student_population_code_ref = 'ISM' AND student_population_year_ref = '2021';")
                            
    students = cursor.fetchall()
    
    cursor2 = db.cursor()
    cursor2.execute("SELECT DISTINCT c.course_code, c.course_name, c.duration\
                    FROM students s\
                    JOIN grades g ON s.student_epita_email = g.grade_student_epita_email_ref\
                    JOIN courses c ON g.grade_course_code_ref = c.course_code\
                    WHERE s.student_population_code_ref = 'ISM';")
    courses = cursor2.fetchall()
    return render_template("populations/msc-ism.html", students=students, courses=courses)


@app.route("/populations/se")
def populations_se():
    cursor = db.cursor()
    # cursor.execute("SELECT students.student_epita_email, contacts.contact_first_name, contacts.contact_last_name\
    #                FROM students\
    #                JOIN contacts ON students.student_contact_ref = contacts.contact_email\
    #                WHERE student_population_code_ref = 'AIs'")
    cursor.execute("SELECT\
                        s.student_epita_email AS email,\
                        c.contact_first_name AS first_name,\
                        c.contact_last_name AS last_name,\
                        CONCAT(\
                            COALESCE(passed_classes.passed_count, 0),\
                            '/',\
                            COALESCE(total_classes.total_count, 0)\
                        ) AS passed_classes_over_total\
                    FROM\
                        students s\
                    JOIN\
                        contacts c ON s.student_contact_ref = c.contact_email\
                    LEFT JOIN\
                        (SELECT\
                            grade_student_epita_email_ref,\
                            COUNT(*) AS passed_count\
                        FROM\
                            (SELECT\
                                grade_student_epita_email_ref,\
                                grade_course_code_ref,\
                                AVG(grade_score) AS avg_grade\
                            FROM\
                                grades\
                            GROUP BY\
                                grade_student_epita_email_ref, grade_course_code_ref\
                            ) AS avg_grades\
                        WHERE\
                            avg_grade >= 10\
                        GROUP BY\
                            grade_student_epita_email_ref\
                        ) AS passed_classes\
                    ON\
                        s.student_epita_email = passed_classes.grade_student_epita_email_ref\
                    LEFT JOIN\
                        (SELECT\
                            grade_student_epita_email_ref,\
                            COUNT(*) AS total_count\
                        FROM\
                            (SELECT\
                                grade_student_epita_email_ref,\
                                grade_course_code_ref\
                            FROM\
                                grades\
                            GROUP BY\
                                grade_student_epita_email_ref, grade_course_code_ref\
                            ) AS distinct_courses\
                        GROUP BY\
                            grade_student_epita_email_ref\
                        ) AS total_classes\
                    ON\
                        s.student_epita_email = total_classes.grade_student_epita_email_ref\
                    WHERE\
                        s.student_population_code_ref = 'SE' AND student_population_year_ref = '2021';")
                            
    students = cursor.fetchall()
    
    cursor2 = db.cursor()
    cursor2.execute("SELECT DISTINCT c.course_code, c.course_name, c.duration\
                    FROM students s\
                    JOIN grades g ON s.student_epita_email = g.grade_student_epita_email_ref\
                    JOIN courses c ON g.grade_course_code_ref = c.course_code\
                    WHERE s.student_population_code_ref = 'SE';")
    courses = cursor2.fetchall()
    return render_template("populations/msc-se.html", students=students, courses=courses)


# --------------- AIS Grades ----------------
@app.route("/ais_grades/ai_data_prep")
def ais_grades_ai_data_prep():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'AI_DATA_PREP'\
                    AND s.student_population_code_ref = 'AIs'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/ais_grades/ai_data_prep.html", grades=grades)


@app.route("/ais_grades/ai_data_science_in_prod")
def ais_grades_ai_data_science_in_prod():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'AI_DATA_SCIENCE_IN_PROD'\
                    AND s.student_population_code_ref = 'AIs'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/ais_grades/ai_data_science_in_prod.html", grades=grades)

@app.route("/ais_grades/pg_python")
def ais_grades_pg_python():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'PG_PYTHON'\
                    AND s.student_population_code_ref = 'AIs'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/ais_grades/pg_python.html", grades=grades)

@app.route("/ais_grades/dt_rdbms")
def ais_grades_dt_rdbms():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'DT_RDBMS'\
                    AND s.student_population_code_ref = 'AIs'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/ais_grades/dt_rdbms.html", grades=grades)


# --------------- Cyber Security Grades ----------------
@app.route("/cs_grades/cs_data_priv")
def cs_grades_cs_data_priv():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'CS_DATA_PRIV'\
                    AND s.student_population_code_ref = 'CS'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/cs_grades/cs_data_priv.html", grades=grades)

@app.route("/cs_grades/cs_software_security")
def cs_grades_cs_software_security():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'CS_SOFTWARE_SECURITY'\
                    AND s.student_population_code_ref = 'CS'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/cs_grades/cs_software_security.html", grades=grades)

@app.route("/cs_grades/pg_python")
def cs_grades_pg_python():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'PG_PYTHON'\
                    AND s.student_population_code_ref = 'CS'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/cs_grades/pg_python.html", grades=grades)

@app.route("/cs_grades/dt_rdbms")
def cs_grades_dt_rdbms():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'DT_RDBMS'\
                    AND s.student_population_code_ref = 'CS'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/cs_grades/dt_rdbms.html", grades=grades)


# --------------- DSA Grades ----------------
@app.route("/dsa_grades/ai_data_science_in_prod")
def dsa_grades_ai_data_science_in_prod():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'AI_DATA_SCIENCE_IN_PROD'\
                    AND s.student_population_code_ref = 'DSA'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/dsa_grades/ai_data_science_in_prod.html", grades=grades)

@app.route("/dsa_grades/pg_python")
def dsa_grades_pg_python():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'PG_PYTHON'\
                    AND s.student_population_code_ref = 'DSA'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/dsa_grades/pg_python.html", grades=grades)

@app.route("/dsa_grades/dt_rdbms")
def dsa_grades_dt_rdbms():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'DT_RDBMS'\
                    AND s.student_population_code_ref = 'DSA'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/dsa_grades/dt_rdbms.html", grades=grades)


# --------------- ISM Grades ----------------
@app.route("/ism_grades/mk_com_for_leaders")
def ism_grades_mk_com_for_leaders():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'MK_COM_FOR_LEADER'\
                    AND s.student_population_code_ref = 'ISM'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/ism_grades/mk_com_for_leaders.html", grades=grades)

@app.route("/ism_grades/pg_python")
def ism_grades_pg_python():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'PG_PYTHON'\
                    AND s.student_population_code_ref = 'ISM'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/ism_grades/pg_python.html", grades=grades)

@app.route("/ism_grades/pm_agile")
def ism_grades_pm_agile():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'PM_AGILE'\
                    AND s.student_population_code_ref = 'ISM'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/ism_grades/pm_agile.html", grades=grades)

@app.route("/ism_grades/dt_rdbms")
def ism_grades_dt_rdbms():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'DT_RDBMS'\
                    AND s.student_population_code_ref = 'ISM'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/ism_grades/dt_rdbms.html", grades=grades)

# --------------- SE Grades ----------------
@app.route("/se_grades/pg_python")
def se_grades_pg_python():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'PG_PYTHON'\
                    AND s.student_population_code_ref = 'SE'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/se_grades/pg_python.html", grades=grades)

@app.route("/se_grades/se_adv_db")
def se_grades_se_adv_db():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'SE_ADV_DB'\
                    AND s.student_population_code_ref = 'SE'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/se_grades/se_adv_db.html", grades=grades)

@app.route("/se_grades/se_adv_java")
def se_grades_se_adv_java():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'SE_ADV_JAVA'\
                    AND s.student_population_code_ref = 'SE'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/se_grades/se_adv_java.html", grades=grades)

@app.route("/se_grades/dt_rdbms")
def se_grades_dt_rdbms():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'DT_RDBMS'\
                    AND s.student_population_code_ref = 'SE'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/se_grades/dt_rdbms.html", grades=grades)

@app.route("/se_grades/se_adv_js")
def se_grades_se_adv_js():
    cursor = db.cursor()
    cursor.execute("SELECT\
                        g.grade_student_epita_email_ref,\
                        c.contact_first_name,\
                        c.contact_last_name,\
                        g.grade_exam_type_ref, \
                        g.grade_score\
                    FROM grades g\
                    JOIN students s ON g.grade_student_epita_email_ref = s.student_epita_email\
                    JOIN contacts c ON s.student_contact_ref = c.contact_email\
                    WHERE g.grade_course_code_ref = 'SE_ADV_JS'\
                    AND s.student_population_code_ref = 'SE'\
                    AND s.student_population_year_ref = 2021;")
    grades = cursor.fetchall()
    return render_template("grades/se_grades/se_adv_js.html", grades=grades)


#     _  _____ _____ _____ _   _ ____    _    _   _  ____ _____ 
#    / \|_   _|_   _| ____| \ | |  _ \  / \  | \ | |/ ___| ____|
#   / _ \ | |   | | |  _| |  \| | | | |/ _ \ |  \| | |   |  _|  
#  / ___ \| |   | | | |___| |\  | |_| / ___ \| |\  | |___| |___ 
# /_/   \_\_|   |_| |_____|_| \_|____/_/   \_\_| \_|\____|_____|
                                                              
#   ____ ____      _    ____  _   _ 
#  / ___|  _ \    / \  |  _ \| | | |
# | |  _| |_) |  / _ \ | |_) | |_| |
# | |_| |  _ <  / ___ \|  __/|  _  |
#  \____|_| \_\/_/   \_\_|   |_| |_|

def pie_chart():
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="db")
    # Fetch data from MySQL database
    cursor = db.cursor()
    query = """
    SELECT student_population_code_ref, COUNT(*) AS num_students
    FROM students s 
    WHERE student_population_year_ref = 2021
    GROUP BY student_population_code_ref;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db.close()

    # Extract labels and number of students for the pie chart
    labels = [row[0] for row in data]
    num_students = [row[1] for row in data]

    # Define custom colors
    colors = ['#007AFF', '#34C759', '#FF6482', '#FF9500', '#5856D6']

    # Define the explode values to create white space
    explode = (0.01, 0.01, 0.01, 0.01, 0.01)

    # Create the pie chart with customizations
    plt.figure(figsize=(8, 6))
    plt.pie(num_students, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, explode=explode, textprops={'fontname': 'monospace'})

    # Add title with monospaced font
    plt.title('Student Population Distribution', fontname='monospace', fontsize=14)


    plt.tight_layout()
    plt.savefig('app/static/pie_chart.png', dpi=300)  # Save the bar chart as a PNG file
    plt.close()  # Close the plot to free up memory
    

def bar_chart():
    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="db")
    # Fetch data from MySQL database
    cursor = db.cursor()
    query = """
    SELECT
        s.student_population_code_ref,
        COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) AS total_presences,
        COUNT(*) AS total_records,
        (COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) * 100.0 / COUNT(*)) AS presence_percentage
    FROM
        students s
    LEFT JOIN
        attendance a ON s.student_epita_email = a.attendance_student_ref
    WHERE
        a.attendance_population_year_ref = 2021
    GROUP BY
        s.student_population_code_ref;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    db.close()

    # Extract labels and presence_percentage for the bar chart
    labels = [row[0] for row in data]
    presence_percentage = [row[3] for row in data]

    # Define custom colors
    colors = ['#007AFF', '#34C759', '#FF9500', '#FF6482', '#5856D6']

    # Create the bar chart with customizations
    plt.figure(figsize=(8, 6))  # Reduced figure size
    bars = plt.bar(labels, presence_percentage, color=colors, width=0.4, zorder=3)  # Reduced width and space between bars

    # Customize axis settings
    plt.xlabel('Student Population', fontname='monospace', fontsize=12)
    plt.ylabel('Presence Percentage', fontname='monospace', fontsize=12)
    plt.title('Presence Percentage by Student Population', fontname='monospace', fontsize=14)
    plt.xticks(rotation=0, fontname='monospace', fontsize=10, horizontalalignment='center')
    plt.yticks(fontname='monospace', fontsize=10)
    plt.gca().spines['top'].set_visible(False)  # Remove top border
    plt.gca().spines['right'].set_visible(False)  # Remove right border
    plt.gca().spines['left'].set_linewidth(0.5)  # Set left border linewidth to 0.5

    # Add labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), va='bottom', ha='center', fontname='monospace', fontsize=10)

    plt.tight_layout()
    plt.savefig('app/static/bar_chart.png', dpi=300)  # Save the bar chart as a PNG file
    plt.close()  # Close the plot to free up memory


if __name__ == "__main__":
    pie_chart()
    bar_chart()
    app.run(debug=True)
