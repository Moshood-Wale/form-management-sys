from bson import ObjectId
from core.mongodb_client import db
from .data_structures import Form, FormResponse

class FormService:
    @staticmethod
    def create_form(form_data):
        form = Form(**form_data)
        result = db.forms.insert_one(form.to_dict())
        return str(result.inserted_id)

    @staticmethod
    def get_form(form_id):
        form_data = db.forms.find_one({"_id": ObjectId(form_id)})
        if form_data:
            try:
                return Form(**form_data).to_dict()
            except ValueError as e:
                # Log the error
                print(f"Error parsing form data: {e}")
                # Try to fix the date
                if 'created_at' in form_data and isinstance(form_data['created_at'], str):
                    form_data['created_at'] = datetime.utcnow()
                return Form(**form_data).to_dict()
        return None

    @staticmethod
    def update_form(form_id, form_data):
        result = db.forms.update_one(
            {"_id": ObjectId(form_id)},
            {"$set": form_data}
        )
        return result.modified_count > 0

    @staticmethod
    def delete_form(form_id):
        result = db.forms.delete_one({"_id": ObjectId(form_id)})
        return result.deleted_count > 0

    @staticmethod
    def get_all_forms():
        forms = db.forms.find().sort("created_at", -1)  # Sort by creation date, newest first
        return [Form(**form).to_dict() for form in forms]

    @staticmethod
    def submit_response(form_id, response_data):
        form = FormService.get_form(form_id)
        if not form:
            raise ValueError("Form not found")

        FormService.validate_response(form, response_data)

        response = FormResponse(form_id=ObjectId(form_id), responses=response_data)
        result = db.form_responses.insert_one(response.to_dict())

        db.forms.update_one(
            {"_id": ObjectId(form_id)},
            {"$inc": {"submission_count": 1}}
        )

        return str(result.inserted_id)

    @staticmethod
    def validate_response(form, response_data):
        for field in form['fields']:
            if field['required'] and field['name'] not in response_data:
                raise ValueError(f"Required field '{field['name']}' is missing")

    @staticmethod
    def get_form_responses(form_id):
        responses = db.form_responses.find({"form_id": ObjectId(form_id)})
        return [FormResponse(**response).to_dict() for response in responses]

    @staticmethod
    def get_form_analytics(form_id):
        form = FormService.get_form(form_id)
        return {"submission_count": form['submission_count'] if form else 0}