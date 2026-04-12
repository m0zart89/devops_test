import redis

r = redis.Redis(host="redis", port=6379)

print("Worker started, waiting for tasks...", flush=True)

while True:
    task = r.brpop("tasks", timeout=5)
    if task:
        print("Worker received task")
        print("Processing task...")
        print("Task completed")
