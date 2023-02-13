import logging
import threading

from flask import request
from service.question_answering import answer_query_with_context
from flask import current_app as app

from service.utils import save_questions_and_answers


@app.route('/generate_answer', methods=['POST'])
def generate_answer():

    try:
        json_body = request.json
        question = json_body.get('question')

        answer = answer_query_with_context(question)
        thread = threading.Thread(target=save_questions_and_answers, args=(question, answer,))
        thread.start()

        return {
            'answer': answer
        }

    except Exception as e:
        logging.error("Request is not properly formatted: " + str(e), exc_info=True)
        return {
            'answer': ""
        }
