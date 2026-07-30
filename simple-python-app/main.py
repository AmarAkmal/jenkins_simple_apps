from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Simple Task API")


class Task(BaseModel):
    title: str
    completed: bool = False


tasks: dict[int, Task] = {}
next_id = 1


@app.get("/")
def root():
    return {"message": "Task API is running"}


@app.get("/tasks")
def list_tasks():
    return [{"id": id, **t.model_dump()} for id, t in tasks.items()]


@app.post("/tasks", status_code=201)
def create_task(task: Task):
    global next_id
    task_id = next_id
    next_id += 1
    tasks[task_id] = task
    return {"id": task_id, **task.model_dump()}


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task_id, **tasks[task_id].model_dump()}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = task
    return {"id": task_id, **task.model_dump()}


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
