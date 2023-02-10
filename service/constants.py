import os.path

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

MAX_SECTION_LEN = 1500
SEPARATOR = "\n* "
ENCODING = "cl100k_base"  # encoding for text-embedding-ada-002

COMPLETIONS_API_PARAMS = {
    "temperature": 0.7,
    "max_tokens": 500,
    "model": COMPLETIONS_MODEL,
}

DATA_DIR = "data"
DOCUMENT_LIBRARY_PATH = os.path.join(DATA_DIR, "choreo_docs_library_with_tokens.csv")
DOCUMENT_EMBEDDINGS_PATH = os.path.join(DATA_DIR, "choreo_document_embeddings.pkl")
QUESTION_EMBEDDINGS_PATH = os.path.join(DATA_DIR, "choreo_question_embeddings.pkl")
QUESTIONS_AND_ANSWERS_PATH = os.path.join(DATA_DIR, "questions_and_answers.csv")

GS_CREDENTIALS_PATH = "/config/gs_credentials.json"
