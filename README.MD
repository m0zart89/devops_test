# DevOps Engineer Technical Task

## What Was Required

- Create Dockerfiles for two services: **app** (Python Flask API) and **worker**
- Add a custom **entrypoint script** for the app container
- Create a **docker-compose.yml** that runs both services on the same network with worker starting before app
- Set up a **CI/CD pipeline** that builds the app Docker image and saves it as an artifact
- *(Bonus)* Mount worker logs to a host directory
- *(Bonus)* Add Redis as a message broker between app and worker

---

## What Was Implemented

### 1. Dockerfiles

**`app/Dockerfile`** — builds the app image:
- Base image: `python:3.11-slim`
- Installs dependencies from `requirements.txt`
- Copies and runs a custom entrypoint script

**`worker/Dockerfile`** — builds the worker image:
- Base image: `python:3.11-slim`
- Installs dependencies from `requirements.txt`
- Sets `PYTHONUNBUFFERED=1` for real-time log output
- Runs via a custom entrypoint script that pipes output to a log file

### 2. Custom Entrypoint (app)

**`app/entrypoint.sh`** prints startup messages and delegates initialization to `app/init.sh` before starting the application:

```
Starting App Container...
Running initialization script...
Application started
```

### 3. Docker Compose

**`docker-compose.yml`** defines three services on a shared `app-network`:
- **redis** — message broker
- **worker** — starts after redis, logs mounted to `./worker/logs`, restarts automatically (`unless-stopped`)
- **app** — starts after redis and worker, exposed on port `5000`, restarts automatically (`unless-stopped`)

### 4. CI/CD Pipeline

**`.github/workflows/ci.yml`** — GitHub Actions pipeline triggered on push to `main`:
1. Checks out the repository
2. Builds the Docker image for the app
3. Saves the image as `app-image.tar`
4. Uploads it as a pipeline artifact

### 5. Bonus: Worker Logging

Worker output is captured via `tee` in `worker/entrypoint.sh` and written to `/app/logs/worker.log`, which is mounted to `./worker/logs/` on the host. Logs persist across container restarts.

### 6. Bonus: Redis

Redis is used as a message broker between the app and worker:
- **app** pushes tasks to a Redis list (`lpush tasks`)
- **worker** blocks on the list waiting for tasks (`brpop tasks`)

---

## Project Structure

```
.
├── app/
│   ├── app.py              # Flask API
│   ├── Dockerfile
│   ├── entrypoint.sh       # Custom entrypoint
│   ├── init.sh             # Initialization script
│   └── requirements.txt
├── worker/
│   ├── worker.py           # Redis consumer
│   ├── Dockerfile
│   ├── entrypoint.sh       # Entrypoint with log piping
│   ├── logs/               # Worker logs (mounted from container)
│   └── requirements.txt
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions pipeline
└── docker-compose.yml
```

---

## How to Run

```bash
docker-compose up --build
```

---

## How to Verify

**1. Check the app is running:**
```bash
curl http://localhost:5000/
# → App is running
```

**2. Send a task through Redis to the worker:**
```bash
curl http://localhost:5000/task
# → Task queued
```

**3. Check worker logs:**
```bash
docker logs worker
# → Worker received task
# → Processing task...
# → Task completed
```

Or check the log file on the host:
```bash
cat worker/logs/worker.log
```

**4. Check CI pipeline:**

Go to: [https://github.com/m0zart89/devops_test/actions](https://github.com/m0zart89/devops_test/actions)

The pipeline runs on every push to `main` and produces `app-image.tar` as a downloadable artifact.
