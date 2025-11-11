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
@app.route('/')
def home():
	students=Student.query.all()
	# students_data=[{
	# 	"id":student.id,
	# 	"name":student.name,
	# 	"email":student.email,
	# 	"age":student.age,
	# 	"gender":student.gendere
	# } for student in students
	# ]
	students_data= [s.to_dict() for s in students ]
	return jsonify (students_data),200

@app.route('/students/<int:id>')
def student_json(id):
	student=Student.query.get(id)
	if not student:
		return jsonify({"error":f"Student {id} not found"}),404
	# student_data={
	# 	"id":student.id,
	# 	"name":student.name,
	# 	"email":student.email,
	# 	"age":student.age,
	# 	"gender":student.gender
	# }
	return jsonify(student.to_dict()),200
@app.route('/courses')
def get_courses():
	courses=Course.query.all()
	courses_data=[c.to_dict() for c in courses]
	return jsonify(courses_data),200

@app.route('/courses/<int:id>')
def get_course(id):
	course= Course.query.get(id)
	if not course:
		return jsonify({"error":f"Course {id} not found"}),404
	return jsonify(course.to_dict()),200

@app.route('/students', methods=['POST'])
def create_students():
	data=request.get_json()
	if not data:
		return jsonify({"error":"Bad Request"}),400
	name=data.get("name")
	email=data.get("email")
	if not name or not email:
		return jsonify({"error":"Missing required fields:name and email"}),400
@app.route('/courses')
@app.cli.command("seed")
def seed():
	from seeds import run_seeds
	with app.app_context():
		run_seeds()

if __name__=='__main__':
	app.run(debug=True)