import logging
import pickle

from gspread import SpreadsheetNotFound

from service import gsclient
from service.constants import DOCUMENT_EMBEDDINGS_PATH, QUESTION_EMBEDDINGS_PATH


def get_document_embeddings():
    with open(DOCUMENT_EMBEDDINGS_PATH, 'rb') as f:
        document_embeddings = pickle.load(f)

    return document_embeddings


def get_question_embeddings():
    with open(QUESTION_EMBEDDINGS_PATH, 'rb') as f:
        question_embeddings = pickle.load(f)

    return question_embeddings


def save_questions_and_answers(question, answer):
    if gsclient:
        try:
            sheet = gsclient.open("Choreo Chatbot - Collected Data").sheet1
            sheet.append_row([question, answer])

        except SpreadsheetNotFound:
            logging.error("Spreadsheet to write the data not found. Creating new spreadsheet.",
                          exc_info=True)
            sheet = gsclient.create("Choreo Chatbot - Collected Data")
            sheet.share('jayanih@wso2.com', perm_type='user', role='writer')
            sheet = gsclient.open("NewDatabase").sheet1
            sheet.append_row('Question', 'Answer')
            sheet.append_row([question, answer])

        except Exception as e:
            logging.error("Error writing questions and answers to google sheet: " + str(e), exc_info=True)

