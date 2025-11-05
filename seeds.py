from models import db,Student,Course 
from faker import Faker 

fake=Faker()

def seed_fake_students(n=30):
	for  _ in range(n):
		student = Student(
			name=fake.name(),
			age=fake.random_int(min=18,max=40),
			email=fake.unique.email(),
			gender=fake.random_element(elements=("M","F"))
		)
		db.session.add(student)
def seed_fake_courses(n=10):
	for _ in range(n):
		course=Course(
			title=fake.catch_phrase(),
			description=fake.paragraph(),
			instructor=fake.name(),
			credits=fake.random_int(min=2,max=6)
		)
		db.session.add(course)

def seed_students():
	students=[
		{"name":"Melvin","age":"24","email":"melvin@example.com", "gender":"M"},
		{"name":"John","age":"24","email":"john@example.com", "gender":"M"},
		{"name":"Alice","age":"22","email":"alice@example.com", "gender":"F"},
		{"name":"Mary","age":"23","email":"mary@example.com", "gender":"F"},
	]
	for s in students:
		student=Student(
			name=s["name"],
			age=s["age"],
			email=s["email"],
			gender=s["gender"]
		)
		db.session.add(student)

def seed_courses():
	courses=[
		{"title":"Intro to Python",
   		"description":"Learn the basics of Python",
		"instructor":"Grace",
		"credits":3
		},
		{"title":"Databases 101",
   		"description":"Understand relational databases and SQL Concepts",
		"instructor":"Daniel",
		"credits":4
		},
		{"title":"Web Development with Flask",
   		"description":"Build modern web applications using Flask",
		"instructor":"Nancy",
		"credits":5
		}
	]
	for c in courses:
		course=Course(
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

		seed_fake_students(30)
		seed_fake_courses(10)


		db.session.commit()
		print("All the seeds applied sucessfully")
	except Exception as e:
		db.session.rollback()
		print('Seeding failed:',e)
		