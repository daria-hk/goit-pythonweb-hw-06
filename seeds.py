from connect import engine, Base, session
from models import Group, Student, Teacher, Subject, Grade
from faker import Faker
from random import randint, choice
from my_select import select_1, select_2, select_3, select_4, select_5, select_6, select_7, select_8, select_9, \
        select_10

Base.metadata.create_all(engine)

fake = Faker()

def create_groups():
    groups = []
    for _ in range(3):
        group = Group(name=fake.word())
        groups.append(group)
    session.add_all(groups)
    session.commit()
    return groups

def create_teachers():
    teachers = []
    for _ in range(3):
        teacher = Teacher(first_name=fake.first_name(), last_name=fake.last_name())
        teachers.append(teacher)
    session.add_all(teachers)
    session.commit()
    return teachers

def create_subjects(teachers):
    subjects = []
    for _ in range(5):
        teacher = choice(teachers)
        subject = Subject(name=fake.word(), teacher_id=teacher.id)
        subjects.append(subject)
    session.add_all(subjects)
    session.commit()
    return subjects

def create_students(groups):
    students = []
    for _ in range(30):
        group = choice(groups)
        student = Student(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            group_id=group.id
        )
        students.append(student)
    session.add_all(students)
    session.commit()
    return students

def create_grades(students, subjects):
    for student in students:
        for subject in subjects:
            grade = Grade(
                student_id=student.id,
                subject_id=subject.id,
                grade=randint(1, 12),
                date=fake.date_time_this_year()
            )
            session.add(grade)
    session.commit()

def seed():

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

    print("Creating groups...")
    groups = create_groups()

    print("Creating teachers...")
    teachers = create_teachers()

    print("Creating subjects...")
    subjects = create_subjects(teachers)

    print("Creating students...")
    students = create_students(groups)

    print("Creating grades...")
    create_grades(students, subjects)

    print("Data successfully added!")

if __name__ == "__main__":
    seed()
    session.close()
