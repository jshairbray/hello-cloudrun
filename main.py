import os
from flask import Flask, request
from google.cloud import storage

app = Flask(__name__)

BUCKET_NAME = "hello-cloudrun-data-504019"import os
import datetime
from flask import Flask, request
from google.cloud import storage
from google.cloud import bigquery

app = Flask(__name__)

BUCKET_NAME = "hello-cloudrun-data-504019"
BQ_DATASET = "hello_cloudrun_data"
BQ_TABLE = "notes"
BQ_PROJECT = "my-generic-project-504019"

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

@app.route("/log")
def log():
    message = request.args.get("message", "default log message")
    client = bigquery.Client()
    table_id = f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}"
    rows = [{"message": message, "created_at": datetime.datetime.utcnow().isoformat()}]
    errors = client.insert_rows_json(table_id, rows)
    if errors:
        return f"Errors inserting row: {errors}", 500
    return f"Logged: {message}"

@app.route("/logs")
def logs():
    client = bigquery.Client()
    query = f"SELECT message, created_at FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}` ORDER BY created_at DESC LIMIT 10"
    results = client.query(query).result()
    rows = [f"{row.created_at}: {row.message}" for row in results]
    return "\n".join(rows) if rows else "No logs yet."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))