from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, select, and_
import pandas as pd
import io
import sys
import psutil

from usermodel import users

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

#This .db file could be in "instance" folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)

# class users(db.Model):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     username: Mapped[str] = mapped_column(String, nullable=False)
#     email: Mapped[str] = mapped_column(String, nullable=False)

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
@app.route("/users/table", methods=["GET"])
def getUsersAsCsv():
	print("Getting users as csv", file=sys.stderr)
	try:
		all_users = db.session.execute(db.select(users)).scalars()
		data = []
		for user in all_users:
			data.append([user.id, user.username, user.email])
		print(data, file=sys.stderr)
		df = pd.DataFrame(data,columns=['id',"username","email"])

		csv_data = io.StringIO()
		df.to_csv(csv_data, index=False)
		response = app.response_class(
			response = csv_data.getvalue(),
			status=200,
		)

		print("ok", file=sys.stderr)

		return(response)
	except:

		return("call failed", 400)

#Create new user, or if a user exists we return some message and data
@app.route("/user", methods=["POST", "GET"])
def showRouteInput():

	# Handle API input process data according to specs
	# This is to create new users
	data = request.get_json()
	if request.method == "POST":
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

	#We try to get the user ID here
	if request.method == "GET":

		#We can use query and filter to capture "lookup" data in DB.
		print("doing GET user here", file=sys.stderr)
		# user = users.query.filter((users.email == data["email"]) and (users.username == data["name"])).first()
		query = select(users).where(and_(users.username == data["name"], users.email == data["email"]))
		result = db.session.execute(query).scalars().first()
		print(result,file=sys.stderr)

		if(result == None):
			return("Cannot find user", 200)
		else:
			print(result.id, result.username, result.email, file=sys.stderr)
			return({"id":result.id, "username": result.username, "email":result.email}, 200)

@app.route("/util")
def checkCpuMemUsage():
	print("Checking Utilization", file=sys.stderr)
	cpuUtil = psutil.cpu_percent()
	memUtil = psutil.virtual_memory().percent
	return({"CPU": cpuUtil,
		 "MEM": memUtil})
