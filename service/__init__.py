import logging

import gspread
from flask import Flask
import os

from oauth2client.service_account import ServiceAccountCredentials

from service.constants import GS_CREDENTIALS_PATH

openai_key = None
gsclient = None


def create_app():
    global openai_key
    global gsclient
    openai_key = os.getenv("OPENAI_API_KEY")

    scope = ['https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive"]

    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(GS_CREDENTIALS_PATH, scope)
        gsclient = gspread.authorize(credentials)

    except Exception as e:
        logging.error("Error authorizing google sheets client : " + str(e), exc_info=True)
        gsclient = None

    app = Flask(__name__)

    with app.app_context():
        # Imports
        # Flake8 complains that the following is an unused import. But it is
        # indeed used. Hence this line has been disabled in Flake8
        from . import question_answering_service  # noqa: F401

        return app
