import os

import numpy as np
import openai
import pandas as pd
import tiktoken

from service.constants import COMPLETIONS_API_PARAMS, ENCODING, MAX_SECTION_LEN, SEPARATOR, EMBEDDING_MODEL
from service.utils import get_document_embeddings, get_question_embeddings


def get_embedding(text):

    result = openai.Embedding.create(
      model=EMBEDDING_MODEL,
      input=text
    )

    return result["data"][0]["embedding"]


def vector_similarity(x, y):
    """
    Returns the similarity between two vectors.

    Because OpenAI Embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    """
    return np.dot(np.array(x), np.array(y))


def order_document_sections_by_query_similarity(query):
    """
    Find the query embedding for the supplied query, and compare it against all of the pre-calculated document embeddings
    to find the most relevant sections.

    Return the list of document sections, sorted by relevance in descending order.
    """

    question_embeddings = get_question_embeddings()

    if query in question_embeddings:
        query_embedding = question_embeddings[query]
    else:
        query_embedding = get_embedding(query)

    contexts = get_document_embeddings()

    document_similarities = sorted([
        (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in contexts.items()
    ], reverse=True)

    return document_similarities


def construct_prompt(question) -> str:
    """
    Fetch relevant
    """
    most_relevant_document_sections = order_document_sections_by_query_similarity(question)

    chosen_sections = []
    chosen_sections_len = 0
    chosen_sections_indexes = []

    encoding = tiktoken.get_encoding(ENCODING)
    separator_len = len(encoding.encode(SEPARATOR))

    df = pd.read_csv("data/choreo_docs_library_with_tokens.csv")
    df = df.set_index(["title", "heading"])
    df = df.sort_index()

    for _, section_index in most_relevant_document_sections:
        # Add contexts until we run out of space.
        document_section = df.loc[section_index].iloc[0]

        chosen_sections_len += document_section.tokens + separator_len
        if chosen_sections_len > MAX_SECTION_LEN:
            break

        chosen_sections.append(SEPARATOR + document_section.content.replace("\n", " "))
        chosen_sections_indexes.append(str(section_index))

    # Useful diagnostic information
    # print(f"Selected {len(chosen_sections)} document sections:")
    # print("\n".join(chosen_sections_indexes))

    header = """Answer the question as truthfully as possible using the provided context, and if the answer is not 
    contained within the text below, say "I don't know."\n\nContext:\n"""

    return header + "".join(chosen_sections) + "\n\n Q: " + question + "\n A:"


def answer_query_with_context(query, show_prompt=False):

    prompt = construct_prompt(query)

    if show_prompt:
        print('Completion model:', COMPLETIONS_API_PARAMS['model'])
        print(prompt)

    response = openai.Completion.create(
        prompt=prompt,
        **COMPLETIONS_API_PARAMS
    )

    return response["choices"][0]["text"].strip(" \n")


if __name__ == "__main__":

    openai.api_key = os.getenv("OPENAI_API_KEY")
    question = "What is WSO2 Choreo?"
    answer = answer_query_with_context(question)
    print(answer)
