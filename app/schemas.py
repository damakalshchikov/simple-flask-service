import marshmallow as ma
from marshmallow import validate

TASK_STATUSES = ["todo", "in_progress", "done"]
TASK_PRIORITIES = ["low", "medium", "high"]


class ProjectSchema(ma.Schema):
    id = ma.fields.UUID(dump_only=True)
    name = ma.fields.String(required=True, validate=validate.Length(min=1, max=255))
    description = ma.fields.String(allow_none=True, load_default=None)
    created_at = ma.fields.DateTime(dump_only=True)


class ProjectUpdateSchema(ma.Schema):
    name = ma.fields.String(validate=validate.Length(min=1, max=255))
    description = ma.fields.String(allow_none=True)


class TaskSchema(ma.Schema):
    id = ma.fields.UUID(dump_only=True)
    project_id = ma.fields.UUID(required=True)
    title = ma.fields.String(required=True, validate=validate.Length(min=1, max=255))
    description = ma.fields.String(allow_none=True, load_default=None)
    status = ma.fields.String(validate=validate.OneOf(TASK_STATUSES), load_default="todo")
    priority = ma.fields.String(validate=validate.OneOf(TASK_PRIORITIES), load_default="medium")
    assignee = ma.fields.String(allow_none=True, load_default=None)
    due_date = ma.fields.Date(allow_none=True, load_default=None)
    created_at = ma.fields.DateTime(dump_only=True)
    updated_at = ma.fields.DateTime(dump_only=True)


class TaskUpdateSchema(ma.Schema):
    title = ma.fields.String(validate=validate.Length(min=1, max=255))
    description = ma.fields.String(allow_none=True)
    status = ma.fields.String(validate=validate.OneOf(TASK_STATUSES))
    priority = ma.fields.String(validate=validate.OneOf(TASK_PRIORITIES))
    assignee = ma.fields.String(allow_none=True)
    due_date = ma.fields.Date(allow_none=True)


class TaskQueryArgsSchema(ma.Schema):
    class Meta:
        unknown = ma.EXCLUDE

    project_id = ma.fields.UUID(load_default=None)
    status = ma.fields.String(validate=validate.OneOf(TASK_STATUSES), load_default=None)


class TaskCommentSchema(ma.Schema):
    id = ma.fields.UUID(dump_only=True)
    task_id = ma.fields.UUID(dump_only=True)
    author = ma.fields.String(required=True, validate=validate.Length(min=1, max=255))
    body = ma.fields.String(required=True, validate=validate.Length(min=1))
    created_at = ma.fields.DateTime(dump_only=True)


class TaskCommentCreateSchema(ma.Schema):
    author = ma.fields.String(required=True, validate=validate.Length(min=1, max=255))
    body = ma.fields.String(required=True, validate=validate.Length(min=1))
