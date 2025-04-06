from sqlalchemy import func
from models import Student, Grade, Subject, Group, Teacher
from connect import engine, Base, session


# 1. Find the top 5 students with the highest average grade across all subjects
def select_1(session):
    return (
        session.query(Student, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade, Grade.student_id == Student.id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )

# 2. Find the student with the highest average grade in a specific subject
def select_2(session, subject_id):
    return (
        session.query(Student, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade, Grade.student_id == Student.id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )

# 3. Find the average grade in each group for a specific subject
def select_3(session, subject_id):
    return (
        session.query(Group.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )

# 4. Find the average grade across all students (overall average grade)
def select_4(session):
    return (
        session.query(func.avg(Grade.grade).label("avg_grade"))
        .all()
    )[0][0]

# 5. Find the courses taught by a specific teacher
def select_5(session, teacher_id):
    return (
        session.query(Subject.name)
        .filter(Subject.teacher_id == teacher_id)
        .all()
    )

# 6. Find the list of students in a specific group
def select_6(session, group_id):
    return (
        session.query(Student.first_name, Student.last_name)
        .filter(Student.group_id == group_id)
        .all()
    )

# 7. Find the grades of students in a specific group for a specific subject
def select_7(session, group_id, subject_id):
    # Combine first and last name into one column for student_name
    return session.query(
        func.concat(Student.first_name, " ", Student.last_name).label("student_name"),
        Grade.grade
    ).join(Grade).join(Subject).filter(
        Student.group_id == group_id,
        Subject.id == subject_id
    ).all()

# 8. Find the average grade given by a specific teacher across their subjects
def select_8(session, teacher_id):
    return (
        session.query(func.avg(Grade.grade).label("avg_grade"))
        .join(Subject, Subject.id == Grade.subject_id)
        .filter(Subject.teacher_id == teacher_id)
        .all()
    )[0][0]

# 9. Find the list of courses a specific student is taking
def select_9(session, student_id):
    return (
        session.query(Subject.name)
        .join(Grade, Grade.subject_id == Subject.id)
        .filter(Grade.student_id == student_id)
        .all()
    )

# 10. Find the list of courses a specific student is taking, taught by a specific teacher
def select_10(session, student_id, teacher_id):
    return (
        session.query(Subject.name)
        .join(Grade, Grade.subject_id == Subject.id)
        .filter(Grade.student_id == student_id)
        .filter(Subject.teacher_id == teacher_id)
        .all()
    )


if __name__ == "__main__":
    # 1. Find the top 5 students with the highest average grade across all subjects
    print("Top 5 students with the highest average grade:")
    top_students = select_1(session)
    for student, avg_grade in top_students:
        print(f"{student.first_name} {student.last_name}: {avg_grade}")
    print("\n")

    # 2. Find the student with the highest average grade in a specific subject
    subject_id = 1  # Example subject_id
    print(f"Student with the highest average grade in subject {subject_id}:")
    student_top_in_subject = select_2(session, subject_id)
    if student_top_in_subject:
        student, avg_grade = student_top_in_subject
        print(f"{student.first_name} {student.last_name}: {avg_grade}")
    else:
        print("No student found for this subject.")
    print("\n")

    # 3. Find the average grade in each group for a specific subject
    subject_id = 1  # Example subject_id
    print(f"Average grade in each group for subject {subject_id}:")
    avg_grades_in_groups = select_3(session, subject_id)
    for group_name, avg_grade in avg_grades_in_groups:
        print(f"Group {group_name}: {avg_grade}")
    print("\n")

    # 4. Find the average grade across all students
    print("Average grade across all students:")
    avg_grade_all_students = select_4(session)
    print(f"Overall average grade: {avg_grade_all_students}")
    print("\n")

    # 5. Find the courses taught by a specific teacher
    teacher_id = 1  # Example teacher_id
    print(f"Courses taught by teacher {teacher_id}:")
    courses_taught_by_teacher = select_5(session, teacher_id)
    for course in courses_taught_by_teacher:
        print(course.name)
    print("\n")

    # 6. Find the list of students in a specific group
    group_id = 1  # Example group_id
    print(f"Students in group {group_id}:")
    students_in_group = select_6(session, group_id)
    for student in students_in_group:
        print(f"{student.first_name} {student.last_name}")
    print("\n")

    # 7. Find the grades of students in a specific group for a specific subject
    group_id = 1  # Example group_id
    subject_id = 1  # Example subject_id
    print(f"Grades of students in group {group_id} for subject {subject_id}:")
    grades_in_group_for_subject = select_7(session, group_id, subject_id)
    for student_name, grade in grades_in_group_for_subject:
        print(f"{student_name}: {grade}")
    print("\n")

    # 8. Find the average grade given by a specific teacher across their subjects
    teacher_id = 1  # Example teacher_id
    print(f"Average grade given by teacher {teacher_id}:")
    avg_grade_by_teacher = select_8(session, teacher_id)
    print(f"Teacher's average grade: {avg_grade_by_teacher}")
    print("\n")

    # 9. Find the list of courses a specific student is taking
    student_id = 1  # Example student_id
    print(f"Courses taken by student {student_id}:")
    courses_taken_by_student = select_9(session, student_id)
    for course in courses_taken_by_student:
        print(course.name)
    print("\n")

    # 10. Find the list of courses a specific student is taking, taught by a specific teacher
    student_id = 1  # Example student_id
    teacher_id = 2  # Example teacher_id
    print(f"Courses taken by student {student_id} taught by teacher {teacher_id}:")
    courses_taken_by_student_teacher = select_10(session, student_id, teacher_id)
    for course in courses_taken_by_student_teacher:
        print(course.name)
    print("\n")
