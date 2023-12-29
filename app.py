from flask import Flask
import sys

app = Flask(__name__)

@app.route("/")
def hello_world():
	print('Hello world!', file=sys.stderr)
	return("Hello World")

@app.route("/user/<username>")
def showRouteInput(username):
	# Handle API input process data according to specs
	if username == " ":
		return "Bad request" , 400
	else:
		print("input:"+username, file=sys.stderr)
		return username , 200