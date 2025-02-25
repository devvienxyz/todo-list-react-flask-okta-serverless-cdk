import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_restx.reqparse import RequestParser
from api.experiments import ExperimentListResource
from settings import config


def create_app() -> Flask:
    return Flask(
        __name__,
        static_folder="build",
        static_url_path="/",
    )


def setup_parser() -> RequestParser:
    _parser = RequestParser()
    _parser.add_argument("task")
    return _parser


class AppSetup:

    def __init__(self, application):
        self.application: Flask = application
        self.application.config.update(self.__get_conf())
        self.api: Api = Api(
            self.application, version=1.0, title="Devvien's Todo-list"
        )
        self.parser: RequestParser = setup_parser()

    def __get_conf(self):
        """Private method to access the app config dict."""
        return {
            "OIDC_CLIENT_SECRETS": "./client_secrets.json",
            "OIDC_RESOURCE_SERVER_ONLY": True,
            "SECRET_KEY": config.SECRET_KEY,
        }

    def config_cors(self):
        self.cors = CORS(
            self.application, origins=config.CORS_ORIGINS, supports_credentials=True
        )
        return self

    def config_logger(self):
        self.application.logger.setLevel(logging.INFO)
        # rotate every 1 MB, keep up to 3 backups
        file_handler = RotatingFileHandler("/tmp/app.log", maxBytes=1e6, backupCount=3)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        self.application.logger.addHandler(file_handler)
        return self

    def config_api(self):
        experiment_ns = self.api.namespace(
            "experiments", description="Assay experiments."
        )
        experiment_ns.add_resource(ExperimentListResource, "/")
        # TODO: enable back when ready
        # experiment_ns.add_resource(ExperimentResource, "/<string:experiment_id>")

    def configure_app(self):
        self.config_cors().config_logger().config_api()
        return self
