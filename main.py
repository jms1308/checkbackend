import os

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
  """Example Hello World route."""
  name = os.environ.get("NAME", "World1")
  return f"Hello {name}!"

@app.route("/student")
def get_student_name():
  """Gets a student's name from query params, adds quotes, and returns it."""
  student_name = request.args.get('name')
  if student_name:  
    return f'"{student_name} Hello and what"' 
  return "No student name provided."

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))