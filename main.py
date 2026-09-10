import os
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Cloud Run and be kind! 🎉"

@app.route("/greet")
def greet():
    name = request.args.get("name", "friend")
    return f"Hey there, {name}! Welcome to your second Cloud Run route."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))