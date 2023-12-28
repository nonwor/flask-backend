from flask import Flask
import sys

app = Flask(__name__)

@app.route("/")
def hello_world():
	print('Hello world!', file=sys.stderr)
	return "Hello World"