from flask.views import MethodView
from flask_smorest import Blueprint

from app.extensions import db
from app.models import Task, TaskComment
from app.resources.common import get_or_404
from app.schemas import TaskCommentCreateSchema, TaskCommentSchema

blp = Blueprint("task_comments", __name__, description="Operations on task comments")


@blp.route("/tasks/<uuid:task_id>/comments")
class TaskCommentList(MethodView):
    @blp.response(200, TaskCommentSchema(many=True))
    def get(self, task_id):
        get_or_404(Task, task_id, "Task not found")
        return (
            db.session.query(TaskComment)
            .filter(TaskComment.task_id == task_id)
            .order_by(TaskComment.created_at)
            .all()
        )

    @blp.arguments(TaskCommentCreateSchema)
    @blp.response(201, TaskCommentSchema)
    def post(self, new_data, task_id):
        get_or_404(Task, task_id, "Task not found")
        comment = TaskComment(task_id=task_id, **new_data)
        db.session.add(comment)
        db.session.commit()
        return comment


@blp.route("/task_comments/<uuid:comment_id>")
class TaskCommentItem(MethodView):
    @blp.response(204)
    def delete(self, comment_id):
        comment = get_or_404(TaskComment, comment_id, "Comment not found")
        db.session.delete(comment)
        db.session.commit()
