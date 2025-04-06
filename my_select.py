from sqlalchemy import func
from models import Student, Grade, Subject, Group, Teacher

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
