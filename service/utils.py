import pickle


def get_document_embeddings():
    with open('data/choreo_document_embeddings.pkl', 'rb') as f:
        document_embeddings = pickle.load(f)

    return document_embeddings


def get_question_embeddings():
    with open('data/choreo_question_embeddings.pkl', 'rb') as f:
        question_embeddings = pickle.load(f)

    return question_embeddings
