from flask import Flask
from middlewares import check_authorization
from settings.helpers import AppSetup, create_app


application: Flask = create_app()
app_setup = AppSetup(application).configure_app()
api = app_setup.api
parser = app_setup.parser

check_authorization(application)
