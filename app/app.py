from flask import Flask
import redis

app = Flask(__name__)

r = redis.Redis(host="redis", port=6379)

@app.route("/")
def home():
    return "App is running"

@app.route("/task")
def send_task():
    r.lpush("tasks", "task")
    return "Task queued"

app.run(host="0.0.0.0", port=5000)
