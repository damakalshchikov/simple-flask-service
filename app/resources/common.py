from uuid import UUID

from flask_smorest import abort

from app.extensions import Base, db


def get_or_404[ModelT: Base](model: type[ModelT], id_: UUID, message: str) -> ModelT:
    obj = db.session.get(model, id_)
    if obj is None:
        abort(404, message=message)
    assert obj is not None
    return obj
