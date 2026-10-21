from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=True)
    experience = Column(String, nullable=True)

    projects = relationship(
        "Project",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    deadline = Column(String, nullable=True)
    progress = Column(Float, default=0)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="projects"
    )

    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan"
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    priority = Column(String, default="Medium")
    task_type = Column(String, nullable=True)

    estimated_hours = Column(Float, default=1.0)

    deadline = Column(String, nullable=True)

    status = Column(
        String,
        default="Pending"
    )

    github_issue = Column(
        String,
        nullable=True
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    project = relationship(
        "Project",
        back_populates="tasks"
    )


class DailyCheckIn(Base):
    __tablename__ = "daily_checkins"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    date = Column(
        String,
        nullable=False
    )

    sleep_hours = Column(
        Float,
        nullable=True
    )

    stress_level = Column(
        Float,
        nullable=True
    )

    energy_level = Column(
        Float,
        nullable=True
    )

    capacity_score = Column(
        Float,
        nullable=True
    )

    effective_hours = Column(
        Float,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class GitHubActivity(Base):
    __tablename__ = "github_activities"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    activity_type = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    repository = Column(
        String,
        nullable=True
    )

    github_id = Column(
        String,
        nullable=True
    )

    task_id = Column(
        Integer,
        ForeignKey("tasks.id"),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class DailyPlan(Base):
    __tablename__ = "daily_plans"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    date = Column(
        String,
        nullable=False
    )

    capacity_hours = Column(
        Float,
        nullable=True
    )

    total_planned_hours = Column(
        Float,
        nullable=True
    )

    status = Column(
        String,
        default="Generated"
    )


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    task_id = Column(
        Integer,
        ForeignKey("tasks.id"),
        nullable=True
    )

    rating = Column(
        Float,
        nullable=True
    )

    comment = Column(
        Text,
        nullable=True
    )

    actual_hours = Column(
        Float,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )