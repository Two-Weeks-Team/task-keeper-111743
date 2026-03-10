from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routes import router

app = FastAPI()
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def root():
    html = """<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='UTF-8'>
<title>Task Keeper API</title>
<style>
  body{background:#111;color:#eee;font-family:Arial,sans-serif;padding:2rem}
  a{color:#4af}
  h1{color:#fff}
  pre{background:#222;padding:1rem;border-radius:4px}
</style>
</head>
<body>
<h1>Task Keeper API</h1>
<p>Privacy‑first task manager with AI‑powered task creation and subtask generation.</p>
<h2>Endpoints</h2>
<ul>
  <li>GET <code>/health</code> – health check</li>
  <li>POST <code>/api/tasks</code> – create task via natural language (AI)</li>
  <li>POST <code>/api/tasks/{task_id}/subtasks</code> – generate subtasks (AI)</li>
  <li>GET <code>/api/tasks</code> – list tasks</li>
  <li>GET <code>/api/tasks/{task_id}</code> – get task details</li>
</ul>
<h2>Tech Stack</h2>
<ul>
  <li>FastAPI 0.115.0</li>
  <li>PostgreSQL</li>
  <li>DigitalOcean Serverless Inference (openai-gpt-oss-120b)</li>
  <li>Python 3.12</li>
</ul>
<p><a href="/docs">OpenAPI Docs</a> | <a href="/redoc">ReDoc</a></p>
</body>
</html>"""
    return HTMLResponse(content=html)
