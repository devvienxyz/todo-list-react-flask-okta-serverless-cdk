from flask_restx import Resource

from ..utils.activity_history import create_activity_history_mock_data


class CoreAPIResource(Resource):
    
    def get(self):
        return {
            "mock_activity_history": create_activity_history_mock_data()
        }
