from flask import request
from service.question_answering import answer_query_with_context
from flask import current_app as app


@app.route('/generate_answer', methods=['POST'])
def generate_answer():

    json_body = request.json
    question = json_body.get('question')
    answer = answer_query_with_context(question)

    return {
        'answer': answer
    }
