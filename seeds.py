from connect import engine, Base, session
from models import Group, Student, Teacher, Subject, Grade
from faker import Faker
from random import randint, choice

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
