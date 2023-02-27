import os.path

COMPLETIONS_MODEL = "davinci"
EMBEDDING_MODEL = "embedding"

MAX_SECTION_LEN = 1500
SEPARATOR = "\n* "
ENCODING = "cl100k_base"  # encoding for text-embedding-ada-002

COMPLETIONS_API_PARAMS = {
    "temperature": 0.7,
    "max_tokens": 500,
    "engine": COMPLETIONS_MODEL,
}

DATA_DIR = "data"
DOCUMENT_LIBRARY_PATH = os.path.join(DATA_DIR, "choreo_information_library.csv")
DOCUMENT_EMBEDDINGS_PATH = os.path.join(DATA_DIR, "choreo_document_embeddings.pkl")
QUESTION_EMBEDDINGS_PATH = os.path.join(DATA_DIR, "choreo_question_embeddings.pkl")

GS_CREDENTIALS_PATH = "/config/gs_credentials.json"
