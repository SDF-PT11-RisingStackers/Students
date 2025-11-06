from flask import Flask, make_response,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Student 

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
	students_data=[{
		"id":student.id,
		"name":student.name,
		"email":student.email,
		"age":student.age,
		"gender":student.gender
	} for student in students
	]
	return jsonify (students_data),200

@app.route('/students/<int:id>')
def student_json(id):
	student=Student.query.get(id)
	if not student:
		return jsonify({"error":f"Student {id} not found"}),404
	student_data={
		"id":student.id,
		"name":student.name,
		"email":student.email,
		"age":student.age,
		"gender":student.gender
	}
	return jsonify(student_data),200


@app.cli.command("seed")
def seed():
	from seeds import run_seeds
	with app.app_context():
		run_seeds()

if __name__=='__main__':
	app.run(debug=True)