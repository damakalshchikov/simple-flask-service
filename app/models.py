from sqlalchemy import Enum, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.extensions import Base, db

task_status = Enum("todo", "in_progress", "done", name="task_status", create_type=False)
task_priority = Enum("low", "medium", "high", name="task_priority", create_type=False)


class Project(Base):
    __tablename__ = "projects"

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=text("now()"))

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    project_id = db.Column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(task_status, nullable=False, server_default="todo")
    priority = db.Column(task_priority, nullable=False, server_default="medium")
    assignee = db.Column(db.String(255))
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime(timezone=True), server_default=text("now()"))
    updated_at = db.Column(db.DateTime(timezone=True), server_default=text("now()"))

    project = relationship("Project", back_populates="tasks")
    comments = relationship("TaskComment", back_populates="task", cascade="all, delete-orphan")


class TaskComment(Base):
    __tablename__ = "task_comments"

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    task_id = db.Column(
        UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )
    author = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=text("now()"))

    task = relationship("Task", back_populates="comments")
