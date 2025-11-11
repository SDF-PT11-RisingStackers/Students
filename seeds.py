from models import db, Student, Course
from faker import Faker
import random

fake = Faker()

def seed_fake_students(n=100, assign_mode='random'):
    """
    Create `n` fake students and assign each to an existing course.
    assign_mode: 'random' or 'roundrobin'
    Note: This function adds to db.session but does NOT commit.
    """
    courses = Course.query.all()
    if not courses:
        raise RuntimeError("No courses found. Create courses before seeding students.")

    num_courses = len(courses)
    rr_index = 0

    for _ in range(n):
        try:
            email = fake.unique.email()
        except Exception:
            email = f"{fake.user_name()}.{random.randint(1000,9999)}@example.com"

        if Student.query.filter_by(email=email).first():
            continue

        if assign_mode == 'roundrobin':
            course_obj = courses[rr_index % num_courses]
            rr_index += 1
        else:
            course_obj = random.choice(courses)

        student = Student(
            name=fake.name(),
            age=fake.random_int(min=18, max=40),
            email=email,
            gender=fake.random_element(elements=("M","F")),
            course=course_obj
        )
        db.session.add(student)

    print(f"✅ seed_fake_students: prepared up to {n} fake students assigned to courses (not yet committed).")


def seed_fake_courses(n=10):
    for _ in range(n):
        course = Course(
            title=fake.catch_phrase(),
            description=fake.paragraph(),
            instructor=fake.name(),
            credits=fake.random_int(min=2, max=6)
        )
        db.session.add(course)


def seed_students():
    students = [
        {"name": "Melvin", "age": "24", "email": "melvin@example.com", "gender": "M"},
        {"name": "John", "age": "24", "email": "john@example.com", "gender": "M"},
        {"name": "Alice", "age": "22", "email": "alice@example.com", "gender": "F"},
        {"name": "Mary", "age": "23", "email": "mary@example.com", "gender": "F"},
    ]
    for s in students:
        student = Student(
            name=s["name"],
            age=s["age"],
            email=s["email"],
            gender=s["gender"]
        )
        db.session.add(student)


def seed_courses():
    courses = [
        {"title": "Intro to Python",
         "description": "Learn the basics of Python",
         "instructor": "Grace",
         "credits": 3
         },
        {"title": "Databases 101",
         "description": "Understand relational databases and SQL Concepts",
         "instructor": "Daniel",
         "credits": 4
         },
        {"title": "Web Development with Flask",
         "description": "Build modern web applications using Flask",
         "instructor": "Nancy",
         "credits": 5
         }
    ]
    for c in courses:
        course = Course(
            title=c["title"],
            description=c["description"],
            instructor=c["instructor"],
            credits=c["credits"]
        )
        db.session.add(course)


def run_seeds():
    try:
        seed_students()
        seed_courses()

        # ensure fake courses exist if you want them
        seed_fake_courses(10)

        # create fake students and assign them to courses
        seed_fake_students(30, assign_mode='random')

        db.session.commit()
        print("All the seeds applied successfully")
    except Exception as e:
        db.session.rollback()
        print('Seeding failed:', e)
