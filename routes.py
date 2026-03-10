from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session

from models import SessionLocal, TaskModel, SubtaskModel
from ai_service import parse_natural_language, generate_subtasks

router = APIRouter()

# Dependency to provide a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------
class TaskCreateRequest(BaseModel):
    natural_language_text: str = Field(..., min_length=10, max_length=500)

class TaskResponse(BaseModel):
    task_id: str
    title: str
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    category: Optional[str] = None

    class Config:
        orm_mode = True

class SubtaskItem(BaseModel):
    id: str
    title: str
    completed: bool

    class Config:
        orm_mode = True

class SubtaskGenerateResponse(BaseModel):
    subtasks: List[SubtaskItem]

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@router.post("/api/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(request: TaskCreateRequest, db: Session = Depends(get_db)):
    # Call AI to parse the natural language description
    ai_result = await parse_natural_language(request.natural_language_text)

    if "note" in ai_result:
        # Fallback – use the raw text as the title
        title = request.natural_language_text
        due_date = None
        priority = None
        category = None
    else:
        title = ai_result.get("title", request.natural_language_text)
        due_date = ai_result.get("due_date")
        priority = ai_result.get("priority")
        category = ai_result.get("category")
        # Convert ISO string to datetime if present
        if isinstance(due_date, str):
            try:
                due_date = datetime.fromisoformat(due_date)
            except Exception:
                due_date = None

    task = TaskModel(
        title=title,
        description=request.natural_language_text,
        due_date=due_date,
        priority=priority,
        category=category,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return TaskResponse(
        task_id=task.id,
        title=task.title,
        due_date=task.due_date,
        priority=task.priority,
        category=task.category,
    )

@router.post("/api/tasks/{task_id}/subtasks", response_model=SubtaskGenerateResponse)
async def create_subtasks(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    ai_result = await generate_subtasks(task.title)
    if "note" in ai_result:
        # Fallback – no subtasks generated
        return SubtaskGenerateResponse(subtasks=[])

    # Expecting a list of strings under key "subtasks"
    subtask_titles = ai_result.get("subtasks", [])
    created_items = []
    for title in subtask_titles:
        sub = SubtaskModel(task_id=task.id, title=title)
        db.add(sub)
        created_items.append(sub)
    db.commit()
    # Refresh to obtain IDs
    for sub in created_items:
        db.refresh(sub)
    return SubtaskGenerateResponse(
        subtasks=[SubtaskItem(id=sub.id, title=sub.title, completed=sub.completed) for sub in created_items]
    )

@router.get("/api/tasks", response_model=List[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).all()
    return [
        TaskResponse(
            task_id=t.id,
            title=t.title,
            due_date=t.due_date,
            priority=t.priority,
            category=t.category,
        )
        for t in tasks
    ]

@router.get("/api/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(
        task_id=task.id,
        title=task.title,
        due_date=task.due_date,
        priority=task.priority,
        category=task.category,
    )
