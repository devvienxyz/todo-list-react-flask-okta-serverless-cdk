from flask_restx import Resource


class StatsAPIResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Collective stats for the current observation session:

        Start of session
        End of session
        Running time
        Count for the ff:
        - Blue
        - Pink
        - Colorless

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return {
        #   "start_of_session": start_of_session,
        #   "end_of_session": end_of_session,
        #   "running_time_in_ms": running_time_in_ms,
        #   "color_count": {
        #       "blue": blue_wells,
        #       "pink": pink_wells,
        #       "colorless": colorless_wells
        #   },
        }
