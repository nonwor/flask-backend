from flask import Flask, render_template
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

@app.route("/")
def hello_world():
	print('Hello world!', file=sys.stderr)
	stmt = select(users)
	all_users = db.session.execute(db.select(users).order_by(users.username)).scalars()
	for user in all_users:
		print(user.email, file=sys.stderr)
	return ("ok")

@app.route("/user/<username>")
def showRouteInput(username):
	# Handle API input process data according to specs
	if username == " ":
		return "Bad request" , 400
	else:
		print("input:"+username, file=sys.stderr)
		
		return username , 200

