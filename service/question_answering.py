import logging
import os
import time

import numpy as np
import openai
import pandas as pd
import tiktoken
import weaviate

from service.constants import COMPLETIONS_API_PARAMS, ENCODING, MAX_SECTION_LEN, SEPARATOR, EMBEDDING_MODEL, \
    DOCUMENT_LIBRARY_PATH
from service.utils import get_document_embeddings, get_question_embeddings

# initialize weaviate client for importing and searching
client = weaviate.Client("https://choreo-chatbot.weaviate.network",
                         timeout_config=(5, 60)
                         )


def get_embedding(text):

    result = openai.Embedding.create(
      engine=EMBEDDING_MODEL,
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


def search(query="", limit=3):
    before = time.time()
    vec = get_embedding(query)
    vec_took = time.time() - before

    before = time.time()
    near_vec = {"vector": vec}
    res = client \
        .query.get("ChoreoDocs", ["docs", "tokens", "_additional {certainty}"]) \
        .with_near_vector(near_vec) \
        .with_limit(limit) \
        .do()
    search_took = time.time() - before

    print("\nQuery \"{}\" with {} results took {:.3f}s ({:.3f}s to vectorize and {:.3f}s to search)" \
          .format(query, limit, vec_took+search_took, vec_took, search_took))
    documents = res["data"]["Get"]["ChoreoDocs"]
    return documents


def construct_prompt(question) -> str:
    """
    Fetch relevant
    """
    most_relevant_document_sections = search(question, limit=10)

    chosen_sections = []
    chosen_sections_len = 0

    encoding = tiktoken.get_encoding(ENCODING)
    separator_len = len(encoding.encode(SEPARATOR))

    for document_section in most_relevant_document_sections:
        # Add contexts until we run out of space.
        chosen_sections_len += document_section['tokens'] + separator_len
        if chosen_sections_len > MAX_SECTION_LEN:
            break

        chosen_sections.append(SEPARATOR + document_section['docs'].replace("\n", " "))

    # Useful diagnostic information
    # print(f"Selected {len(chosen_sections)} document sections:")
    # print("\n".join(chosen_sections_indexes))

    header = """Answer the question as truthfully as possible using the provided context, and if the answer is not 
    contained within the text below, say "Sorry, I didn't understand the question. 
    If it is about Choreo, could you please rephrase it and try again?"\n\nContext:\n"""

    return header + "".join(chosen_sections) + "\n\n Q: " + question + "\n A:"


def answer_query_with_context(query, show_prompt=False):

    prompt = construct_prompt(query)

    if show_prompt:
        print('Completion model:', COMPLETIONS_API_PARAMS['model'])
        print(prompt)

    try:

        response = openai.Completion.create(
            prompt=prompt,
            **COMPLETIONS_API_PARAMS
        )

        return response["choices"][0]["text"].strip(" \n")


    except Exception as e:
        logging.error("Failed to generate response from the model: " + str(e), exc_info=True)
        return "Sorry, there was an error generating the answer. Could you please try again?"
