from flask.views import MethodView
from flask_smorest import Blueprint

from app.extensions import db
from app.models import Project, Task
from app.resources.common import get_or_404
from app.schemas import TaskQueryArgsSchema, TaskSchema, TaskUpdateSchema

blp = Blueprint("tasks", __name__, url_prefix="/tasks", description="Operations on tasks")


@blp.route("/")
class TaskList(MethodView):
    @blp.arguments(TaskQueryArgsSchema, location="query")
    @blp.response(200, TaskSchema(many=True))
    def get(self, args):
        query = db.session.query(Task)
        if args["project_id"] is not None:
            query = query.filter(Task.project_id == args["project_id"])
        if args["status"] is not None:
            query = query.filter(Task.status == args["status"])
        return query.order_by(Task.created_at).all()

    @blp.arguments(TaskSchema)
    @blp.response(201, TaskSchema)
    def post(self, new_data):
        get_or_404(Project, new_data["project_id"], "Project not found")
        task = Task(**new_data)
        db.session.add(task)
        db.session.commit()
        return task


@blp.route("/<uuid:task_id>")
class TaskItem(MethodView):
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        return get_or_404(Task, task_id, "Task not found")

    @blp.arguments(TaskUpdateSchema)
    @blp.response(200, TaskSchema)
    def patch(self, update_data, task_id):
        task = get_or_404(Task, task_id, "Task not found")
        for key, value in update_data.items():
            setattr(task, key, value)
        db.session.commit()
        return task

    @blp.response(204)
    def delete(self, task_id):
        task = get_or_404(Task, task_id, "Task not found")
        db.session.delete(task)
        db.session.commit()
