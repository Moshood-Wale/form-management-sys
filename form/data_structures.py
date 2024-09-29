from datetime import datetime
from bson import ObjectId

class Field:
    def __init__(self, name, field_type, options=None, required=False):
        self.name = name
        self.field_type = field_type
        self.options = options
        self.required = required

    def to_dict(self):
        return {
            "name": self.name,
            "field_type": self.field_type,
            "options": self.options,
            "required": self.required
        }

class Form:
    def __init__(self, title, description, fields, created_by, created_at=None, _id=None, submission_count=0):
        self._id = _id if isinstance(_id, ObjectId) else ObjectId(_id) if _id else ObjectId()
        self.title = title
        self.description = description
        self.fields = [Field(**f) if isinstance(f, dict) else f for f in fields]
        self.created_by = created_by
        self.created_at = created_at if isinstance(created_at, datetime) else datetime.fromisoformat(created_at) if created_at else datetime.utcnow()
        self.submission_count = submission_count

    def to_dict(self):
        return {
            "_id": str(self._id),
            "title": self.title,
            "description": self.description,
            "fields": [f.to_dict() for f in self.fields],
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "submission_count": self.submission_count
        }

class FormResponse:
    def __init__(self, form_id, responses, submitted_at=None, _id=None):
        self._id = _id if isinstance(_id, ObjectId) else ObjectId(_id) if _id else ObjectId()
        self.form_id = form_id if isinstance(form_id, ObjectId) else ObjectId(form_id)
        self.responses = responses
        self.submitted_at = submitted_at if isinstance(submitted_at, datetime) else datetime.fromisoformat(submitted_at) if submitted_at else datetime.utcnow()

    def to_dict(self):
        return {
            "_id": str(self._id),
            "form_id": str(self.form_id),
            "responses": self.responses,
            "submitted_at": self.submitted_at.isoformat()
        }