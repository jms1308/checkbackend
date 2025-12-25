import os

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    item = request.args.get('name')
    return f'Hello, {item}!'
    

@app.route('/expense')
def expense():
    item = request.args.get('item', 0, type=int)
    return str(item + 1)


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
