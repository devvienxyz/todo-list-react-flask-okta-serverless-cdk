from flask_restx import Resource
from analyzer.index import Analyzer


class ActivityLogsAPIResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.analyzer = Analyzer()

    def get(self):
        return {
            "wells": [{
                "A1": "rgb(255,1,1)",
            }]
        }
