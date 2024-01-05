from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, select

import sys

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

#This .db file could be in "instance" folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)

class users(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)

with app.app_context():
    db.create_all()

#Get users as json
@app.route("/users", methods=["GET"])
def hello_world():
	print('Hello world!', file=sys.stderr)
	#We can do a get all user request here
	#We don't really need to check for GET, since it is handled by Flask
	if request.method == "GET":
		all_users = db.session.execute(db.select(users).order_by(users.username)).scalars()
		json = {}
		for user in all_users:
			json[user.id] = {"username":user.username, "email":user.email}
			print(user.email, file=sys.stderr)
		print(json, file=sys.stderr)
		return (json,200)

#Get users as a CSV

#Create new user, or if a user exists we return some message and data
@app.route("/user", methods=["POST"])
def showRouteInput():
	# Handle API input process data according to specs
	data = request.get_json()
	print(data, file=sys.stderr)
	user = users(
		username=data["name"],
		email=data["email"],
	)
	try:
		db.session.add(user)
		db.session.commit()
		return("success", 200)
	except:
		return("Failed to add user", 400)
	
	return("ok",200)

