from flask_restx import Resource


class HealthResource(Resource):
    def get(self):
        return {"message": "App is healthy"}
