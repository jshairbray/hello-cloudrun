import os
from flask import Flask, request
from google.cloud import storage

app = Flask(__name__)

BUCKET_NAME = "hello-cloudrun-data-504019"

@app.route("/")
def hello():
    return "Hello from Cloud Run and be kind! 🎉"

@app.route("/greet")
def greet():
    name = request.args.get("name", "friend")
    return f"Hey there, {name}! Welcome to your second Cloud Run route."

@app.route("/save")
def save():
    message = request.args.get("message", "default message")
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob("notes/latest.txt")
    blob.upload_from_string(message)
    return f"Saved to gs://{BUCKET_NAME}/notes/latest.txt: {message}"

@app.route("/read")
def read():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob("notes/latest.txt")
    if not blob.exists():
        return "No file saved yet."
    return blob.download_as_text()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))