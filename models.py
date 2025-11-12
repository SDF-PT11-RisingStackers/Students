from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db=SQLAlchemy()

class Student(db.Model,SerializerMixin):
	__tablename__="students"

	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(100))
	age=db.Column(db.Integer)
	email=db.Column(db.String(120),unique=True)
	gender=db.Column(db.String)
	course_id=db.Column(db.Integer,db.ForeignKey('courses.id'))
	course=db.relationship('Course',back_populates='students')

	serialize_rules = ('-course.students',)
class Course (db.Model,SerializerMixin):
	__tablename__="courses"

	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(100), nullable=False)
	description=db.Column(db.Text)
	instructor=db.Column(db.String(100))
	credits=db.Column(db.Integer)
	students=db.relationship('Student',back_populates="course")

	serialize_rules = ('-students.course',)
	#.to_dict()-> return a dictionary
	#.to_json()->return a JSON string version of the same dictionary