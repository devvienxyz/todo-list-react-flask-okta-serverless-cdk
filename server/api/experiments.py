from flask import jsonify, request, make_response
from flask_restx import Resource
from pydantic_core import ValidationError

from services.experiment import experiment_service
from utils.logger import logger


class ExperimentListResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self):
        try:
            experiments = experiment_service.get_all()
            return make_response({"experiments": experiments}, 200)

        except Exception as e:
            logger.exception(e)
            return make_response("", 500)

    def post(self):
        try:
            experiment = experiment_service.create_instance_from_form_data(request.form)
            response = experiment_service.create(experiment)
            return make_response("", 201 if response else 400)

        except ValidationError as val_e:
            errors = [
                {"field": ".".join(map(str, err["loc"])), "message": err["msg"]}
                for err in val_e.errors()
            ]
            logger.exception(errors)
            return make_response(jsonify({"error": errors}), 400)

        except Exception as e:
            logger.exception(e)
            return make_response("", 500)


class ExperimentResource(Resource):
    PATCH_ALLOWED_ATTRS = [
        "title",
        "notes",
    ]

    def patch(self, experiment_id):
        try:
            # Check if all attributes are valid
            if not all(
                attr in self.PATCH_ALLOWED_ATTRS for attr in request.form.keys()
            ):
                return make_response(
                    {
                        "error": f"The only editable attributes are [{self.PATCH_ALLOWED_ATTRS}]."
                    },
                    400,
                )

            experiment_id = experiment_service.update(
                experiment_id=experiment_id, attrs_to_update=request.form
            )
            return make_response({"experiment_id": experiment_id}, 200)

        except Exception:
            return make_response("", 500)

    def delete(self, experiment_id):
        try:
            if experiment_id is None:
                return make_response({"error": "Experiment id is required."}, 400)

            delete_count = experiment_service.delete(experiment_id=experiment_id)

            if delete_count:
                return make_response({"acknowledged": True}, 200)
            return make_response({"acknowledged": False}, 400)

        except Exception:
            return make_response("", 500)
