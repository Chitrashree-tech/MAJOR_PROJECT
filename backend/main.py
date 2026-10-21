from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import User, Project, Task
from .schemas import UserCreate, TaskCreate


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WorkFlow AI API",
    description="Backend API for personalized productivity optimization",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "WorkFlow AI API is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/users")
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    user = User(
        name=user_data.name,
        email=user_data.email,
        role=user_data.role,
        experience=user_data.experience
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }


@app.get("/users")
def get_users(
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "experience": user.experience
        }
        for user in users
    ]


@app.post("/tasks")
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    task = Task(
        name=task_data.name,
        description=task_data.description,
        priority=task_data.priority,
        task_type=task_data.task_type,
        estimated_hours=task_data.estimated_hours,
        deadline=task_data.deadline,
        github_issue=task_data.github_issue,
        project_id=task_data.project_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "id": task.id,
        "name": task.name,
        "priority": task.priority,
        "estimated_hours": task.estimated_hours,
        "status": task.status
    }


@app.get("/projects/{project_id}/tasks")
def get_project_tasks(
    project_id: int,
    db: Session = Depends(get_db)
):
    tasks = (
        db.query(Task)
        .filter(Task.project_id == project_id)
        .all()
    )

    return [
        {
            "id": task.id,
            "name": task.name,
            "priority": task.priority,
            "estimated_hours": task.estimated_hours,
            "deadline": task.deadline,
            "status": task.status
        }
        for task in tasks
    ]

from .services.github_service import (
    get_user_info,
    get_repositories,
    get_recent_commits,
    get_pull_requests
)


@app.get("/github/user")
def github_user(token: str):
    return get_user_info(token)


@app.get("/github/repositories")
def github_repositories(token: str):
    return get_repositories(token)


@app.get("/github/commits")
def github_commits(
    repository: str,
    token: str,
    limit: int = 20
):
    return get_recent_commits(
        repository,
        token,
        limit
    )


@app.get("/github/pull-requests")
def github_pull_requests(
    repository: str,
    token: str
):
    return get_pull_requests(
        repository,
        token
    )