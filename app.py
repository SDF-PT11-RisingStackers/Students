from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Student 

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

migrate=Migrate(app,db)

@app.route('/')
def home():
	return "Welcome to the Student App"

if __name__=='__main__':
	app.run(debug=True)