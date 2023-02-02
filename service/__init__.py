from flask import Flask
import os

openai_key = None


def create_app():
    global openai_key
    openai_key = os.getenv("OPENAI_API_KEY")

    app = Flask(__name__)

    with app.app_context():
        # Imports
        # Flake8 complains that the following is an unused import. But it is
        # indeed used. Hence this line has been disabled in Flake8
        from . import question_answering_service  # noqa: F401

        return app
