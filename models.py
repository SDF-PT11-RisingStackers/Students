from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Student(db.Model):
	__tablename__="students"

	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(100))
	age=db.Column(db.Integer)
	email=db.Column(db.String(120),unique=True)
	gender=db.Column(db.String)

class Course (db.Model):
	__tablename__="courses"

	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(100), nullable=False)
	description=db.Column(db.Text)
	instructor=db.Column(db.String(100))
	credits=db.Column(db.Integer)