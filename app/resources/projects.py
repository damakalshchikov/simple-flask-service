from flask.views import MethodView
from flask_smorest import Blueprint

from app.extensions import db
from app.models import Project
from app.resources.common import get_or_404
from app.schemas import ProjectSchema, ProjectUpdateSchema

blp = Blueprint("projects", __name__, url_prefix="/projects", description="Operations on projects")


@blp.route("/")
class ProjectList(MethodView):
    @blp.response(200, ProjectSchema(many=True))
    def get(self):
        return db.session.query(Project).order_by(Project.created_at).all()

    @blp.arguments(ProjectSchema)
    @blp.response(201, ProjectSchema)
    def post(self, new_data):
        project = Project(**new_data)
        db.session.add(project)
        db.session.commit()
        return project


@blp.route("/<uuid:project_id>")
class ProjectItem(MethodView):
    @blp.response(200, ProjectSchema)
    def get(self, project_id):
        return get_or_404(Project, project_id, "Project not found")

    @blp.arguments(ProjectUpdateSchema)
    @blp.response(200, ProjectSchema)
    def patch(self, update_data, project_id):
        project = get_or_404(Project, project_id, "Project not found")
        for key, value in update_data.items():
            setattr(project, key, value)
        db.session.commit()
        return project

    @blp.response(204)
    def delete(self, project_id):
        project = get_or_404(Project, project_id, "Project not found")
        db.session.delete(project)
        db.session.commit()
