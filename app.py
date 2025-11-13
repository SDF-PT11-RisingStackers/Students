from flask import Flask, make_response,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Student,Course

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

migrate=Migrate(app,db)

# @app.route('/')
# def home():
# 	students=Student.query.all()
# 	response_body='<h1>Students Names</h1>'
# 	for s in students:
# 		response_body+=f'<p>{s.name}</p>'#response_body=response_body+f'<p>{s.name}</p> x+=1=>x=x+1
# 	response=make_response(response_body,200)
# 	return response

# @app.route('/students/<int:id>')	
# def student_by_id(id):
# 	student=Student.query.get(id)
# 	if student:
# 		response_body=f'<p>{student.name}</p>'
# 		status=200
# 	else:
# 		response_body=f'<p>Student {id} not found</p>'
# 		status=404
# 	response=make_response(response_body,status)
# 	return response
# @app.route('/')
# def home():
# 	students=Student.query.all()
# 	students_data= [s.to_dict() for s in students ]
# 	return jsonify (students_data),200

# @app.route('/students/<int:id>')
# def student_json(id):
# 	student=Student.query.get(id)
# 	if not student:
# 		return jsonify({"error":f"Student {id} not found"}),404
# 	return jsonify(student.to_dict()),200

# @app.route('/courses')
# def get_courses():
# 	courses=Course.query.all()
# 	courses_data=[c.to_dict() for c in courses]
# 	return jsonify(courses_data),200

# @app.route('/courses/<int:id>')
# def get_course(id):
# 	course= Course.query.get(id)
# 	if not course:
# 		return jsonify({"error":f"Course {id} not found"}),404
# 	return jsonify(course.to_dict()),200

@app.route('/students', methods=['POST'])
def create_students():
	data=request.get_json() #read the JSON body from the request
	if not data:
		return jsonify({"error":"Bad Request"}),400
	name=data.get("name")
	email=data.get("email")
	if not name or not email:
		return jsonify({"error":"Missing required fields:name and email"}),400
	if Student.query.filter_by(email=email).first():
		return jsonify({"error":"A student with that email already exists"}),400
	student= Student(
		name=name,
		email=email,
		age=data.get("age"),
		gender=data.get("gender")
	)
	db.session.add(student)
	db.session.commit()

	return jsonify(student.to_dict()),201

@app.route('/students',methods=['GET'])
def get_students():
	students=Student.query.all()
	students_data=[s.to_dict()for s in students]
	return jsonify(students_data),200

@app.route('/students/<int:id>',methods=['GET'])
def get_student(id):
	student=Student.query.get(id)
	if not student:
		return jsonify({"error":f"student {id} not found"}),404 
	return jsonify(student.to_dict()),200

@app.route('/courses', methods=['GET'])
def get_courses():
	courses=Course.query.all()
	courses_data=[c.to_dict()for c in courses]
	return jsonify(courses_data),200

@app.route('/courses/<int:id>', methods=['GET'])
def get_course(id):
	course=Course.query.get(id)
	if not course:
		return jsonify({"error":f"Course {id} not found"}),404
	return jsonify(course.to_dict()),200

@app.route('/students/<int:id>', methods=['PATCH'])
def update_student(id):
	student=Student.query.get(id)
	if not student:
		return jsonify({"error":f"student {id} not found"})
	data=request.get_json()
	if not data:
		return jsonify({"error":"Request must be JSON"}),400
	
	# if email is changing ensure uniqueness
	new_email=data.get("email")
	if new_email and new_email !=student.email:
		existing=Student.query.filter_by(email=new_email).first()
		if existing:
			return jsonify({"error":"A student with that email already exists"}),400
		
	#apply updates for fields that were provided 
	if "name" in data:
		student.name=data.get("name")
	if "email" in data:
		student.email=data.get("email")
	if "age" in data:
		student.age=data.get("age")
	if "gender" in data:
		student.gender=data.get("gender")

	db.session.commit()
	return jsonify(student.to_dict()),200

@app.route('/courses/<int:id>', methods=['PATCH'])
def update_course(id):
	course=Course.query.get(id)
	if not course:
		return jsonify({"error":f"Course {id} not found"}),404
	
	data=request.get_json()
	if not data:
		return jsonify({"error":"Request must be JSON"}),400
	new_title=data.get("title")
	if new_title and new_title!=course.title:
		existing=Course.query.filter_by(title=new_title).first()
		if existing:
			return jsonify({"error":"A course with that title already exists"}),400
	
	if "title" in data:
		course.title=data.get("title")
	if "description" in data:
		course.description=data.get("description")
	if "instructor" in data:
		course.instructor=data.get("instructor")
	if "credits" in data:
		course.credits=data.get("credits")
	db.session.commit()
	return jsonify(course.to_dict()),200

@app.cli.command("seed")
def seed():
	from seeds import run_seeds
	with app.app_context():
		run_seeds()


if __name__=='__main__':
	app.run(debug=True)